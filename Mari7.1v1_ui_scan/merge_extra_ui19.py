#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第十九批：几何/对象/UV/图像类界面词，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX19 = {
    "Geometry": "几何体",
    "Geometry List": "几何体列表",
    "Object List": "对象列表",
    "Object Properties": "对象属性",
    "Geometry Properties": "几何体属性",
    "Object Mode": "对象模式",
    "Patch Mode": "面片模式",
    "Face Mode": "面模式",
    "Subdivision": "细分",
    "Subdivision Level": "细分级别",
    "Mesh": "网格",
    "Mesh Properties": "网格属性",
    "Quad": "四边形",
    "Quad Faces": "四边形面",
    "Triangle": "三角形",
    "Triangle Faces": "三角形面",
    "Topology": "拓扑",
    "Vertex": "顶点",
    "Vertices": "顶点",
    "Edge": "边",
    "Edges": "边",
    "Face": "面",
    "Faces": "面",
    "UV": "UV",
    "UVs": "UV",
    "UV Map": "UV 贴图",
    "UV Set": "UV 集",
    "UV Layer": "UV 图层",
    "UV Channel": "UV 通道",
    "UV Space": "UV 空间",
    "UV Transform": "UV 变换",
    "UV Scale": "UV 缩放",
    "UV Offset": "UV 偏移",
    "UV Rotation": "UV 旋转",
    "UV Flip": "UV 翻转",
    "UV Mirror": "UV 镜像",
    "UV Wrap": "UV 循环",
    "UV Clamp": "UV 钳制",
    "UV Tile": "UV 瓦片",
    "UV Islands": "UV 岛",
    "UV Layout": "UV 布局",
    "UV Editor": "UV 编辑器",
    "UV Unwrap": "UV 展开",
    "UV Pack": "UV 打包",
    "UV Snap": "UV 吸附",
    "UV Align": "UV 对齐",
    "UV Grid": "UV 网格",
    "Image Set": "图像集",
    "Image Sets": "图像集",
    "Image Sequence": "图像序列",
    "Image Stack": "图像堆栈",
    "Image Properties": "图像属性",
    "Image Format": "图像格式",
    "Image Resolution": "图像分辨率",
    "Image Size": "图像大小",
    "Image Width": "图像宽度",
    "Image Height": "图像高度",
    "Image Depth": "图像深度",
    "Image Path": "图像路径",
    "Image Name": "图像名称",
    "Image Type": "图像类型",
    "Tile": "瓦片",
    "Tiles": "瓦片",
    "Tile Size": "瓦片大小",
    "Mipmap": "Mipmap",
    "Mipmaps": "Mipmap",
    "Proxy": "代理",
    "Proxy Level": "代理级别",
    "Resolution Mode": "分辨率模式",
    "Base Resolution": "基础分辨率",
    "Max Resolution": "最大分辨率",
    "Dilation": "扩张",
    "Bleed": "渗色",
    "Feather": "羽化",
    "Padding": "内边距",
    "Margin": "边距",
    "Reference": "参考",
    "Reference Image": "参考图像",
    "Reference Object": "参考对象",
    "Reference Frame": "参考帧",
    "Color Space": "颜色空间",
    "Depth": "深度",
    "Alpha": "Alpha",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX19.items():
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
