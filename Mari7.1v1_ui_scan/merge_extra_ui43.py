#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第四十三批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX43 = {
    "Time": "时间",
    "Date": "日期",
    "Date Time": "日期时间",
    "Timestamp": "时间戳",
    "Duration": "时长",
    "Elapsed Time": "已用时间",
    "Remaining Time": "剩余时间",
    "Start Time": "开始时间",
    "End Time": "结束时间",
    "Current Time": "当前时间",
    "Total Time": "总时间",
    "Time Frame": "时间范围",
    "Time Range": "时间范围",
    "Time Code": "时间码",
    "Time Unit": "时间单位",
    "Frames": "帧",
    "Frames Per Second": "帧每秒",
    "Frame Rate": "帧率",
    "Frame Index": "帧索引",
    "Frame Number": "帧号",
    "Frame Count": "帧数",
    "Frame Start": "起始帧",
    "Frame End": "结束帧",
    "Frame Offset": "帧偏移",
    "Frame Step": "帧步长",
    "Frame Time": "帧时间",
    "Frame Interval": "帧间隔",
    "Frame Range": "帧范围",
    "Frame Duration": "帧时长",
    "Start Frame": "起始帧",
    "End Frame": "结束帧",
    "Animation": "动画",
    "Animation Settings": "动画设置",
    "Animation Range": "动画范围",
    "Animation Length": "动画长度",
    "Animation Loop": "动画循环",
    "Animation Playback": "动画播放",
    "Play Animation": "播放动画",
    "Stop Animation": "停止动画",
    "Pause Animation": "暂停动画",
    "Loop Animation": "循环动画",
    "Play Once": "播放一次",
    "Play Loop": "循环播放",
    "Playback Loop": "播放循环",
    "Playback Range": "播放范围",
    "Playback Rate": "播放速率",
    "Playback Speed": "播放速度",
    "Playback Direction": "播放方向",
    "Playback Mode": "播放模式",
    "Playback Controls": "播放控制",
    "Timeline": "时间线",
    "Timeline Zoom": "时间线缩放",
    "Timeline Scrub": "时间线拖动",
    "Set Time": "设置时间",
    "Go to Start": "转到开头",
    "Go to End": "转到结尾",
    "Go to Frame": "转到帧",
    "Go to Previous": "转到上一个",
    "Go to Next": "转到下一个",
    "Skip Forward": "前进",
    "Skip Backward": "后退",
    "Step Forward": "单步前进",
    "Step Backward": "单步后退",
    "Next Frame": "下一帧",
    "Previous Frame": "上一帧",
    "First Frame": "第一帧",
    "Last Frame": "最后一帧",
    "Current Frame": "当前帧",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX43.items():
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
