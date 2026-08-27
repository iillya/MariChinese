#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第三十一批：几何/绘制/烘焙操作补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX31 = {
    "Quadrangulate": "四边形化",
    "Triangulate": "三角化",
    "Retopologize": "重新拓扑",
    "Decimate": "减面",
    "Subdivide": "细分",
    "Subdivide Selected": "细分所选",
    "Unsubdivide": "取消细分",
    "Extrude": "挤出",
    "Bevel": "倒角",
    "Inset": "内插",
    "Bridge": "桥接",
    "Merge Vertices": "合并顶点",
    "Weld": "焊接",
    "Split": "拆分",
    "Separate": "分离",
    "Join": "合并",
    "Combine": "组合",
    "Boolean": "布尔",
    "Boolean Union": "布尔并集",
    "Boolean Subtract": "布尔差集",
    "Boolean Intersect": "布尔交集",
    "Smooth": "平滑",
    "Smooth Selected": "平滑所选",
    "Flat": "平直",
    "Flat Shade": "平直着色",
    "Smooth Shade": "平滑着色",
    "Recalculate Normals": "重新计算法线",
    "Flip Normals": "翻转法线",
    "Invert Normals": "反转法线",
    "Normals": "法线",
    "Tangent": "切线",
    "Tangents": "切线",
    "Rebuild Tangents": "重建切线",
    "Unwrap": "展开",
    "Unwrap UVs": "展开 UV",
    "Project UVs": "投影 UV",
    "Planar UV": "平面 UV",
    "Cylindrical UV": "圆柱 UV",
    "Spherical UV": "球面 UV",
    "Box UV": "盒式 UV",
    "Tri-planar UV": "三面 UV",
    "Pack UVs": "打包 UV",
    "Layout UVs": "布局 UV",
    "Optimize UVs": "优化 UV",
    "Scale UVs": "缩放 UV",
    "Rotate UVs": "旋转 UV",
    "Flip UVs": "翻转 UV",
    "Mirror UVs": "镜像 UV",
    "Fill": "填充",
    "Fill Selection": "填充所选",
    "Fill Layer": "填充图层",
    "Fill Channel": "填充通道",
    "Fill Color": "填充颜色",
    "Fill Foreground": "填充前景",
    "Fill Background": "填充背景",
    "Fill Selection Color": "用颜色填充所选",
    "Fill with Foreground": "以前景色填充",
    "Fill with Background": "以背景色填充",
    "Paint Selection": "绘制所选",
    "Paint Layer": "绘制图层",
    "Paint Channel": "绘制通道",
    "Paint on All Layers": "在所有图层上绘制",
    "Paint on Current Layer": "在当前图层上绘制",
    "Paint on Layer Mask": "在图层蒙版上绘制",
    "Paint on Channel": "在通道上绘制",
    "Bake Selected": "烘焙所选",
    "Bake Channel": "烘焙通道",
    "Bake Layer": "烘焙图层",
    "Bake All": "全部烘焙",
    "Bake Point": "烘焙点",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX31.items():
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
