#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第二十七批：混合模式/颜色科学/工作流补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX27 = {
    "Normal": "正常",
    "Multiply": "正片叠底",
    "Screen": "滤色",
    "Overlay": "叠加",
    "Soft Light": "柔光",
    "Hard Light": "强光",
    "Color Dodge": "颜色减淡",
    "Color Burn": "颜色加深",
    "Darken": "变暗",
    "Lighten": "变亮",
    "Difference": "差值",
    "Exclusion": "排除",
    "Add": "相加",
    "Subtract": "相减",
    "Divide": "相除",
    "Average": "平均",
    "Pin Light": "点光",
    "Vivid Light": "鲜明光",
    "Linear Light": "线性光",
    "Hard Mix": "实色混合",
    "Hue": "色相",
    "Saturation": "饱和度",
    "Color": "颜色",
    "Luminosity": "明度",
    "Blend Mode": "混合模式",
    "Blend": "混合",
    "Blending": "混合",
    "Blend Color": "混合颜色",
    "Blend Opacity": "混合不透明度",
    "Blend All": "全部混合",
    "Apply Blend": "应用混合",
    "Remove Blend": "移除混合",
    "Reset Blend": "重置混合",
    "Blend Override": "混合覆盖",
    "Blend Offset": "混合偏移",
    "Blend Ramp": "混合渐变",
    "Blend Curve": "混合曲线",
    "Blend Weight": "混合权重",
    "Gradient": "渐变",
    "Gradient Editor": "渐变编辑器",
    "Gradient Type": "渐变类型",
    "Gradient Color": "渐变颜色",
    "Gradient Start": "渐变起点",
    "Gradient End": "渐变终点",
    "Gradient Angle": "渐变角度",
    "Gradient Repeat": "渐变重复",
    "Edit Gradient": "编辑渐变",
    "Add Gradient Stop": "添加渐变色标",
    "Remove Gradient Stop": "移除渐变色标",
    "Reset Gradient": "重置渐变",
    "Ramp": "渐变条",
    "Color Ramp": "颜色渐变",
    "Alpha Ramp": "Alpha 渐变",
    "Falloff": "衰减",
    "Falloff Rate": "衰减速率",
    "Falloff Curve": "衰减曲线",
    "Falloff Type": "衰减类型",
    "Linear": "线性",
    "Smooth": "平滑",
    "Ease In": "缓入",
    "Ease Out": "缓出",
    "Ease In Out": "缓入缓出",
    "Clamp": "钳制",
    "Dither": "抖动",
    "Interpolate": "插值",
    "Interpolation": "插值",
    "Wrap Mode": "循环模式",
    "Repeat Mode": "重复模式",
    "Mirror Mode": "镜像模式",
    "Clamp Mode": "钳制模式",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX27.items():
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
