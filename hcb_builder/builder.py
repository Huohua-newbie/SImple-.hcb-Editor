"""文件组装：把汇编结果写回 ``base.chb`` 模板，产出可执行脚本。

原版 ``base.chb`` 结构：:

    [0:4]            总长度/主区偏移字段 L0（小端）
    [4:base_off]     常量区（函数表、资源索引等）
    [base_off:L0]    脚本正文区
    [L0:EOF]         main 主体（引擎入口/收尾）

组装输出：:

    [0:4]            base_off + length_now（新脚本总偏移）
    [4:base_off]     原常量区（其中的旧基址被重定位为 new_off）
    [base_off:...]   新脚本正文（return_bytes，已回填跳转）
    [...:EOF]        原 main 主体（原样追加）
"""

from __future__ import annotations

import logging

from .assembler import Assembler
from .data import load_base_chb

logger = logging.getLogger("hcb_builder")


def build_script(asm: Assembler, out_path: str) -> None:
    """读取内置模板 ``base.chb``，替换脚本正文后写出新文件。

    参数:
        asm: 已解析完成的 :class:`hcb_builder.assembler.Assembler`。
        out_path: 输出文件路径。
    """
    oribytes = load_base_chb()

    # 原文件头 4 字节 = main 主体起始偏移
    main_start = int.from_bytes(oribytes[:4], "little")
    mainender = oribytes[main_start:]

    # 新脚本总偏移
    total_offset = asm.base_off + asm.length_now

    # 常量区：旧基址重定位为 new_off（cgload 前置插入使正文后移）
    constants = oribytes[4: asm.base_off].replace(
        asm.base_off.to_bytes(4, "little"),
        asm.new_off.to_bytes(4, "little"),
    )

    # 回填跳转后的最终正文
    body = asm.resolve()

    with open(out_path, "wb") as h:
        h.write(total_offset.to_bytes(4, "little"))
        h.write(constants)
        h.write(body)
        h.write(mainender)

    logger.info(
        "写出 %s：总偏移 0x%08X，正文 %d 字节",
        out_path, total_offset, len(body),
    )
