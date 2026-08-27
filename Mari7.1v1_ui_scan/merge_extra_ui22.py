#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第二十二批：色彩管理/视图/选择类界面词，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX22 = {
    "Color Management": "色彩管理",
    "Color Management Settings": "色彩管理设置",
    "Color Settings": "颜色设置",
    "Color Profile": "颜色配置文件",
    "Color Space": "颜色空间",
    "Color Spaces": "颜色空间",
    "Working Color Space": "工作颜色空间",
    "Display Color Space": "显示颜色空间",
    "Input Color Space": "输入颜色空间",
    "Output Color Space": "输出颜色空间",
    "Data Color Space": "数据颜色空间",
    "Source Color": "源颜色",
    "Target Color": "目标颜色",
    "Color Transform": "颜色变换",
    "Color Correction": "色彩校正",
    "Color Grading": "调色",
    "Color Balance": "色彩平衡",
    "Color Wheels": "颜色轮盘",
    "Color Picker": "颜色选择器",
    "Color Sampler": "颜色采样器",
    "Color Monitor": "颜色显示器",
    "Color Histogram": "颜色直方图",
    "Color Swatches": "颜色色板",
    "Pick Color": "拾取颜色",
    "Copy Color": "复制颜色",
    "Paste Color": "粘贴颜色",
    "Reset Color": "重置颜色",
    "Default Color": "默认颜色",
    "Foreground Color": "前景颜色",
    "Background Color": "背景颜色",
    "Wireframe Color": "线框颜色",
    "Background": "背景",
    "View Settings": "视图设置",
    "View Properties": "视图属性",
    "View Mode": "视图模式",
    "View Options": "视图选项",
    "Show Grid": "显示网格",
    "Hide Grid": "隐藏网格",
    "Show Guides": "显示参考线",
    "Hide Guides": "隐藏参考线",
    "Show Rulers": "显示标尺",
    "Hide Rulers": "隐藏标尺",
    "Show Axes": "显示坐标轴",
    "Hide Axes": "隐藏坐标轴",
    "Show Frame": "显示边框",
    "Hide Frame": "隐藏边框",
    "Show Selection": "显示选择",
    "Hide Selection": "隐藏选择",
    "Show Marquee": "显示选框",
    "Hide Marquee": "隐藏选框",
    "Selection Color": "选择颜色",
    "Selection Outline": "选择轮廓",
    "Selection Mode": "选择模式",
    "Selection Box": "选择框",
    "Selection Radius": "选择半径",
    "Selection Brush": "选择笔刷",
    "Select All Faces": "选择所有面",
    "Select All Patches": "选择所有面片",
    "Select All Objects": "选择所有对象",
    "Select Visible": "选择可见",
    "Select Hidden": "选择隐藏",
    "Select Invert": "反转选择",
    "Select None": "全不选",
    "Select Similar": "选择相似",
    "Select by Color": "按颜色选择",
    "Select by Tag": "按标签选择",
    "Select by Layer": "按图层选择",
    "Select Group": "选择组",
    "Grow Selection": "扩展选择",
    "Shrink Selection": "收缩选择",
    "Invert Selection": "反转选择",
    "Feather Selection": "羽化选择",
    "Add to Selection": "添加到选择",
    "Subtract from Selection": "从选择中减去",
    "Intersect Selection": "选择交集",
    "Selection Group": "选择组",
    "Selection Set": "选择集",
    "Create Selection": "创建选择",
    "Save Selection": "保存选择",
    "Load Selection": "加载选择",
    "Delete Selection": "删除选择",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX22.items():
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
        print("已存在跳过(部分):", existed[:20])


if __name__ == "__main__":
    main()
