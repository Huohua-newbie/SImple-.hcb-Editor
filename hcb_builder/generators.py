"""各剧本指令的字节码生成器。

以 mixin 形式组织，供 :class:`hcb_builder.assembler.Assembler` 混入使用。
每个 ``gen_*`` 方法都返回 ``bytes``，不直接写入字节流——由解析器负责把
返回值交给 ``Assembler.append``，从而统一维护偏移计数。

生成器会读取汇编器的运行时状态（偏移、选项计数、立绘缓存、CG 已加载表等），
因此所有方法都通过 ``self`` 访问状态，而非全局变量。
"""

from __future__ import annotations

import logging

from .opcodes import (
    OP_NIL,
    OP_U8,
    OP_U16,
    OP_U32,
    call,
    call_hex,
    op_int,
    op_string,
    op_u8,
    op_u16,
    push_int,
    u8,
    u32,
)


class InstructionGenerators:
    """剧本指令 -> HCB 字节码 的生成方法集合（mixin）。

    以下属性与辅助方法由 :class:`hcb_builder.assembler.Assembler` 在
    实例化时注入 / 实现，本类仅声明其存在以便类型检查与阅读。
    """

    # --- 由 Assembler 注入的运行时状态 ---
    str_code: str
    base_off: int
    length_now: int
    select_num: int
    op_num: int
    sel_target: list[str]
    bs_current: list[str]
    bg_list: dict[int, list[str]]
    cha_list: dict[str, list]
    cg_loaded: dict[str, int]
    logger: logging.Logger

    def label_load(self, label: str, offset: int) -> None:  # 由 Assembler 实现
        ...

    def emit_jump(self, kind: str, target_label: str) -> bytes:  # 由 Assembler 实现
        ...

    # ------------------------------------------------------------------ #
    # 选项系统
    # ------------------------------------------------------------------ #
    def gen_selset(self, inputlist: list[str]) -> bytes:
        """生成选项指令块。

        参数形式：:

            ["start", 标题文本]             # 选项开始，渲染标题
            ["op", 选项文本, 目标标签]      # 单个选项项
            ["end"]                         # 选项结束，生成 G[103] 比较分支

        生成逻辑：
        - ``start`` 调用 0x0003836D 渲染选项基底，并注册 ``::selectN`` 标签；
        - ``op`` 调用 0x00057F0D 渲染单个选项，并记录其跳转目标；
        - ``end`` 调用 0x0005800B 结束选项，随后为每个选项生成
          「比较全局变量 G[103] == i，不等则跳到下一判断，相等则跳到目标」的
          if-else 分支链。
        """
        out = bytearray()

        if inputlist[0] == "start":
            str_bytes = op_string(inputlist[1], self.str_code)
            # 记录选项块标签到当前偏移
            self.select_num += 1
            select_label = f"::select{self.select_num}"
            self.label_load(select_label, self.base_off + self.length_now)
            out += str_bytes
            out += OP_NIL * 3  # 其余 3 个入参为 nil
            out += call(0x0003836D)

        elif inputlist[0] == "op":
            str_bytes = op_string(inputlist[1], self.str_code)
            self.op_num += 1
            out += str_bytes
            out += OP_NIL * 2  # 其余 2 个入参为 nil
            out += call(0x00057F0D)
            # 记录该选项的目标标签，供 end 阶段生成跳转
            self.sel_target.append(inputlist[-1])

        elif inputlist[0] == "end":
            now_offset = self.base_off + self.length_now
            out += call(0x0005800B)
            now_offset += 5  # call 指令共 5 字节
            for i in range(1, self.op_num + 1):
                # 记录当前比较分支的偏移
                self.label_load(f"::select{self.select_num}-{i}", now_offset)
                # 比较 G[103] 与 i：0f 67 00 0c <i> 22
                out += b"\x0f\x67\x00\x0c"
                out += u8(i)
                out += b"\x22"
                next_tar = (
                    f"::select{self.select_num}-{i + 1}"
                    if i < self.op_num
                    else f"::select{self.select_num}"
                )
                # 不相等则跳到下一判断
                out += self.emit_jump("jz", next_tar)
                now_offset += 11  # 比较指令 6 字节 + jz 5 字节
                # 相等则跳到目标
                jump_bytes = self.emit_jump("jump", self.sel_target[i - 1])
                out += jump_bytes
                now_offset += len(jump_bytes)
            # 清空选项相关记录
            self.op_num = 0
            self.sel_target = []

        return bytes(out)

    # ------------------------------------------------------------------ #
    # 背景
    # ------------------------------------------------------------------ #
    def gen_bgset(self, inputlist: list[str]) -> bytes:
        """背景设置。

        参数：``[背景编号]`` 或 ``[背景编号, 细分编号]``。背景编号查
        :data:`~hcb_builder.data.BG_LIST` 得到 function 地址。
        """
        bg_id = int(inputlist[0])
        if bg_id not in self.bg_list:
            self.logger.warning("未知背景编号 %s，已忽略该指令", bg_id)
            return b""

        function_offset = self.bg_list[bg_id][-1]
        out = bytearray()

        if len(inputlist) > 1:
            # 第七个入参控制具体细分
            bg_num = int(inputlist[-1])
            out += OP_NIL * 6
            out += op_u8(bg_num)
            out += OP_NIL * 3
            out += call_hex(function_offset)
        else:
            # 第八个入参为 -1
            out += OP_NIL * 7
            out += b"\x0c\x01\x19"  # -1
            out += OP_NIL * 2
            out += call_hex(function_offset)

        out += (
            b"\x0c\x00\x0b\x20\x03\x08\x08\x08\x08\x08\x08\x08\x02\x5a\x11\x04\x00"
        )
        return bytes(out)

    # ------------------------------------------------------------------ #
    # 立绘
    # ------------------------------------------------------------------ #
    def gen_bsset(self, inputlist: list[str]) -> bytes:
        """立绘设置。

        参数（共 10 项）：``[cha, pose, cloth, face, l, 'l/m/r', z, x, y, lyr]``。

        - 前 4 个入参对应角色、姿势、服装、表情；
        - ``l`` 控制构图状态：``0``=L、``1``=U、``2``=S、``-1``=默认，
          ``-10`` 清除当前立绘；
        - ``l/m/r`` 为预设站位（0 右 / 1 中 / 2 左）。
        """
        if len(inputlist) < 10:
            raise ValueError(f"bsset 需要 10 个参数，实际 {len(inputlist)}")

        function_offset = 0x00043F97
        self.bs_current = inputlist[:4]
        out = bytearray()

        # 前 4 个入参：角色 / 姿势 / 服装 / 表情
        for value in inputlist[:4]:
            out += op_u8(int(value))

        # 第 1 个自由入参 l（负数编码为绝对值 + 0x19）
        out += OP_U8
        out += op_int(int(inputlist[4]), 1)

        # 第 2 个自由入参：预设站位
        bslocation = {"l": 2, "m": 1, "r": 0}
        out += op_u8(bslocation[inputlist[5]])

        # 第 3 个自由入参：未知，置 nil
        out += OP_NIL

        # 第 4 个自由入参：z
        out += op_u16(int(inputlist[6]))

        # 第 5、6 个自由入参：x, y（有符号双字节）
        out += OP_U16 + op_int(int(inputlist[7]), 2)
        out += OP_U16 + op_int(int(inputlist[8]), 2)

        # 第 7 个自由入参：不明确，置 nil
        out += OP_NIL

        # 第 8 个自由入参：层次
        out += op_u8(int(inputlist[9]))

        # 第 9、10 个自由入参：透明度 / 第二层 alpha，不设置
        out += OP_NIL * 2

        out += call(function_offset)
        return bytes(out)

    def gen_bsfade(self) -> bytes:
        """立绘淡出。消费 ``bs_current`` 缓存并调用 0x0000BAA9。"""
        if not self.bs_current:
            self.logger.info("当前无立绘，无法消除")
            return b""
        out = bytearray(OP_NIL * 2)
        out += call(0x0000BAA9)
        self.bs_current = []
        return bytes(out)

    # ------------------------------------------------------------------ #
    # 角色说话人
    # ------------------------------------------------------------------ #
    def gen_chaset(self, inputlist: list[str]) -> bytes:
        """角色说话人设置（SPEAK 部分）。

        参数：``[角色名]`` 或 ``[角色名/显示名, 语音编号]``。

        - 首入参为语音编号（4 字节）或 nil；
        - 次入参为显示名：本名 → nil，别名 → 枚举编号，``？？？`` → -1。
        """
        out = bytearray()

        # 第一入参：语音调用
        if len(inputlist) == 2:
            out += OP_U32 + u32(int(inputlist[1]))
        else:
            out += OP_NIL

        cha_realname = inputlist[0].split("/")[0]
        if cha_realname not in self.cha_list:
            self.logger.warning("无预设人名 %s，请手修 hcb", cha_realname)
            return b""

        function_offset = int(self.cha_list[cha_realname][0])

        # 第二入参：使用名义判断
        if "/" in inputlist[0]:
            cha_showname = inputlist[0].split("/")[-1]
            aliases = self.cha_list[cha_realname][-1]
            if cha_showname in aliases:
                out += op_u8(aliases[cha_showname])
            elif cha_showname == "？？？":
                out += b"\x0c\x01\x19"  # -1，隐藏名
            else:
                # 使用了未预设名义，当作使用本名处理
                out += OP_NIL
        else:
            # 本名，第二入参为 nil
            out += OP_NIL

        # 后续入参：大雅 3 个，普通角色 1 个
        out += OP_NIL * (3 if cha_realname == "大雅" else 1)

        out += call(function_offset)
        return bytes(out)

    def gen_chaload(self, inputlist: list[str]) -> bytes:
        """动态生成一个说话人（SPEAK）函数并注册进 ``cha_list``。

        输入：``[真实名, "编号:显示名", ...]``。函数体在当前脚本位置内联生成，
        通过全局变量 G[227] 传入角色编号，按「名义编号」逐项比较后显示对应名字，
        未匹配时兜底显示真实名；最后把函数地址与显示名映射写回 ``cha_list``，
        供 :meth:`gen_chaset` 调用。

        对应原作者的 ``chaload``，须在 [start] 之前使用。
        """
        if not inputlist:
            return b""

        inputname = inputlist[0].strip()
        if inputname in self.cha_list:
            self.logger.info("%s 已加载", inputname)
            return b""

        cha_count = len(self.cha_list)
        function_offset = self.base_off + self.length_now
        now_offset = self.base_off + self.length_now
        dict_cha: dict[str, int] = {}

        out = bytearray()

        # SPEAK 函数固定开头：init_stack(args=3, locals=0)
        out += b"\x01\x03\x00"
        out += push_int(cha_count)
        out += b"\x15\xe3\x00\x0f\xe3\x00"
        out += call(0x0000186E)
        now_offset += 16

        # 显示人名判定块（if-else 链）
        for i in range(len(inputlist) + 1):
            tmp = bytearray()
            if i == 0:
                # 入参 == -1 → 显示 "？？？"
                tmp += b"\x10\xfd\x0c\x01\x19\x22"
                tmp += self.emit_jump("jz", f"speak_cha{cha_count}-{i + 1}")
                tmp += op_string("　 ？？？ 　", self.str_code)
                tmp += b"\x08"
                tmp += call(0x00038124)
                tmp += b"\x0f\xe3\x00\x09"
                tmp += call(0x000821AB)
                tmp += b"\x08"
                tmp += self.emit_jump("jump", "::speak_end")
            elif i < len(inputlist):
                # 入参 == 名义编号 → 显示对应名字
                self.label_load(f"speak_cha{cha_count}-{i}", now_offset)
                tmp += b"\x10\xfd"
                tmp += push_int(int(inputlist[i].split(":")[0]))
                tmp += b"\x22"
                tmp += self.emit_jump("jz", f"speak_cha{cha_count}-{i + 1}")
                showname = str(inputlist[i].split(":")[-1])
                tmp += op_string(showname, self.str_code)
                tmp += b"\x08"
                tmp += call(0x00038124)
                tmp += b"\x0f\xe3\x00\x09"
                tmp += call(0x000821AB)
                tmp += b"\x08"
                tmp += self.emit_jump("jump", "::speak_end")
                dict_cha[showname] = int(inputlist[i].split(":")[0])
            else:
                # 兜底：显示真实名
                self.label_load(f"speak_cha{cha_count}-{i}", now_offset)
                tmp += op_string(str(inputlist[0]), self.str_code)
                tmp += b"\x08"
                tmp += call(0x00038124)
                tmp += b"\x0f\xe3\x00\x09"
                tmp += call(0x000821AB)
                tmp += b"\x08"
            now_offset += len(tmp)
            out += tmp

        # 收尾：保存入参到全局变量并返回
        self.label_load("::speak_end", now_offset)
        out += b"\x0c\x01\x15\x1d\x00\x10\xfc\x15\x25\x01\x10\xfe\x15\x26\x01"
        out += push_int(51)
        out += call(0x0007837B)
        out += b"\x14\x15\x27\x01\x04\x04"

        self.cha_list[inputname] = [function_offset, dict_cha]
        return bytes(out)

    # ------------------------------------------------------------------ #
    # CG
    # ------------------------------------------------------------------ #
    def gen_cgload(self, cgname: str) -> bytes:
        """CG 资源加载代码。

        参数：CG 名（不区分大小写）。若该 CG 已在 ``cg_loaded`` 表中则视为
        已加载，返回空字节。
        """
        realcgname = cgname.upper()
        if realcgname in self.cg_loaded:
            self.logger.info("%s 已加载", cgname)
            return b""

        out = bytearray(b"\x01\x06\x00\x02\xac\x51\x00\x00")
        out += op_string(realcgname, self.str_code)
        out += (
            b"\x10\xf9\x0c\x01\x08\x10\xfa\x10\xfb\x10\xfc\x10\xfd\x08\x08"
            b"\x02\x6a\xc8\x03\x00\x08\x08\x10\xfe\x02\xd3\x51\x00\x00\x04"
        )
        return bytes(out)

    def gen_cgset(self, inputlist: list[str]) -> bytes:
        """CG 设置。

        参数：``[cg名]``（沿用现有设定）或 ``[cg名, x, y, zoom, time]``。
        ``zoom`` 以千分之一为单位，内部换算为 ``3000 - zoom*1000``。
        """
        cgname = inputlist[0].upper()
        if cgname not in self.cg_loaded:
            self.logger.warning("%s 未加载", cgname)
            return b""
        function_offset = self.cg_loaded[cgname]

        out = bytearray()
        if len(inputlist) == 5:
            # 不使用现有设定
            out += b"\x0c\x00"
            out += OP_U16 + op_int(int(inputlist[1]), 2)  # x
            out += OP_U16 + op_int(int(inputlist[2]), 2)  # y
            zoom = 3000 - int(float(inputlist[3]) * 1000)
            out += op_u16(zoom)  # z
            out += OP_NIL  # rotate 不设置
        else:
            # 使用现有设定，xyz 与 rotate 均置 nil
            out += OP_NIL * 5

        out += op_u16(int(inputlist[-1]))  # time
        out += call(function_offset)
        return bytes(out)

    # ------------------------------------------------------------------ #
    # 对话 / 对话框 / BGM / 音效
    # ------------------------------------------------------------------ #
    def gen_diaset(self, text: str) -> bytes:
        """对话内容。字符串 + 4 个 nil 入参 + 调用 0x00038347。"""
        out = bytearray(op_string(text, self.str_code))
        out += OP_NIL * 4
        out += call_hex("00038347")
        return bytes(out)

    def gen_msgset(self, inputtype: str) -> bytes:
        """对话框位置 / 显示控制。

        参数：``middle``（居中）、``normal``（通常并恢复显示）、
        ``boxin``（显示对话框）、``boxout``（隐藏对话框）。
        """
        if inputtype == "middle":
            # (1,-1) 居中
            return b"\x0c\x01\x0c\x01\x19" + call_hex("000349F1")
        if inputtype == "normal":
            # (0,nil) 通常，并强制恢复对话栏显示（0003B797）
            return (
                b"\x0c\x00\x08"
                + call_hex("000349F1")
                + b"\x0c\x00"
                + call_hex("0003B797")
            )
        if inputtype == "boxin":
            # 恢复对话框 (0,nil)
            return b"\x0c\x00\x08" + call_hex("000864F4")
        if inputtype == "boxout":
            # 隐藏对话框 (1,-2)
            return b"\x0c\x01\x0c\x02\x19" + call_hex("000864F4")
        self.logger.warning("未定义对话栏位置或特殊操作: %s", inputtype)
        return b""

    def gen_bgmset(self, bgm_number: str) -> bytes:
        """BGM 设置。参数为 1-255 之间的 BGM 编号。"""
        try:
            bgmnum = int(bgm_number)
        except (TypeError, ValueError) as exc:
            raise ValueError("不合规的入参，预期输入 1-255 之间的整数") from exc
        return op_u8(bgmnum) + OP_NIL * 4 + call_hex("00040552")

    def gen_seset(self, inputlist: list[str]) -> bytes:
        """音效设置。

        参数：``[编号]``（单次播放）、``[编号, loop, 时长]``（循环）或
        ``[编号, end, 时长]``（停止循环）。
        """
        senum = int(inputlist[0])
        out = bytearray(op_u16(senum))

        if len(inputlist) > 1:
            if inputlist[1] == "loop":
                out += b"\x0c\x01\x08\x08"
                out += op_u16(int(inputlist[-1]))
            elif inputlist[1] == "end":
                out += op_u16(int(inputlist[-1]))
                out += b"\x0c\x00\x08\x08"
            else:
                self.logger.warning("与预期输入不符，请检查: %s", inputlist)
                return b""
        else:
            out += OP_NIL * 4

        out += call_hex("0003FC08")
        return bytes(out)
