#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第五十八批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX58 = {
    "Show": "显示",
    "Hide": "隐藏",
    "Display": "显示",
    "View": "视图",
    "Preview": "预览",
    "Overview": "概览",
    "Look": "外观",
    "Style": "样式",
    "Layout": "布局",
    "Arrange": "排列",
    "Place": "放置",
    "Align": "对齐",
    "Distribute": "分布",
    "Center": "居中",
    "Stack": "堆叠",
    "Overlap": "重叠",
    "Inset": "内缩",
    "Outset": "外扩",
    "Spread": "展开",
    "Gap": "间距",
    "Margin": "边距",
    "Padding": "内边距",
    "Spacer": "间隔",
    "Separator": "分隔符",
    "Divider": "分隔线",
    "Border": "边框",
    "Outline": "轮廓",
    "Frame": "边框",
    "Edge": "边缘",
    "Corner": "角",
    "Radius": "圆角",
    "Roundness": "圆度",
    "Smoothness": "平滑度",
    "Curved": "弯曲",
    "Straight": "直线",
    "Thickness": "粗细",
    "Weight": "粗细",
    "Width": "宽度",
    "Height": "高度",
    "Depth": "深度",
    "Thickness": "粗细",
    "Fill": "填充",
    "Stroke": "描边",
    "Line": "线条",
    "Line Style": "线条样式",
    "Line Width": "线条宽度",
    "Line Color": "线条颜色",
    "Line End": "线条端点",
    "Line Join": "线条连接",
    "Cap": "端点",
    "Cap Style": "端点样式",
    "Joint": "连接",
    "Joint Style": "连接样式",
    "Arrow": "箭头",
    "Arrow Head": "箭头",
    "Arrow Tail": "箭尾",
    "Dash": "虚线",
    "Dotted": "点线",
    "Solid": "实线",
    "Dashed": "虚线",
    "Dot": "点",
    "Grid": "网格",
    "Grid Spacing": "网格间距",
    "Grid Size": "网格大小",
    "Grid Line": "网格线",
    "Grid Color": "网格颜色",
    "Grid Opacity": "网格不透明度",
    "Show Grid": "显示网格",
    "Hide Grid": "隐藏网格",
    "Snap to Grid": "吸附到网格",
    "Grid Snap": "网格吸附",
    "Grid Type": "网格类型",
    "Grid Mode": "网格模式",
    "Grid Origin": "网格原点",
    "Grid Extent": "网格范围",
    "Grid Subdiv": "网格细分",
    "Grid Visibility": "网格可见性",
    "Grid Lock": "网格锁定",
    "Lock Grid": "锁定网格",
    "Unlock Grid": "解锁网格",
    "Clear Grid": "清除网格",
    "Reset Grid": "重置网格",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX58.items():
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
