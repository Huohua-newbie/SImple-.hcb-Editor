"""原版 ``base.chb`` 模板资源（内置）。

模板以二进制文件形式随包分发，通过 :func:`load_base_chb` 读取，
不再需要从命令行传入路径。
"""

from __future__ import annotations

from pathlib import Path

#: 内置模板文件的路径（与模块同目录）
BASE_CHB_PATH: Path = Path(__file__).with_name("base.chb")


def load_base_chb() -> bytes:
    """读取内置的原版 ``base.chb`` 模板字节。"""
    return BASE_CHB_PATH.read_bytes()
