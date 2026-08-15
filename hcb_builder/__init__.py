"""HCB 剧本汇编器（工程化重构版）。

把人类可读的剧本 DSL 汇编成 HCB 字节码，再嫁接到原版 ``base.chb``
模板上，输出目标引擎可执行的脚本文件。

模块划分：

- :mod:`hcb_builder.opcodes`    字节码编码原语
- :mod:`hcb_builder.data`       常量表与资源表加载
- :mod:`hcb_builder.generators` 各剧本指令的字节码生成器
- :mod:`hcb_builder.assembler`  汇编器核心（字节流、符号表、跳转回填）
- :mod:`hcb_builder.parser`     剧本文本解析
- :mod:`hcb_builder.builder`    文件组装与写出

典型用法::

    from hcb_builder import Assembler, build_script, parse_script

    asm = Assembler(...)
    parse_script(asm, "test.txt")
    build_script(asm, "base.chb", ".test.chb")
"""

from .assembler import Assembler
from .builder import build_script
from .parser import parse_script

__all__ = ["Assembler", "build_script", "parse_script"]
