#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第八十三批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX83 = {
    "Show": "显示",
    "Hide": "隐藏",
    "Toggle": "切换",
    "Enable": "启用",
    "Disable": "禁用",
    "Invert": "反转",
    "Flip": "翻转",
    "Mirror": "镜像",
    "Rotate": "旋转",
    "Scale": "缩放",
    "Twist": "扭转",
    "Skew": "倾斜",
    "Distort": "扭曲",
    "Warp": "弯曲",
    "Deform": "变形",
    "Bend": "弯曲",
    "Squeeze": "挤压",
    "Stretch": "拉伸",
    "Shrink": "收缩",
    "Inflate": "膨胀",
    "Punch": "冲压",
    "Relax": "松弛",
    "Smooth": "平滑",
    "Sharpen": "锐化",
    "Dirty": "弄脏",
    "Enhance": "增强",
    "Enhance Detail": "增强细节",
    "Enhance Color": "增强颜色",
    "Enhance Contrast": "增强对比度",
    "Enhance Edges": "增强边缘",
    "Enhance Details": "增强细节",
    "Blur Radius": "模糊半径",
    "Blur Amount": "模糊量",
    "Blur Strength": "模糊强度",
    "Blur Direction": "模糊方向",
    "Blur Type": "模糊类型",
    "Blur Mode": "模糊模式",
    "Gaussian Blur": "高斯模糊",
    "Box Blur": "方框模糊",
    "Motion Blur": "运动模糊",
    "Radial Blur": "径向模糊",
    "Zoom Blur": "缩放模糊",
    "Lens Blur": "镜头模糊",
    "Surface Blur": "表面模糊",
    "Sharpness Strength": "锐度强度",
    "Sharpen Amount": "锐化量",
    "Sharpen Radius": "锐化半径",
    "Sharpen Strength": "锐化强度",
    "Unsharp Mask": "锐化遮罩",
    "Smart Sharpen": "智能锐化",
    "Noise Amount": "噪点量",
    "Noise Type": "噪点类型",
    "Noise Size": "噪点大小",
    "Noise Strength": "噪点强度",
    "Add Noise": "添加噪点",
    "Reduce Noise": "减少噪点",
    "Remove Noise": "移除噪点",
    "Denoise Strength": "降噪强度",
    "Noise Reduction": "降噪",
    "Median": "中值",
    "Median Filter": "中值滤镜",
    "Median Radius": "中值半径",
    "De-noise": "降噪",
    "Deinterlace": "去隔行",
    "Despeckle": "去斑点",
    "Remove Dust": "去除灰尘",
    "Remove Scratches": "去除划痕",
    "Retouch": "修饰",
    "Retouch Brush": "修饰笔刷",
    "Healing": "修复",
    "Healing Brush": "修复笔刷",
    "Patch": "修补",
    "Patch Tool": "修补工具",
    "Content Aware Fill": "内容识别填充",
    "Content Fill": "内容填充",
    "Smart Fill": "智能填充",
    "Spot Healing": "斑点修复",
    "Clone Adjust": "克隆调整",
    "Clone Stamp": "克隆图章",
    "Pattern Stamp": "图案图章",
    "Pattern Fill": "图案填充",
    "Pattern Preview": "图案预览",
    "Pattern Type": "图案类型",
    "Pattern Scale": "图案缩放",
    "Pattern Offset": "图案偏移",
    "Pattern Rotation": "图案旋转",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX83.items():
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
