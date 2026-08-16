"""Python DSL 层：把 HCB 剧本指令封装为类方法。

继承 :class:`HCBScript` 并覆写 ``constructor``，即可用方法调用方式撰写剧本，
然后调用 :meth:`HCBScript.build` 直接产出 HCB 文件。

用法示例::

    from cli import HCBScript

    class Foo(HCBScript):
        def constructor(self):
            self.cgload("chiwa_fd01a")   # 必须在 start 之前
            self.start()
            self.bg(67)                  # 背景 67
            self.dia("显示背景")
            self.bgm(3)                  # 播放 BGM 3
            self.cha("千和")              # 说话人
            self.dia("……你好。")
            self.end()

    Foo().build("out.chb")               # 直接生成 HCB 文件

标签与跳转::

    class Loop(HCBScript):
        def constructor(self):
            self.start()
            self.label("loop")           # ::loop
            self.dia("循环中")
            self.jump("loop")            # 跳回 ::loop
            self.end()
"""

from __future__ import annotations

from hcb_builder import Assembler, build_script
from hcb_builder.data import (
    BASE_OFFSET,
    BG_LIST,
    CG_LOADED,
    CHA_LIST,
    ENDER_BYTES,
    HEADER_BYTES,
    SCRIPT_ENCODING,
    STRING_ENCODING,
)
from hcb_builder.parser import RAW_COMMANDS

# ---------------------------------------------------------------------- #
# 常用参数常量（可直接导入使用）
# ---------------------------------------------------------------------- #

# 对话框位置（msg 参数）
MSG_MIDDLE: str = "middle"
MSG_NORMAL: str = "normal"
MSG_BOXIN: str = "boxin"
MSG_BOXOUT: str = "boxout"

# 音效模式（se 参数）
SE_LOOP: str = "loop"
SE_END: str = "end"

# 立绘站位（bs 的 loc 参数）
LOC_LEFT: str = "l"
LOC_MIDDLE: str = "m"
LOC_RIGHT: str = "r"

# 立绘构图状态（bs 的 layout 参数）
LAYOUT_L: int = 0
LAYOUT_U: int = 1
LAYOUT_S: int = 2
LAYOUT_DEFAULT: int = -1
LAYOUT_CLEAR: int = -10


def _ensure_label(name: str) -> str:
    """把标签名规范为 ``::name`` 形式（无前缀时自动补 ``::``）。"""
    return name if name.startswith("::") else f"::{name}"


class HCBScript:
    """HCB 剧本 DSL 基类。

    子类覆写 :meth:`constructor`，在其中调用各指令方法（``self.cha(...)`` 等）。
    每个指令方法都返回 ``self``，可链式调用。
    """

    def __init__(self) -> None:
        self._asm = Assembler(
            base_off=BASE_OFFSET,
            str_code=STRING_ENCODING,
            cg_loaded=CG_LOADED,
            bg_list=BG_LIST,
            cha_list=CHA_LIST,
            script_encoding=SCRIPT_ENCODING,
        )
        self._constructed = False

    # ------------------------------------------------------------------ #
    # 生命周期
    # ------------------------------------------------------------------ #
    def constructor(self) -> None:
        """子类覆写此方法，定义剧本内容。"""
        raise NotImplementedError("请覆写 constructor() 并调用指令方法")

    def _ensure_constructed(self) -> None:
        """确保 ``constructor`` 只执行一次。"""
        if not self._constructed:
            self.constructor()
            self._constructed = True

    def assemble(self) -> bytes:
        """执行剧本构造并回填跳转，返回最终脚本字节（不写文件）。"""
        self._ensure_constructed()
        return self._asm.resolve()

    def build(self, out_path: str = "out.chb") -> str:
        """执行剧本构造并写出 HCB 文件，返回输出路径。"""
        self._ensure_constructed()
        build_script(self._asm, out_path)
        return out_path

    # ------------------------------------------------------------------ #
    # 结构指令
    # ------------------------------------------------------------------ #
    def start(self) -> "HCBScript":
        """脚本开始标志（必须），展开为头部模板。"""
        self._asm.isstart += 1
        self._asm.append(HEADER_BYTES)
        return self

    def end(self) -> "HCBScript":
        """脚本结束标志（必须），展开为尾部模板。"""
        self._asm.isend += 1
        self._asm.append(ENDER_BYTES)
        return self

    def label(self, name: str) -> "HCBScript":
        """定义跳转标签（等价 ``::name``）。"""
        self._asm.register_current_label(_ensure_label(name))
        return self

    def jump(self, target: str) -> "HCBScript":
        """无条件跳转到标签。"""
        self._asm.append(self._asm.emit_jump("jump", _ensure_label(target)))
        return self

    # ------------------------------------------------------------------ #
    # 资源加载
    # ------------------------------------------------------------------ #
    def cgload(self, name: str) -> "HCBScript":
        """加载 CG 资源，必须在 :meth:`start` 之前调用。"""
        if self._asm.isstart != 0:
            self._asm.logger.warning("cgload 必须放在 start 之前，已忽略: %s", name)
            return self
        cg_offset = self._asm.base_off + self._asm.length_now
        result = self._asm.gen_cgload(name)
        self._asm.append(result)
        self._asm.cg_loaded[name.upper()] = cg_offset
        self._asm.new_off += len(result)
        return self

    def chaload(self, realname: str, aliases: dict[str, int] | None = None) -> "HCBScript":
        """动态定义说话人（SPEAK）函数，必须在 :meth:`start` 之前调用。

        ``aliases`` 为 ``{显示名: 名义编号}`` 映射；省略时仅支持真实名显示。
        """
        if self._asm.isstart != 0:
            self._asm.logger.warning("chaload 必须放在 start 之前，已忽略: %s", realname)
            return self
        parts = [realname] + [f"{num}:{showname}" for showname, num in (aliases or {}).items()]
        result = self._asm.gen_chaload(parts)
        self._asm.append(result)
        self._asm.new_off += len(result)
        return self

    # ------------------------------------------------------------------ #
    # 背景 / CG
    # ------------------------------------------------------------------ #
    def bg(self, number: int, variant: int | None = None) -> "HCBScript":
        """设置背景。

        ``variant`` 可选，为背景细分编号。
        """
        args = [str(number)] if variant is None else [str(number), str(variant)]
        self._asm.append(self._asm.gen_bgset(args))
        return self

    def cg(
        self,
        name: str,
        x: int | None = None,
        y: int | None = None,
        zoom: float | None = None,
        time: int | None = None,
    ) -> "HCBScript":
        """显示 CG。省略 x/y/zoom/time 时沿用该 CG 的内置设定。

        ``zoom`` 以 1 为原始大小（内部换算 ``3000 - zoom*1000``）。
        """
        if x is None or y is None or zoom is None or time is None:
            args = [name]
        else:
            args = [name, str(x), str(y), str(zoom), str(time)]
        self._asm.append(self._asm.gen_cgset(args))
        return self

    # ------------------------------------------------------------------ #
    # 立绘
    # ------------------------------------------------------------------ #
    def bs(
        self,
        character: int,
        pose: int,
        costume: int,
        expression: int,
        layout: int = -1,
        loc: str = "m",
        z: int = 0,
        x: int = 0,
        y: int = 0,
        layer: int = 1,
    ) -> "HCBScript":
        """设置立绘。

        - ``layout``：构图状态，``0``=L、``1``=U、``2``=S、``-1``=默认；
        - ``loc``：站位，``'l'/'m'/'r'``；
        - ``z/x/y``：深度与坐标；``layer``：层次。
        """
        args = [
            str(character), str(pose), str(costume), str(expression),
            str(layout), loc, str(z), str(x), str(y), str(layer),
        ]
        self._asm.append(self._asm.gen_bsset(args))
        return self

    def bsfade(self) -> "HCBScript":
        """消除当前立绘。"""
        self._asm.append(self._asm.gen_bsfade())
        return self

    # ------------------------------------------------------------------ #
    # 音频
    # ------------------------------------------------------------------ #
    def bgm(self, number: int) -> "HCBScript":
        """播放 BGM。"""
        self._asm.append(self._asm.gen_bgmset(str(number)))
        return self

    def bgmstop(self) -> "HCBScript":
        """停止 BGM。"""
        self._asm.append(RAW_COMMANDS["bgmstop"])
        return self

    def se(
        self,
        number: int,
        mode: str | None = None,
        time: int | None = None,
    ) -> "HCBScript":
        """播放音效。

        - 省略 ``mode``：单次播放；
        - ``mode="loop"``：循环播放，``time`` 为循环时间参数；
        - ``mode="end"``：停止循环，``time`` 为收尾时长。
        """
        if mode is None:
            args = [str(number)]
        elif mode in ("loop", "end"):
            args = [str(number), mode, str(time)]
        else:
            raise ValueError(f"未知音效模式 {mode!r}，应为 loop / end 或省略")
        self._asm.append(self._asm.gen_seset(args))
        return self

    # ------------------------------------------------------------------ #
    # 对话
    # ------------------------------------------------------------------ #
    def msg(self, position: str) -> "HCBScript":
        """对话框位置 / 显隐。``position`` 为 middle / normal / boxin / boxout。"""
        self._asm.append(self._asm.gen_msgset(position))
        return self

    def cha(self, name: str, voice: int | None = None) -> "HCBScript":
        """设置说话人。

        ``name`` 支持 ``角色名`` 或 ``角色名/显示名``（如 ``真白/？？？``）。
        """
        args = [name] if voice is None else [name, str(voice)]
        self._asm.append(self._asm.gen_chaset(args))
        return self

    def dia(self, text: str) -> "HCBScript":
        """显示对话文本。"""
        self._asm.append(self._asm.gen_diaset(text))
        return self

    def speak(self, name: str, text: str, voice: int | None = None) -> "HCBScript":
        """便捷组合：设置说话人并显示一句台词（等价 cha + dia）。"""
        self.cha(name, voice)
        self.dia(text)
        return self

    # ------------------------------------------------------------------ #
    # 选项
    # ------------------------------------------------------------------ #
    def sel_start(self, text: str) -> "HCBScript":
        """选项开始，渲染标题文本。"""
        self._asm.append(self._asm.gen_selset(["start", text]))
        return self

    def sel_op(self, text: str, target: str) -> "HCBScript":
        """单个选项项，选中后跳转到 ``target`` 标签。"""
        self._asm.append(self._asm.gen_selset(["op", text, _ensure_label(target)]))
        return self

    def sel_end(self) -> "HCBScript":
        """选项结束，生成 G[103] 逐项比较分支。"""
        self._asm.append(self._asm.gen_selset(["end"]))
        return self

    # ------------------------------------------------------------------ #
    # 特效
    # ------------------------------------------------------------------ #
    def white(self) -> "HCBScript":
        """背景调白（白屏）。"""
        self._asm.append(RAW_COMMANDS["white"])
        return self

    def eyecatch(self) -> "HCBScript":
        """转场效果。"""
        self._asm.append(RAW_COMMANDS["eyecatch"])
        return self
