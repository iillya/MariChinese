#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第五十九批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX59 = {
    "Units": "单位",
    "Unit Settings": "单位设置",
    "Unit System": "单位系统",
    "Pixel Units": "像素单位",
    "Centimeter": "厘米",
    "Millimeter": "毫米",
    "Meter": "米",
    "Inch": "英寸",
    "Foot": "英尺",
    "Pixels": "像素",
    "Percent": "百分比",
    "Percentages": "百分比",
    "Degrees": "度",
    "Radians": "弧度",
    "Factor": "系数",
    "Scale Factor": "缩放系数",
    "Multiplier": "倍率",
    "Divisor": "除数",
    "Ratio": "比率",
    "Proportion": "比例",
    "Frac": "分数",
    "Indicator": "指示器",
    "Readout": "读数",
    "Gauge": "仪表",
    "Meter": "仪表",
    "Dial": "刻度盘",
    "Slider": "滑块",
    "Slider Range": "滑块范围",
    "Slider Value": "滑块值",
    "Slider Min": "滑块最小值",
    "Slider Max": "滑块最大值",
    "Slider Step": "滑块步长",
    "Number Field": "数字输入框",
    "Text Field": "文本框",
    "Input Field": "输入框",
    "Combo Box": "下拉框",
    "Dropdown": "下拉菜单",
    "Check Box": "复选框",
    "Radio Button": "单选按钮",
    "Toggle Button": "切换按钮",
    "Push Button": "按钮",
    "Button": "按钮",
    "Button Text": "按钮文本",
    "Button Label": "按钮标签",
    "Button Icon": "按钮图标",
    "Button Style": "按钮样式",
    "Button Size": "按钮大小",
    "Button Position": "按钮位置",
    "Tab": "标签页",
    "Tab Label": "标签页标签",
    "Tab Icon": "标签页图标",
    "Tab Order": "标签页顺序",
    "Tab Index": "标签页索引",
    "Active Tab": "活动标签页",
    "Inactive Tab": "非活动标签页",
    "Close Tab": "关闭标签页",
    "Open Tab": "打开标签页",
    "New Tab": "新建标签页",
    "Dock": "停靠",
    "Undock": "取消停靠",
    "Float": "浮动",
    "Maximize": "最大化",
    "Minimize": "最小化",
    "Restore Down": "向下还原",
    "Restore Up": "向上还原",
    "Full Screen": "全屏",
    "Exit Full Screen": "退出全屏",
    "Toggle Full Screen": "切换全屏",
    "Window Mode": "窗口模式",
    "Windowed": "窗口化",
    "Maximized": "已最大化",
    "Minimized": "已最小化",
    "Restored": "已还原",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX59.items():
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
