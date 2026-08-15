"""HCB 汇编所需的静态数据（引擎知识库）。

本包集中管理所有硬编码数据表，适配其它 HCB 脚本时只需修改这里：

- :mod:`hcb_builder.data.constants`  全局常量与头尾模板
- :mod:`hcb_builder.data.bg_list`    背景表
- :mod:`hcb_builder.data.cha_list`   角色表
- :mod:`hcb_builder.data.cg_loaded`  内置的 CG 已加载偏移表
"""

from .bg_list import BG_LIST
from .cg_loaded import CG_LOADED
from .cha_list import CHA_LIST
from .constants import (
    BASE_OFFSET,
    ENDER_BYTES,
    HEADER_BYTES,
    INSTRUCTION_REFERENCE,
    STRING_ENCODING,
)

__all__ = [
    "BASE_OFFSET",
    "BG_LIST",
    "CG_LOADED",
    "CHA_LIST",
    "ENDER_BYTES",
    "HEADER_BYTES",
    "INSTRUCTION_REFERENCE",
    "STRING_ENCODING",
]
