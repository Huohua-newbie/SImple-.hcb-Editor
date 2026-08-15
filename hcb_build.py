"""HCB 剧本编译器 CLI 入口。

把人类可读的剧本 DSL 汇编成 HCB 字节码，并嫁接到原版 ``base.chb``
模板上输出可执行脚本。

用法::

    python hcb_build.py [选项]

常用选项::

    --script 剧本文件，默认 test.txt
    --base   原版 base.chb 模板，默认 base.chb
    --out    输出文件，默认 .test.chb
    -v       输出详细日志
"""

from __future__ import annotations

import argparse
import logging
import sys

from hcb_builder import Assembler, build_script, parse_script
from hcb_builder.data import (
    BASE_OFFSET,
    BG_LIST,
    CG_LOADED,
    CHA_LIST,
    STRING_ENCODING,
)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="把剧本 DSL 汇编为 HCB 字节码并嫁接到 base.chb 模板。"
    )
    parser.add_argument("--script", default="test.txt", help="剧本文本文件（默认 test.txt）")
    parser.add_argument("--base", default="base.chb", help="原版 base.chb 模板（默认 base.chb）")
    parser.add_argument("--out", default=".test.chb", help="输出文件（默认 .test.chb）")
    parser.add_argument("-v", "--verbose", action="store_true", help="输出详细日志")
    return parser


def main(argv=None) -> int:
    args = build_arg_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format="%(levelname)s %(message)s",
    )

    asm = Assembler(
        base_off=BASE_OFFSET,
        str_code=STRING_ENCODING,
        cg_loaded=CG_LOADED,
        bg_list=BG_LIST,
        cha_list=CHA_LIST,
    )

    parse_script(asm, args.script)
    build_script(asm, args.base, args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
