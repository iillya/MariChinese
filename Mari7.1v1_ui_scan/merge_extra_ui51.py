#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第五十一批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX51 = {
    "Offset": "偏移",
    "Offset X": "X 偏移",
    "Offset Y": "Y 偏移",
    "Offset Z": "Z 偏移",
    "Offset U": "U 偏移",
    "Offset V": "V 偏移",
    "Offset Horizontal": "水平偏移",
    "Offset Vertical": "垂直偏移",
    "Offset Distance": "偏移距离",
    "Offset Amount": "偏移量",
    "Offset Value": "偏移值",
    "Offset Direction": "偏移方向",
    "Offset Scale": "偏移缩放",
    "Offset Rotation": "偏移旋转",
    "Offset Angle": "偏移角度",
    "Offset Radius": "偏移半径",
    "Translation": "平移",
    "Translate": "平移",
    "Translate X": "X 平移",
    "Translate Y": "Y 平移",
    "Translate Z": "Z 平移",
    "Translate Horizontal": "水平平移",
    "Translate Vertical": "垂直平移",
    "Translate Distance": "平移距离",
    "Translate Mode": "平移模式",
    "Rotation": "旋转",
    "Rotate": "旋转",
    "Rotate X": "X 轴旋转",
    "Rotate Y": "Y 轴旋转",
    "Rotate Z": "Z 轴旋转",
    "Rotate Horizontal": "水平旋转",
    "Rotate Vertical": "垂直旋转",
    "Rotate Angle": "旋转角度",
    "Rotate Direction": "旋转方向",
    "Rotate Around": "围绕旋转",
    "Rotate Around Pivot": "围绕枢轴旋转",
    "Rotate Around Center": "围绕中心旋转",
    "Rotate Around Axis": "围绕轴旋转",
    "Rotation Mode": "旋转模式",
    "Scale": "缩放",
    "Scale X": "X 缩放",
    "Scale Y": "Y 缩放",
    "Scale Z": "Z 缩放",
    "Scale Uniform": "等比缩放",
    "Scale Non-Uniform": "非等比缩放",
    "Scale Factor": "缩放系数",
    "Scale Multiply": "乘法缩放",
    "Scale Divide": "除法缩放",
    "Scale Around": "围绕缩放",
    "Scale Around Pivot": "围绕枢轴缩放",
    "Scale Around Center": "围绕中心缩放",
    "Scale Mode": "缩放模式",
    "Reset Transform": "重置变换",
    "Apply Transform": "应用变换",
    "Freeze Transform": "冻结变换",
    "Bake Transform": "烘焙变换",
    "Transform Properties": "变换属性",
    "Transform Settings": "变换设置",
    "Transform Mode": "变换模式",
    "Transform Reference": "变换参考",
    "Transform Pivot": "变换枢轴",
    "Transform Gizmo": "变换控件",
    "Transform Handle": "变换控制柄",
    "Transform Order": "变换顺序",
    "Transform Type": "变换类型",
    "Transform Time": "变换时间",
    "Transform Amount": "变换量",
    "Transform Delta": "变换增量",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX51.items():
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
