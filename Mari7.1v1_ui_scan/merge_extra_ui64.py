#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第六十四批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX64 = {
    "Color": "颜色",
    "Colors": "颜色",
    "Color Settings": "颜色设置",
    "Color Options": "颜色选项",
    "Color Properties": "颜色属性",
    "Color Name": "颜色名称",
    "Color Type": "颜色类型",
    "Color Value": "颜色值",
    "Color Mode": "颜色模式",
    "Color Model": "颜色模型",
    "Color Space": "颜色空间",
    "Color Profile": "颜色配置文件",
    "Color Temperature": "色温",
    "Color Tint": "颜色色调",
    "Color Opacity": "颜色不透明度",
    "Color Intensity": "颜色强度",
    "Color Brightness": "颜色亮度",
    "Color Saturation": "颜色饱和度",
    "Color Hue": "颜色色相",
    "Color Contrast": "颜色对比度",
    "Color Balance": "色彩平衡",
    "Color Correction": "色彩校正",
    "Color Grading": "调色",
    "Color Adjustment": "颜色调整",
    "Color Picker": "颜色选择器",
    "Color Picker Mode": "颜色选择器模式",
    "Color Picker Size": "颜色选择器大小",
    "Color Sample": "颜色采样",
    "Color Swatch": "颜色色板",
    "Color Swatches": "颜色色板",
    "Color Palette": "颜色面板",
    "Color Wheel": "颜色轮盘",
    "Color Ramp": "颜色渐变",
    "Color Gradient": "颜色渐变",
    "Color Curve": "颜色曲线",
    "Color Histogram": "颜色直方图",
    "Color Matrix": "颜色矩阵",
    "Color LUT": "颜色 LUT",
    "Color Look": "颜色外观",
    "Primaries": "基色",
    "White Point": "白点",
    "Black Point": "黑点",
    "Midpoint": "中间点",
    "Exposure": "曝光",
    "Saturation": "饱和度",
    "Hue": "色相",
    "Saturation Value": "饱和度值",
    "Hue Value": "色相值",
    "Luminance": "亮度",
    "Brightness": "亮度",
    "Contrast": "对比度",
    "Vibrance": "自然饱和度",
    "Saturation Shift": "饱和度偏移",
    "Hue Shift": "色相偏移",
    "Tint": "色调",
    "Shade": "阴影",
    "Tone": "色调",
    "Tone Map": "色调映射",
    "Tone Mapping": "色调映射",
    "Tone Curve": "色调曲线",
    "Color Mapping": "颜色映射",
    "Color Domain": "颜色域",
    "Color Range": "颜色范围",
    "Color Clamp": "颜色钳制",
    "Color Blend": "颜色混合",
    "Color Mix": "颜色混合",
    "Color Overlay": "颜色覆盖",
    "Color Multiply": "颜色正片叠底",
    "Color Screen": "颜色滤色",
    "Color Dodge": "颜色减淡",
    "Color Burn": "颜色加深",
    "Color Darken": "颜色变暗",
    "Color Lighten": "颜色变亮",
    "Color Difference": "颜色差值",
    "Color Exclusion": "颜色排除",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX64.items():
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
