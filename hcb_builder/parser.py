"""剧本解析：把文本 DSL 逐行翻译为字节码。

剧本行格式约定：:

    # 注释行
    [指令,参数...]
    ::标签

每条 ``[指令]`` 行被分发到对应的 ``gen_*`` 生成器，生成字节后追加到
汇编器；``::标签`` 行则把标签注册为当前偏移。
"""

from __future__ import annotations

import logging

from .assembler import Assembler
from .data import ENDER_BYTES, HEADER_BYTES

logger = logging.getLogger("hcb_builder")

# 无需参数的固定字节指令：指令名 -> 字节
RAW_COMMANDS: dict[str, bytes] = {
    "white": (
        b"\x02\x67\x54\x00\x00\x0c\x00\x0b\xe8\x03\x08\x08\x08\x08\x08\x08"
        b"\x08\x02\x5a\x11\x04\x00"
    ),
    "bgmstop": b"\x08\x02\x95\x06\x04\x00",
    "eyecatch": b"\x08\x08\x08\x08\x08\x02\x7b\x6e\x03\x00",
}


def parse_script(asm: Assembler, script_path: str) -> None:
    """解析剧本文件，结果累积到 ``asm`` 中。

    参数:
        asm: :class:`hcb_builder.assembler.Assembler` 实例。
        script_path: 剧本文本文件路径。
    """
    with open(script_path, "r", encoding=asm.str_code) as f:
        for line in f:
            raw = line.rstrip("\n").rstrip("\r")
            if not raw or raw.startswith("#"):
                continue
            if raw.startswith("::"):
                asm.register_current_label(raw.strip())
            elif raw.startswith("["):
                _dispatch(asm, raw)
            else:
                logger.debug("跳过无法识别的行: %r", raw)


def _dispatch(asm: Assembler, line: str) -> None:
    """分发单条 ``[指令,...]`` 行。"""
    if not line.endswith("]"):
        logger.warning("行格式错误（缺少右括号）: %r", line)
        return

    body = line[1:-1]  # 去掉两侧 [ ]
    cmd, sep, rest = body.partition(",")
    cmd = cmd.strip()
    args = [a.strip() for a in rest.split(",")] if rest else []

    if cmd in RAW_COMMANDS:
        asm.append(RAW_COMMANDS[cmd])
    elif cmd == "bg":
        asm.append(asm.gen_bgset(args))
    elif cmd == "dia":
        asm.append(asm.gen_diaset(rest))
    elif cmd == "bgm":
        asm.append(asm.gen_bgmset(rest.strip()))
    elif cmd == "msg":
        asm.append(asm.gen_msgset(rest.strip()))
    elif cmd == "se":
        asm.append(asm.gen_seset(args))
    elif cmd == "cha":
        asm.append(asm.gen_chaset(args))
    elif cmd == "bs":
        asm.append(asm.gen_bsset(args))
    elif cmd == "bsfade":
        asm.append(asm.gen_bsfade())
    elif cmd == "cg":
        asm.append(asm.gen_cgset(args))
    elif cmd == "jump":
        asm.append(asm.emit_jump("jump", args[0] if args else ""))
    elif cmd == "sel":
        _dispatch_sel(asm, rest)
    elif cmd == "cgload":
        _dispatch_cgload(asm, rest.strip())
    elif cmd == "start":
        asm.isstart += 1
        asm.append(HEADER_BYTES)
    elif cmd == "end":
        asm.isend += 1
        asm.append(ENDER_BYTES)
    else:
        logger.warning("未知指令，已忽略: %s", cmd)


def _dispatch_sel(asm: Assembler, rest: str) -> None:
    """分发选项指令。

    支持：``[sel,start,文本]``、``[sel,op,文本,目标]``、``[sel,end]``。
    文本中允许出现逗号（取最后一个逗号之后为目标标签）。
    """
    kind, sep, tail = rest.partition(",")
    kind = kind.strip()

    if kind == "start":
        asm.append(asm.gen_selset(["start", tail.strip()]))
    elif kind == "op":
        text, sep, target = tail.rpartition(",")
        asm.append(asm.gen_selset(["op", text.strip(), target.strip()]))
    elif kind == "end":
        asm.append(asm.gen_selset(["end"]))
    else:
        logger.warning("未知选项子指令: %s", kind)


def _dispatch_cgload(asm: Assembler, cgname: str) -> None:
    """分发 CG 加载指令。要求出现在 [start] 之前（isstart == 0）。"""
    if asm.isstart != 0:
        logger.warning("cgload 必须放在 [start] 之前，已忽略: %s", cgname)
        return

    # 追加前计算 cg 块起始偏移
    cg_offset = asm.base_off + asm.length_now
    result = asm.gen_cgload(cgname)
    asm.append(result)
    asm.cg_loaded[cgname.upper()] = cg_offset
    asm.new_off += len(result)
    logger.info("cgload %s -> 0x%08X", cgname.upper(), cg_offset)
