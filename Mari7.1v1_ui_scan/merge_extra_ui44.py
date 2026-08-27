#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第四十四批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX44 = {
    "Face": "面",
    "Faces": "面",
    "Vertex": "顶点",
    "Vertices": "顶点",
    "Edge": "边",
    "Edges": "边",
    "Polygon": "多边形",
    "Polygons": "多边形",
    "Patch": "面片",
    "Patches": "面片",
    "Patch Selection": "面片选择",
    "Face Selection": "面选择",
    "Object Selection": "对象选择",
    "Selection Mode": "选择模式",
    "Select Patches": "选择面片",
    "Select Faces": "选择面",
    "Select Objects": "选择对象",
    "Deselect Patches": "取消选择面片",
    "Deselect Faces": "取消选择面",
    "Deselect Objects": "取消选择对象",
    "Toggle Selection": "切换选择",
    "Toggle Patches": "切换面片",
    "Toggle Faces": "切换面",
    "Toggle Objects": "切换对象",
    "Add to Patch Selection": "添加到面片选择",
    "Add to Face Selection": "添加到面选择",
    "Add to Object Selection": "添加到对象选择",
    "Remove from Patch Selection": "从面片选择中移除",
    "Remove from Face Selection": "从面选择中移除",
    "Remove from Object Selection": "从对象选择中移除",
    "Invert Patch Selection": "反转面片选择",
    "Invert Face Selection": "反转面选择",
    "Invert Object Selection": "反转对象选择",
    "Grow Patch Selection": "扩展面片选择",
    "Grow Face Selection": "扩展面选择",
    "Shrink Patch Selection": "收缩面片选择",
    "Shrink Face Selection": "收缩面选择",
    "Select All Patches": "选择所有面片",
    "Select All Faces": "选择所有面",
    "Select All Objects": "选择所有对象",
    "Select Visible Patches": "选择可见面片",
    "Select Visible Faces": "选择可见面",
    "Select Visible Objects": "选择可见对象",
    "Select Hidden Patches": "选择隐藏面片",
    "Select Hidden Faces": "选择隐藏面",
    "Select Hidden Objects": "选择隐藏对象",
    "Select Border": "选择边界",
    "Select Loop": "选择循环",
    "Select Ring": "选择环",
    "Select Similar Faces": "选择相似面",
    "Select Similar Patches": "选择相似面片",
    "Select by UV": "按 UV 选择",
    "Select by Area": "按面积选择",
    "Select by Material": "按材质选择",
    "Selection Filter": "选择滤镜",
    "Filter Selection": "过滤选择",
    "Clear Selection": "清除选择",
    "Lock Selection": "锁定选择",
    "Unlock Selection": "解锁选择",
    "Hide Selection": "隐藏选择",
    "Show Selection": "显示选择",
    "Delete Selection": "删除选择",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX44.items():
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
