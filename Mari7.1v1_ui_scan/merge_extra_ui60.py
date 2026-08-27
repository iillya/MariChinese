#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第六十批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX60 = {
    "Selection": "选择",
    "Select": "选择",
    "Deselect": "取消选择",
    "Selected": "已选择",
    "Unselected": "未选择",
    "Selection Set": "选择集",
    "Selection Group": "选择组",
    "Selection Mask": "选择蒙版",
    "Selection Color": "选择颜色",
    "Selection Opacity": "选择不透明度",
    "Selection Preview": "选择预览",
    "Selection Mode": "选择模式",
    "Selection Type": "选择类型",
    "Selection Source": "选择来源",
    "Selection Target": "选择目标",
    "Selection Range": "选择范围",
    "Selection Area": "选择区域",
    "Selection Region": "选择区域",
    "Selection Bounds": "选择范围",
    "Selection Extent": "选择范围",
    "Selection Level": "选择级别",
    "Selection Filter": "选择滤镜",
    "Selection Lock": "选择锁定",
    "Selection Hide": "选择隐藏",
    "Selection Show": "选择显示",
    "Selection Border": "选择边框",
    "Selection Outline": "选择轮廓",
    "Selection Pivot": "选择枢轴",
    "Selection Handle": "选择控制柄",
    "Selection Gizmo": "选择控件",
    "Selection Tool": "选择工具",
    "Selection Brush": "选择笔刷",
    "Selection Marquee": "选择选框",
    "Selection Box": "选择框",
    "Selection Lasso": "选择套索",
    "Selection Wand": "选择魔棒",
    "Selection Radius": "选择半径",
    "Selection Threshold": "选择阈值",
    "Selection Tolerance": "选择容差",
    "Selection Grow": "扩展选择",
    "Selection Shrink": "收缩选择",
    "Selection Expand": "扩展选择",
    "Selection Contract": "收缩选择",
    "Selection Feather": "羽化选择",
    "Selection Invert": "反转选择",
    "Selection Add": "添加选择",
    "Selection Subtract": "减去选择",
    "Selection Intersect": "选择交集",
    "Selection Xor": "选择异或",
    "Selection Union": "选择并集",
    "Selection Difference": "选择差集",
    "Selection Copy": "复制选择",
    "Selection Paste": "粘贴选择",
    "Selection Delete": "删除选择",
    "Selection Name": "选择名称",
    "Selection ID": "选择 ID",
    "Selection Label": "选择标签",
    "Selection Note": "选择备注",
    "Selection Color Picker": "选择颜色选择器",
    "Selection Preview View": "选择预览视图",
    "Selection Viewport": "选择视口",
    "Selection Highlight": "选择高亮",
    "Selection Overlay": "选择覆盖层",
    "Selection Visibility": "选择可见性",
    "Selection Enabled": "选择已启用",
    "Selection Disabled": "选择已禁用",
    "Selection Locked": "选择已锁定",
    "Selection Hidden": "选择已隐藏",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX60.items():
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
