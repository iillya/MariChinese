#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第四十六批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX46 = {
    "Frame": "帧",
    "Frames": "帧",
    "Image Frame": "图像帧",
    "Frame Rate": "帧率",
    "Time Code": "时间码",
    "Play": "播放",
    "Pause": "暂停",
    "Stop": "停止",
    "Record": "录制",
    "Rewind": "倒放",
    "Forward": "前进",
    "Backward": "后退",
    "Loop": "循环",
    "Play Once": "播放一次",
    "Play Loop": "循环播放",
    "Play Reverse": "反向播放",
    "Shuttle": "往复",
    "Scrub": "拖动",
    "Scrub Timeline": "拖动时间线",
    "Timeline": "时间线",
    "Frame Step": "帧步长",
    "Step Forward": "单步前进",
    "Step Backward": "单步后退",
    "Skip Forward": "快进",
    "Skip Backward": "快退",
    "Go to Beginning": "转到开头",
    "Go to End": "转到结尾",
    "Go to Previous Frame": "转到上一帧",
    "Go to Next Frame": "转到下一帧",
    "Previous": "上一个",
    "Next": "下一个",
    "First": "第一个",
    "Last": "最后一个",
    "Begin": "开始",
    "Finish": "完成",
    "Complete": "完成",
    "Start Over": "重新开始",
    "Restart": "重启",
    "Resume": "继续",
    "Skip": "跳过",
    "Advance": "前进",
    "Rewind to Start": "倒回到开头",
    "Fast Forward to End": "快进到结尾",
    "Load Frame": "加载帧",
    "Save Frame": "保存帧",
    "Import Frame": "导入帧",
    "Export Frame": "导出帧",
    "Insert Frame": "插入帧",
    "Delete Frame": "删除帧",
    "Duplicate Frame": "复制帧",
    "Rename Frame": "重命名帧",
    "Frame Properties": "帧属性",
    "Frame Settings": "帧设置",
    "Frame Options": "帧选项",
    "Frame Preview": "帧预览",
    "Frame Info": "帧信息",
    "Frame Counter": "帧计数器",
    "Frame Total": "帧总计",
    "Frames Remaining": "剩余帧数",
    "Frames Done": "已完成帧数",
    "Frames Rendered": "已渲染帧数",
    "Frames Skipped": "已跳过帧数",
    "Frames Failed": "失败帧数",
    "Frames Dropped": "丢弃帧数",
    "Frame Progress": "帧进度",
    "Frame Slider": "帧滑块",
    "Frame Field": "帧字段",
    "Frame Label": "帧标签",
    "Frame Size": "帧大小",
    "Frame Width": "帧宽度",
    "Frame Height": "帧高度",
    "Frame Range": "帧范围",
    "Frame Start": "帧起点",
    "Frame End": "帧终点",
    "Frame Step": "帧步长",
    "Frame Offset": "帧偏移",
    "Frame Padding": "帧内边距",
    "Frame Sequence": "帧序列",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX46.items():
        if k in trans:
            existed.append(k)
        else:
            trans[k] = v
            added.append(k)
    doc["translations"] = trans
    with open(DICT, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("added:", len(added))
    print("already existed (skip):", len(existed))
    print("total now:", len(trans))


if __name__ == "__main__":
    main()
