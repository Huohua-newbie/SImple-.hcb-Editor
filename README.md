# HCB 剧本编译器（工程化重构版）

这是一个把**人类可读的剧本 DSL** 编译成 **HCB 字节码**、并嫁接回原版
`base.chb` 模板的工具。它来自对《さくら、もゆ。》体验版脚本格式的反向分析，
原版只有一个数百行的单文件脚本（旧 `hcb_build.py`）。本仓库将其拆分为一个
结构清晰的 Python 包，并补全了文档。

---

## 目录结构

```
SImple-.hcb-Editor/
├── hcb_build.py            # CLI 入口（薄封装，参数解析后调用包）
├── hcb_builder/            # 核心包
│   ├── __init__.py         # 包导出
│   ├── opcodes.py          # 字节码编码原语（值 → 字节）
│   ├── data.py             # 常量表与资源表加载（背景/角色/CG/头尾模板）
│   ├── generators.py       # 各剧本指令的字节码生成器（mixin）
│   ├── assembler.py        # 汇编器核心（字节流、符号表、跳转回填）
│   ├── parser.py           # 剧本文本解析（行分发）
│   └── builder.py          # 文件组装与写出
├── base.chb                # 原版模板（只读，提供常量区与 main 尾部）
├── cg_loaded.txt           # CG 已加载偏移表（资源名 ↔ 偏移）
├── test.txt                # 输入样例剧本（DSL）
└── README.md               # 本文档
```

---

## 快速开始

```powershell
# 在 SImple-.hcb-Editor 目录下
python hcb_build.py --script test.txt --base base.chb --out .test.chb -v
```

参数说明：

| 参数 | 默认值 | 含义 |
|---|---|---|
| `--script` | `test.txt` | 输入剧本文本 |
| `--base` | `base.chb` | 原版 `base.chb` 模板 |
| `--out` | `.test.chb` | 输出文件 |
| `--cg-list` | `cg_loaded.txt` | CG 已加载偏移表 |
| `-v` | 关 | 输出详细日志（info 级） |

也可以用库方式调用：

```python
from hcb_builder import Assembler, build_script, parse_script
from hcb_builder.data import BASE_OFFSET, STRING_ENCODING, BG_LIST, CHA_LIST, load_cg_loaded

asm = Assembler(
    base_off=BASE_OFFSET,
    str_code=STRING_ENCODING,
    cg_loaded=load_cg_loaded("cg_loaded.txt"),
    bg_list=BG_LIST,
    cha_list=CHA_LIST,
)
parse_script(asm, "test.txt")
build_script(asm, "base.chb", ".test.chb")
```

---

## 输入 DSL 语法

剧本是 GBK 编码的文本文件，支持三种行：

- **注释行**：以 `#` 开头；
- **标签行**：以 `::` 开头，如 `::loop`，用于跳转目标；
- **指令行**：`[指令,参数...]` 形式。

### 指令一览

| 指令 | 格式 | 说明 |
|---|---|---|
| `bg` | `[bg,编号]` 或 `[bg,编号,细分]` | 设置背景图 |
| `bgm` | `[bgm,编号]` | 播放 BGM |
| `bgmstop` | `[bgmstop]` | 停止 BGM |
| `se` | `[se,编号]` / `[se,编号,loop,时长]` / `[se,编号,end,时长]` | 音效（单次/循环/停止） |
| `msg` | `[msg,middle\|normal\|boxin\|boxout]` | 对话框位置/显示控制 |
| `cha` | `[cha,角色名]` 或 `[cha,角色名/显示名,语音编号]` | 设置说话人（可选语音） |
| `dia` | `[dia,文本]` | 对话内容 |
| `cgload` | `[cgload,CG名]` | 加载 CG（必须放在 `[start]` 之前） |
| `cg` | `[cg,CG名]` 或 `[cg,CG名,x,y,zoom,time]` | 显示/设置 CG |
| `bs` | `[bs,cha,pose,cloth,face,l,'l/m/r',z,x,y,lyr]` | 设置立绘 |
| `bsfade` | `[bsfade]` | 消除立绘 |
| `sel` | `[sel,start,标题]` / `[sel,op,选项,目标]` / `[sel,end]` | 选项系统 |
| `jump` | `[jump,::标签]` | 无条件跳转 |
| `start` | `[start]` | 脚本头（展开为 `HEADER_BYTES`） |
| `end` | `[end]` | 脚本尾（展开为 `ENDER_BYTES`） |
| `white` | `[white]` | 背景调白 |
| `eyecatch` | `[eyecatch]` | 转场（eyecatch） |

### 选项示例

```
[sel,start,你要怎么做？]
[sel,op,选小猫,::target1]
[sel,op,选小狗,::target2]
[sel,end]
```

编译后在 `end` 处生成对全局变量 `G[103]` 的逐项比较分支：
选了第 1 项跳到 `::target1`，第 2 项跳到 `::target2`，未匹配则回到选项开头
（`::selectN`）。

### 立绘参数说明

`[bs,cha,pose,cloth,face,l,'l/m/r',z,x,y,lyr]` 中：

- 前 4 项：角色 / 姿势 / 服装 / 表情；
- `l`：构图状态。`0`=L、`1`=U、`2`=S、`-1`=默认、`-10` 清除当前立绘；
- `'l/m/r'`：预设站位（`l` 左=2、`m` 中=1、`r` 右=0）；
- `z/x/y`：深度与坐标；
- `lyr`：层次。

---

## HCB 文件格式

### base.chb 布局

```
[0:4]            总长度/主区偏移字段 L0（小端）
[4:base_off]     常量区（函数表、资源索引等）
[base_off:L0]    脚本正文区（引擎逐字节执行的指令流）
[L0:EOF]         main 主体（引擎入口/收尾）
```

其中 `base_off = 0x0008AEC7` 是原脚本正文区起始偏移。工具只替换正文区，
保留常量区与 main 主体，因此输出文件仍可被引擎正常加载执行。

### 输出组装逻辑

见 [`builder.py`](hcb_builder/builder.py)：

1. 读原模板，头 4 字节得到 main 主体起始位置 `L0`，取出 `mainender`；
2. 新头 4 字节写入 `base_off + length_now`（新脚本总偏移）；
3. 原样复制 `[4:base_off)` 常量区，并把其中出现的旧基址 `base_off`
   重定位为 `new_off`（因 `cgload` 块被前置插入，正文基址后移）；
4. 追加汇编出的正文（已回填跳转）；
5. 追加原 `mainender`。

---

## 字节码编码约定

见 [`opcodes.py`](hcb_builder/opcodes.py)：

| 操作码 | 字节 | 含义 |
|---|---|---|
| `OP_STRING` | `0x0e` | 字符串：1 字节长度 + 字节 + NUL |
| `OP_CALL` | `0x02` | 调用引擎内部函数：+ 4 字节小端地址 |
| `OP_U8` | `0x0c` | 单字节无符号整数 |
| `OP_U16` | `0x0b` | 双字节小端整数 |
| `OP_U32` | `0x0a` | 四字节小端整数 |
| `OP_NIL` | `0x08` | 空值 |
| `OP_NEG` | `0x19` | 取负后缀（数值字节后追加，表示负数） |
| `OP_JMP` | `0x06` | 无条件跳转：+ 4 字节目标地址 |
| `OP_JZ` | `0x07` | 条件跳转：+ 4 字节目标地址 |

> 负数编码：`-1` → `0x01 0x19`，`-2` → `0x02 0x19`，以此类推。

---

## 汇编流程（两阶段）

1. **生成阶段**（[`parser.py`](hcb_builder/parser.py) → [`generators.py`](hcb_builder/generators.py)）
   逐行解析 DSL，每条指令生成字节并追加到汇编器，同时累加 `length_now`。
   标签行把标签注册为 `base_off + length_now`；跳转指令先写入**全局唯一
   占位符**（从 `0xFFFFFFFF` 递减）并记入 `jmp_tem`。

2. **回填阶段**（[`assembler.py`](hcb_builder/assembler.py) 的 `resolve()`）
   遍历 `jmp_tem`，把占位符替换为 `jmp_real` 中登记的真实地址，产出最终字节流。

这种「先汇编、后链接」的方式与正规汇编器/链接器思路一致。

---

## 数据表

### 背景表 `BG_LIST`（[`data.py`](hcb_builder/data.py)）

`编号 -> [名称, function 地址(十六进制字符串)]`。地址会被转成小端字节序作为
`call` 操作数。

### 角色表 `CHA_LIST`

`名字 -> [角色 ID(function 偏移), 显示名, {别名: 别名编号}]`。别名编号为引擎
内置显示名枚举值，`？？？` 表示隐藏名。

### CG 表 `cg_loaded.txt`

每两行一组：奇数行为十六进制偏移，偶数行为带引号的 CG 名。`[cgload]` 指令会在
运行时把新 CG 名注册进此表（以当前偏移为地址）。

---

## 与原版的差异

| 项目 | 原版 | 重构版 |
|---|---|---|
| 结构 | 单文件 + 全局变量 | 分模块包，状态封装在 `Assembler` |
| 生成函数重复调用 | `return_bytes += f(...); length_now += len(f(...))` 调用两次 | 单次调用，消除副作用 |
| 路径硬编码 | `base/test.txt` 等 | CLI 参数，默认为平铺路径 |
| 日志 | `print` 混排 | `logging` 分级输出 |
| 数据修正 | `bg_list[73]` 地址带 `f_` 前缀 | 修正为纯十六进制 `00009345` |
| 未知指令/缺参 | 静默或崩溃 | 日志告警并跳过 |

> 其余字节级行为与原版保持一致，输出文件内容应与原版逻辑等价。

---

## 扩展指南

要适配其它 HCB 脚本，主要修改 [`data.py`](hcb_builder/data.py)：

1. 更新 `BASE_OFFSET`、`HEADER_BYTES`、`ENDER_BYTES`；
2. 更新 `BG_LIST`、`CHA_LIST` 与各指令的 function 偏移；
3. 必要时在 [`generators.py`](hcb_builder/generators.py) 调整入参编码。

如需新增指令：

1. 在 [`generators.py`](hcb_builder/generators.py) 添加 `gen_xxx` 方法；
2. 在 [`parser.py`](hcb_builder/parser.py) 的 `_dispatch` 中添加分发分支。
