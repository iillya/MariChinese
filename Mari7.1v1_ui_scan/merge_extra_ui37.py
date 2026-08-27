#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第三十七批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX37 = {
    "Info": "信息",
    "Details": "详情",
    "Detail": "详情",
    "Summary": "摘要",
    "Overview": "概览",
    "Description": "说明",
    "Label": "标签",
    "Title": "标题",
    "Name": "名称",
    "Label Text": "标签文本",
    "Tooltip": "工具提示",
    "Hint Text": "提示文本",
    "Placeholder": "占位符",
    "Default Value": "默认值",
    "Current Value": "当前值",
    "New Value": "新值",
    "Old Value": "旧值",
    "Value": "值",
    "Range": "范围",
    "Min": "最小值",
    "Max": "最大值",
    "Min Value": "最小值",
    "Max Value": "最大值",
    "Step": "步长",
    "Step Size": "步长",
    "Precision": "精度",
    "Decimal Places": "小数位",
    "Unit": "单位",
    "Units": "单位",
    "Measurement": "度量",
    "Measure": "测量",
    "Unit Type": "单位类型",
    "Conversion": "转换",
    "Convert Unit": "转换单位",
    "Angle Unit": "角度单位",
    "Length Unit": "长度单位",
    "Distance": "距离",
    "Area": "面积",
    "Volume": "体积",
    "Weight": "重量",
    "Speed": "速度",
    "Temperature": "温度",
    "Resolution": "分辨率",
    "Density": "密度",
    "Rate": "速率",
    "Ratio": "比率",
    "Proportion": "比例",
    "Percentage": "百分比",
    "Percent": "百分比",
    "Fraction": "分数",
    "Factor": "系数",
    "Multiplier": "倍率",
    "Threshold": "阈值",
    "Limit": "限制",
    "Maximum": "最大值",
    "Minimum": "最小值",
    "Upper Bound": "上限",
    "Lower Bound": "下限",
    "Bound": "边界",
    "Bounds": "边界",
    "Constraint": "约束",
    "Constraint Type": "约束类型",
    "Apply Constraint": "应用约束",
    "Remove Constraint": "移除约束",
    "Constrained": "受约束",
    "Unconstrained": "不受约束",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX37.items():
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
