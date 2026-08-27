#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第四十九批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX49 = {
    "Pixel": "像素",
    "Pixels": "像素",
    "Pixel Size": "像素大小",
    "Pixel Density": "像素密度",
    "Pixel Format": "像素格式",
    "Pixel Depth": "像素深度",
    "Pixel Ratio": "像素比例",
    "Pixel Aspect": "像素宽高比",
    "Pixel Dimensions": "像素尺寸",
    "Pixels Per Inch": "每英寸像素",
    "Resolution": "分辨率",
    "Resolution Width": "分辨率宽度",
    "Resolution Height": "分辨率高度",
    "Resolution X": "X 分辨率",
    "Resolution Y": "Y 分辨率",
    "Resolution Z": "Z 分辨率",
    "Resolution Scale": "分辨率缩放",
    "Resolution Mode": "分辨率模式",
    "Resolution Quality": "分辨率质量",
    "Resolution Settings": "分辨率设置",
    "Width": "宽度",
    "Height": "高度",
    "Depth": "深度",
    "Width X": "宽度 X",
    "Height Y": "高度 Y",
    "Depth Z": "深度 Z",
    "Aspect Ratio": "宽高比",
    "Pixel Aspect Ratio": "像素宽高比",
    "Frame Aspect Ratio": "帧宽高比",
    "Square Pixels": "方形像素",
    "Non-Square Pixels": "非方形像素",
    "Full Resolution": "完整分辨率",
    "Half Resolution": "半分辨率",
    "Quarter Resolution": "四分之一分辨率",
    "Percent Resolution": "百分比分辨率",
    "Scale to Resolution": "缩放到分辨率",
    "Fit Resolution": "适应分辨率",
    "Sample": "采样",
    "Samples": "采样",
    "Sample Rate": "采样率",
    "Sample Count": "采样数量",
    "Sample Size": "采样大小",
    "Sample Value": "采样值",
    "Take Sample": "采样",
    "Reset Sample": "重置采样",
    "Apply Sample": "应用采样",
    "Copy Sample": "复制采样",
    "Paste Sample": "粘贴采样",
    "Add Sample": "添加采样",
    "Remove Sample": "移除采样",
    "Sample Color": "采样颜色",
    "Sample Pixel": "采样像素",
    "Sample Region": "采样区域",
    "Sample Area": "采样区域",
    "Sample Point": "采样点",
    "Sample Grid": "采样网格",
    "Sample Mask": "采样蒙版",
    "Sample Layer": "采样图层",
    "Sample Channel": "采样通道",
    "Sample Image": "采样图像",
    "Sample Order": "采样顺序",
    "Sample Pattern": "采样模式",
    "Sample Coverage": "采样覆盖",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX49.items():
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
