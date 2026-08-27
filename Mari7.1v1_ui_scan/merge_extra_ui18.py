#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第十八批：通道/图层/几何/着色器类界面词，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX18 = {
    "Channel Stack": "通道堆栈",
    "Layer Stack": "图层堆栈",
    "Mask Stack": "蒙版堆栈",
    "Channel List": "通道列表",
    "Layer List": "图层列表",
    "Shader Stack": "着色器堆栈",
    "Paint Layers": "绘制图层",
    "Adjustment Layers": "调整图层",
    "Material Layers": "材质图层",
    "Projection": "投影",
    "Projections": "投影",
    "Projection Stack": "投影堆栈",
    "Projection List": "投影列表",
    "Projection Settings": "投影设置",
    "Projection Ratio": "投影比例",
    "Projection Scale": "投影缩放",
    "Projection Strength": "投影强度",
    "Projection Blur": "投影模糊",
    "Projection Type": "投影类型",
    "Projection Mode": "投影模式",
    "Projection Direction": "投影方向",
    "Projection Offset": "投影偏移",
    "Projection Rotation": "投影旋转",
    "Projection Reverse": "投影反转",
    "Projection Front": "投影正面",
    "Projection Back": "投影背面",
    "Projection Both": "投影两面",
    "Projection Through": "投穿透",
    "Projection Mirror": "投影镜像",
    "Projector List": "投影器列表",
    "Projector Settings": "投影器设置",
    "Projector View": "投影器视图",
    "Add Projector": "添加投影器",
    "Remove Projector": "移除投影器",
    "Make Projector Current": "将投影器设为当前",
    "Projector Mode": "投影器模式",
    "Projector Orientation": "投影器方向",
    "Projector Distance": "投影器距离",
    "Projector Angle": "投影器角度",
    "Projector Scale": "投影器缩放",
    "Object Projection": "对象投影",
    "Camera Projection": "相机投影",
    "Planar Projection": "平面投影",
    "Cylindrical Projection": "圆柱投影",
    "Spherical Projection": "球面投影",
    "Triplanar Projection": "三面投影",
    "UV Projection": "UV 投影",
    "Camera Projection Settings": "相机投影设置",
    "Projection Normal": "投影法线",
    "Projection Along X": "沿 X 轴投影",
    "Projection Along Y": "沿 Y 轴投影",
    "Projection Along Z": "沿 Z 轴投影",
    "Projection Axis": "投影轴",
    "Projection Bounds": "投影范围",
    "Projection Extents": "投影范围",
    "Projection Falloff": "投影衰减",
    "Projection Softness": "投影柔和度",
    "Projection Opacity": "投影不透明度",
    "Projection Density": "投影密度",
    "Projection Filter": "投影滤镜",
    "Projection Blur Radius": "投影模糊半径",
    "Projection Blur Angle": "投影模糊角度",
    "Projection Blur Offset": "投影模糊偏移",
    "Projection Wrap": "投影循环",
    "Projection Clamp": "投影钳制",
    "Projection Mirror X": "沿 X 轴镜像投影",
    "Projection Mirror Y": "沿 Y 轴镜像投影",
    "Projection Mirror Z": "沿 Z 轴镜像投影",
    "Projection Color Space": "投影颜色空间",
    "Projection Depth": "投影深度",
    "Projection Order": "投影顺序",
    "Projection on Mesh": "在网格上投影",
    "Projection to Mesh": "投影到网格",
    "Projection to Channel": "投影到通道",
    "Projection to Paint Buffer": "投影到绘制缓冲区",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX18.items():
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
