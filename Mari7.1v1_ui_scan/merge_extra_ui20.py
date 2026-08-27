#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第二十批：着色器/程序化/滤镜/绘制类界面词，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX20 = {
    "Shader Network": "着色器网络",
    "Shader Node": "着色器节点",
    "Shader Model": "着色器模型",
    "Shader Type": "着色器类型",
    "Shader Name": "着色器名称",
    "Shader Layer": "着色器图层",
    "Shader Graph": "着色器图",
    "Shader Input": "着色器输入",
    "Shader Output": "着色器输出",
    "Shader Settings": "着色器设置",
    "Create Shader": "创建着色器",
    "Connect Shader": "连接着色器",
    "Disconnect Shader": "断开着色器",
    "Duplicate Shader": "复制着色器",
    "Edit Shader": "编辑着色器",
    "Select Shader": "选择着色器",
    "Delete Shader": "删除着色器",
    "Procedural": "程序化",
    "Procedural Layer": "程序化图层",
    "Procedural Node": "程序化节点",
    "Procedural Shader": "程序化着色器",
    "Procedural Filter": "程序化滤镜",
    "Procedural Settings": "程序化设置",
    "Create Procedural": "创建程序化",
    "Procedural Type": "程序化类型",
    "Procedural Color": "程序化颜色",
    "Procedural Scalar": "程序化标量",
    "Procedural Mask": "程序化蒙版",
    "Procedural Preview": "程序化预览",
    "Filter": "滤镜",
    "Filter Stack": "滤镜堆栈",
    "Filter List": "滤镜列表",
    "Filter Settings": "滤镜设置",
    "Filter Type": "滤镜类型",
    "Filter Name": "滤镜名称",
    "Apply Filter": "应用滤镜",
    "Remove Filter": "移除滤镜",
    "Enable Filter": "启用滤镜",
    "Disable Filter": "禁用滤镜",
    "Filter Preview": "滤镜预览",
    "Filter Strength": "滤镜强度",
    "Filter Opacity": "滤镜不透明度",
    "Filter Order": "滤镜顺序",
    "Filters": "滤镜",
    "Bake Filter": "烘焙滤镜",
    "Quick Apply": "快速应用",
    "Preset Filter": "预设滤镜",
    "Default Filter": "默认滤镜",
    "Paint Buffer": "绘制缓冲区",
    "Paint Target": "绘制目标",
    "Paint Channel": "绘制通道",
    "Paint Layer": "绘制图层",
    "Paint Stack": "绘制堆栈",
    "Paint Mode": "绘制模式",
    "Paint Settings": "绘制设置",
    "Brush": "笔刷",
    "Brush Settings": "笔刷设置",
    "Brush Size": "笔刷大小",
    "Brush Opacity": "笔刷不透明度",
    "Brush Flow": "笔刷流量",
    "Brush Hardness": "笔刷硬度",
    "Brush Spacing": "笔刷间距",
    "Brush Angle": "笔刷角度",
    "Brush Rotation": "笔刷旋转",
    "Brush Scale": "笔刷缩放",
    "Brush Jitter": "笔刷抖动",
    "Brush Color": "笔刷颜色",
    "Brush Shape": "笔刷形状",
    "Brush Tip": "笔刷笔尖",
    "Brush Profile": "笔刷曲线",
    "Brush Preview": "笔刷预览",
    "Brush Texture": "笔刷纹理",
    "Brush Tool": "笔刷工具",
    "New Brush": "新建笔刷",
    "Edit Brush": "编辑笔刷",
    "Reset Brush": "重置笔刷",
    "Save Brush": "保存笔刷",
    "Load Brush": "加载笔刷",
    "Delete Brush": "删除笔刷",
    "Duplicate Brush": "复制笔刷",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX20.items():
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
