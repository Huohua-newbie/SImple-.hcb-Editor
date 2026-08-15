"""
示例剧本 case0（Python DSL 版）。

与 ``examples/case0.txt`` 语义完全一致，使用 :class:`cli.HCBScript` 与
常用参数常量撰写。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from cli import *


class Case0(HCBScript):
    """复刻 case0.txt 的示例剧本。"""

    def constructor(self) -> None:
        self.cgload("chiwa_fd01a") \
            .start() \
            .bg(67) \
            .dia("显示背景") \
            .bgm(3) \
            .dia("播放BGM") \
            .bgmstop() \
            .dia("暂停BGM") \
            .se(209) \
            .dia("音效，钟声，单次播放") \
            .se(168, SE_LOOP, 1000) \
            .dia("音效，熟悉的歌曲") \
            .se(168, SE_END, 3000) \
            .dia("停止播放") \
            .eyecatch() \
            .msg(MSG_BOXOUT) \
            .cg("chiwa_fd01a", 0, 0, 1, 900) \
            .cha("千和") \
            .dia("等[·|那][·|个][·|人]回来后，我们四个人一起来考虑这个孩子的名字就太好了……可以吗？") \
            .bg(67, 1) \
            .bs(3, 1, 1, 17, LAYOUT_DEFAULT, LOC_MIDDLE, 900, 0, 50, 1) \
            .cha("大雅") \
            .msg(MSG_BOXIN) \
            .dia("……这个，是什么恶作剧……吗？") \
            .eyecatch() \
            .msg(MSG_MIDDLE) \
            .bg(106) \
            .bgm(44) \
            .dia("世界于此，暂作叹息……") \
            .cg("mashiro_e011a", 0, 0, 1, 900) \
            .msg(MSG_NORMAL) \
            .msg(MSG_BOXOUT) \
            .cha("真白/？？？", 5000010) \
            .dia("心地善良的人，总是不自觉地成为受难者") \
            .eyecatch() \
            .msg(MSG_BOXIN) \
            .label("loop") \
            .bg(67, 1) \
            .bgm(3) \
            .bs(1, 1, 6, 16, LAYOUT_DEFAULT, LOC_LEFT, 1000, -200, 100, 1) \
            .bs(2, 1, 2, 34, LAYOUT_DEFAULT, LOC_RIGHT, 1000, 200, 100, 2) \
            .sel_start("或者，对一个人，见死不救吧") \
            .sel_op("放弃小黑", "target1") \
            .sel_op("放弃小春", "target2") \
            .sel_op("这不对吧，我玩的不是水葬啊？", "final") \
            .sel_end() \
            .label("target1") \
            .bg(67) \
            .bs(2, 1, 2, 4, LAYOUT_DEFAULT, LOC_MIDDLE, 1000, 0, 100, 2) \
            .dia("你抛弃了小猫") \
            .dia("有哪里不对，再想想") \
            .jump("loop") \
            .label("target2") \
            .bg(67) \
            .bs(1, 1, 6, 4, LAYOUT_DEFAULT, LOC_MIDDLE, 1000, 0, 100, 1) \
            .dia("小春又死了，太没人性了") \
            .dia("有哪里不对，再想想") \
            .jump("loop") \
            .label("final") \
            .dia("对的，实际上这个场景不会发生") \
            .eyecatch() \
            .bg(112) \
            .msg(MSG_MIDDLE) \
            .dia("总之测试到此结束，感谢各位") \
            .end()


if __name__ == "__main__":
    Case0().build("case0.chb")
    print("已生成 case0.chb")
