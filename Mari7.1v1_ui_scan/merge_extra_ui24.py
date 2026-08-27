#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第二十四批：曲线/描边/图集/工具细节类界面词，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX24 = {
    "Curve": "曲线",
    "Curves": "曲线",
    "Curve Editor": "曲线编辑器",
    "Curve Type": "曲线类型",
    "Curve Shape": "曲线形状",
    "Curve Start": "曲线起点",
    "Curve End": "曲线终点",
    "Curve Looping": "曲线循环",
    "Curve Interpolation": "曲线插值",
    "Curve Smooth": "曲线平滑",
    "Curve Linear": "线性曲线",
    "Curve Hold": "保持曲线",
    "Add Point": "添加点",
    "Remove Point": "移除点",
    "Move Point": "移动点",
    "Edit Point": "编辑点",
    "Keyframe": "关键帧",
    "Keyframes": "关键帧",
    "Keyframe Editor": "关键帧编辑器",
    "Add Keyframe": "添加关键帧",
    "Remove Keyframe": "移除关键帧",
    "Timeline": "时间线",
    "Playhead": "播放头",
    "Frame": "帧",
    "Frame Range": "帧范围",
    "Start Frame": "起始帧",
    "End Frame": "结束帧",
    "Playback": "播放",
    "Playback Speed": "播放速度",
    "Ping-Pong": "乒乓",
    "Loop": "循环",
    "Direction": "方向",
    "Stroke": "笔画",
    "Stroke Color": "笔画颜色",
    "Stroke Width": "笔画宽度",
    "Stroke Pressure": "笔画压力",
    "Stroke Length": "笔画长度",
    "Stroke Smoothness": "笔画平滑度",
    "Stroke Blur": "笔画模糊",
    "Stroke Opacity": "笔画不透明度",
    "Steady Stroke": "平稳笔画",
    "Stroke Tilt": "笔画倾斜",
    "Atlas": "图集",
    "Atlas Size": "图集大小",
    "Atlas Resolution": "图集分辨率",
    "Atlas Layout": "图集布局",
    "Generate Atlas": "生成图集",
    "Rebuild Atlas": "重建图集",
    "Padding": "内边距",
    "Margin": "边距",
    "Extraction": "提取",
    "Offset": "偏移",
    "Snapshot": "快照",
    "Snapshot Manager": "快照管理器",
    "Create Snapshot": "创建快照",
    "Restore Snapshot": "还原快照",
    "Compare Snapshot": "比较快照",
    "Layers and Snapshot": "图层与快照",
    "Cache Manager": "缓存管理器",
    "Cache Size": "缓存大小",
    "Cache Path": "缓存路径",
    "Cache Status": "缓存状态",
    "Clear Cache": "清除缓存",
    "Flush Cache": "刷新缓存",
    "Disk Cache": "磁盘缓存",
    "Memory Cache": "内存缓存",
    "Cache Usage": "缓存使用量",
    "Cache Manager Settings": "缓存管理器设置",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX24.items():
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
    if existed:
        print("已存在跳过(部分):", existed[:25])


if __name__ == "__main__":
    main()
