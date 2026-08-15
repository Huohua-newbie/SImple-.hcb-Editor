"""汇编器核心：维护字节流、偏移计数、符号表与跳转占位符。

汇编采用「两阶段」策略：

1. 生成阶段：解析器把每条指令生成的字节交给 :meth:`Assembler.append`，
   同时累加当前偏移 ``length_now``；遇到跳转时先写入全局唯一的占位符，
   并把「标签 → 占位字节」记入 ``jmp_tem``。
2. 回填阶段：所有指令处理完后调用 :meth:`Assembler.resolve`，把占位符
   统一替换为 ``jmp_real`` 中登记的真实地址。
"""

from __future__ import annotations

import logging

from .generators import InstructionGenerators
from .opcodes import OP_JMP, OP_JZ, u32


class Assembler(InstructionGenerators):
    """HCB 脚本汇编器。

    参数:
        base_off: 原脚本正文区起始偏移（新脚本注入位置）。
        str_code: 剧本字符串编码，默认 ``gbk``。
        cg_loaded: CG 已加载偏移表 ``{CG名(大写): 偏移}``。
        bg_list: 背景表。
        cha_list: 角色表。
    """

    def __init__(self, base_off, str_code="gbk", cg_loaded=None,
                 bg_list=None, cha_list=None):
        self.base_off = int(base_off)
        self.str_code = str_code
        self.cg_loaded = dict(cg_loaded or {})
        self.bg_list = dict(bg_list or {})
        self.cha_list = dict(cha_list or {})
        self.logger = logging.getLogger("hcb_builder")

        # 输出缓冲区与累计偏移
        self.output = bytearray()
        self.length_now = 0

        # 流程状态
        self.isstart = 0
        self.isend = 0

        # 选项状态
        self.select_num = 0
        self.op_num = 0
        self.sel_target = []

        # 跳转符号表
        self.jmp_tem = {}     # 标签 -> 占位字节
        self.jmp_real = {}    # 标签 -> 真实地址字节
        self.tem_label = 0xFFFFFFFF  # 占位符从最高位递减，保证唯一

        # 立绘缓存
        self.bs_current = []

        # 重定位后正文基址（cgload 前置插入后增大）
        self.new_off = int(base_off)

    # ------------------------------------------------------------------ #
    # 字节流
    # ------------------------------------------------------------------ #
    def append(self, data: bytes) -> None:
        """追加字节并同步累加偏移计数。"""
        self.output += data
        self.length_now += len(data)

    # ------------------------------------------------------------------ #
    # 标签与跳转
    # ------------------------------------------------------------------ #
    def label_load(self, label, offset) -> None:
        """注册标签真实地址（仅首次定义生效，与源脚本行为一致）。"""
        if label not in self.jmp_real:
            self.jmp_real[label] = u32(offset)

    def register_current_label(self, label) -> None:
        """把标签注册为「当前偏移」处。"""
        self.label_load(label, self.base_off + self.length_now)

    def emit_jump(self, kind, target_label) -> bytes:
        """生成跳转指令字节；目标未解析时写入占位符并登记。

        参数:
            kind: ``"jump"``（无条件，0x06）或其它（条件 jz，0x07）。
            target_label: 目标标签，如 ``"::loop"``。
        """
        code = OP_JMP if kind == "jump" else OP_JZ
        if target_label in self.jmp_tem:
            placeholder = self.jmp_tem[target_label]
        else:
            placeholder = u32(self.tem_label)
            self.jmp_tem[target_label] = placeholder
            self.tem_label -= 1
        return code + placeholder

    def resolve(self) -> bytes:
        """回填所有跳转占位符为真实地址，返回最终字节流。"""
        data = bytes(self.output)
        for label, placeholder in self.jmp_tem.items():
            if label not in self.jmp_real:
                self.logger.warning("有未定义的 jump 目标: %s", label)
                continue
            data = data.replace(placeholder, self.jmp_real[label])
        return data
