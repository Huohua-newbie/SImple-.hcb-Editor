"""HCB 字节码的低层编码原语。

本模块只负责「值 → 字节」的编码，不涉及任何指令语义或状态管理。
编码约定全部来自对原版 ``base.chb`` 的反向分析：

===========  ======  ==================================================
操作码        字节    含义
===========  ======  ==================================================
OP_STRING    0x0e    字符串操作数：1 字节长度 + 字节 + NUL（长度 = 字节数 + 1）
OP_CALL      0x02    调用引擎内部函数：后跟 4 字节小端函数地址
OP_U8        0x0c    单字节无符号整数操作数
OP_U16       0x0b    双字节小端整数操作数
OP_U32       0x0a    四字节小端整数操作数
OP_NIL       0x08    空值操作数（nil）
OP_NEG       0x19    取负后缀（追加在数值字节之后，表示该数值为负）
OP_JMP       0x06    无条件跳转：后跟 4 字节目标地址
OP_JZ        0x07    条件跳转（jz）：后跟 4 字节目标地址
===========  ======  ==================================================

负数编码规则：负数的绝对值按对应宽度编码后，再追加一个 ``0x19`` 字节，
例如 ``-1``（单字节）→ ``0x01 0x19``。
"""

from __future__ import annotations

OP_STRING = b"\x0e"
OP_CALL = b"\x02"
OP_U8 = b"\x0c"
OP_U16 = b"\x0b"
OP_U32 = b"\x0a"
OP_NIL = b"\x08"
OP_NEG = b"\x19"
OP_JMP = b"\x06"
OP_JZ = b"\x07"


def u8(value: int) -> bytes:
    """单字节小端整数（无操作码前缀）。"""
    return int(value).to_bytes(1, "little")


def u16(value: int) -> bytes:
    """双字节小端整数（无操作码前缀）。"""
    return int(value).to_bytes(2, "little")


def u32(value: int) -> bytes:
    """四字节小端整数（无操作码前缀）。"""
    return int(value).to_bytes(4, "little")


def op_u8(value: int) -> bytes:
    """``0x0c`` + 单字节整数操作数。"""
    return OP_U8 + u8(value)


def op_u16(value: int) -> bytes:
    """``0x0b`` + 双字节整数操作数。"""
    return OP_U16 + u16(value)


def op_u32(value: int) -> bytes:
    """``0x0a`` + 四字节整数操作数。"""
    return OP_U32 + u32(value)


def op_nil() -> bytes:
    """``0x08`` 空值操作数。"""
    return OP_NIL


def op_int(value: int, width: int = 1) -> bytes:
    """编码有符号整数（不带操作码前缀，供调用方自行组合前缀）。

    与原版行为一致：正数直接按宽度编码；负数编码为绝对值 + ``0x19`` 后缀。
    """
    if value >= 0:
        return int(value).to_bytes(width, "little")
    return abs(int(value)).to_bytes(width, "little") + OP_NEG


def op_string(value: str, encoding: str = "gbk") -> bytes:
    """编码字符串操作数：``0x0e`` + 长度字节 + 字节 + NUL。

    长度字段 = 字节数 + 1（含结尾 NUL）。编码失败时抛出
    :class:`ValueError`，提示含不支持的字符。
    """
    try:
        data = value.encode(encoding)
    except UnicodeEncodeError as exc:
        raise ValueError(f"在“{value}”中含有 {encoding} 不支持的字符") from exc
    return OP_STRING + bytes([len(data) + 1]) + data + b"\x00"


def call(function_offset: int) -> bytes:
    """函数调用指令：``0x02`` + 4 字节小端函数地址。"""
    return OP_CALL + u32(function_offset)


def call_hex(function_offset_hex: str) -> bytes:
    """函数调用指令，地址以十六进制字符串给出（自动转小端）。

    例如 ``call_hex("000349F1")`` → ``b"\\x02\\xf1\\x49\\x03\\x00"``。
    """
    return OP_CALL + bytes.fromhex(function_offset_hex.strip())[::-1]


def jump(target: bytes) -> bytes:
    """无条件跳转指令：``0x06`` + 目标占位/地址字节。"""
    return OP_JMP + target


def jz(target: bytes) -> bytes:
    """条件跳转指令：``0x07`` + 目标占位/地址字节。"""
    return OP_JZ + target
