#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第十六批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX16 = {
    "Render": "渲染",
    "Render Frame": "渲染帧",
    "Render Preview": "渲染预览",
    "Render All": "全部渲染",
    "Render Selected": "渲染所选",
    "Render Range": "渲染范围",
    "Render Sequence": "渲染序列",
    "Start Render": "开始渲染",
    "Stop Render": "停止渲染",
    "Render Output": "渲染输出",
    "Render Engine": "渲染引擎",
    "Render Pass": "渲染通道",
    "Render In Background": "后台渲染",
    "Export Render": "导出渲染",
    "Save Render": "保存渲染",
    "Adjust Colors": "调整颜色",
    "Adjust Lighting": "调整灯光",
    "Adjust Curves": "调整曲线",
    "Adjust Levels": "调整色阶",
    "Auto Levels": "自动色阶",
    "Auto Contrast": "自动对比度",
    "Auto Color": "自动颜色",
    "Brightness": "亮度",
    "Contrast": "对比度",
    "Saturation": "饱和度",
    "Hue": "色相",
    "Exposure": "曝光",
    "Gamma": "伽马",
    "Vibrance": "自然饱和度",
    "Sharpness": "锐度",
    "Blur": "模糊",
    "Noise": "噪点",
    "Denoise": "降噪",
    "Grain": "颗粒",
    "Vignette": "暗角",
    "Chromatic Aberration": "色差",
    "Color Balance": "色彩平衡",
    "White Balance": "白平衡",
    "Color Temperature": "色温",
    "Tint": "色调",
    "Black Point": "黑点",
    "White Point": "白点",
    "Midpoint": "中间点",
    "Gamma Correction": "伽马校正",
    "Color Correct": "色彩校正",
    "Color Correction": "色彩校正",
    "Color Adjustments": "颜色调整",
    "Adjust Exposure": "调整曝光",
    "Adjust White Balance": "调整白平衡",
    "Apply Color Grading": "应用调色",
    "Reset Colors": "重置颜色",
    "Grade": "分级",
    "Look": "外观",
    "LUT": "LUT",
    "Load LUT": "加载 LUT",
    "Apply LUT": "应用 LUT",
    "Remove LUT": "移除 LUT",
    "Color Space": "颜色空间",
    "Working Space": "工作空间",
    "Display Space": "显示空间",
    "Input Space": "输入空间",
    "Output Space": "输出空间",
    "Source Space": "源空间",
    "Target Space": "目标空间",
    "Transform": "变换",
    "Transform Tool": "变换工具",
    "Move Tool": "移动工具",
    "Rotate Tool": "旋转工具",
    "Scale Tool": "缩放工具",
    "Select Tool": "选择工具",
    "Paint Tool": "绘制工具",
    "Project Tool": "投影工具",
    "Brush Tool": "笔刷工具",
    "Eyedropper Tool": "吸管工具",
    "Color Picker Tool": "颜色选择器工具",
    "Zoom Tool": "缩放工具",
    "Pan Tool": "平移工具",
    "Orbit Tool": "环绕工具",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX16.items():
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
