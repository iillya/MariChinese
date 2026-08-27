#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第三十八批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX38 = {
    "Click": "点击",
    "Right Click": "右键点击",
    "Left Click": "左键点击",
    "Double Click": "双击",
    "Middle Click": "中键点击",
    "Drag": "拖动",
    "Drag and Drop": "拖放",
    "Drop": "放置",
    "Hover": "悬停",
    "Press": "按下",
    "Hold": "按住",
    "Release": "松开",
    "Tap": "轻点",
    "Swipe": "滑动",
    "Scroll": "滚动",
    "Wheel": "滚轮",
    "Click to Select": "点击选择",
    "Click to Open": "点击打开",
    "Click to Edit": "点击编辑",
    "Click to Apply": "点击应用",
    "Click to Toggle": "点击切换",
    "Click to Execute": "点击执行",
    "Double Click to Edit": "双击编辑",
    "Right Click for Options": "右键查看选项",
    "Drag to Move": "拖动移动",
    "Drag to Resize": "拖动调整大小",
    "Drag to Reorder": "拖动重新排序",
    "Drag to Create": "拖动创建",
    "Scroll to Zoom": "滚动缩放",
    "Hover for Details": "悬停查看详情",
    "Hover to Preview": "悬停预览",
    "Alt": "Alt",
    "Ctrl": "Ctrl",
    "Shift": "Shift",
    "Tab": "Tab",
    "Esc": "Esc",
    "Enter": "Enter",
    "Space": "空格",
    "Backspace": "退格",
    "Delete": "Delete",
    "Arrow Up": "上方向键",
    "Arrow Down": "下方向键",
    "Arrow Left": "左方向键",
    "Arrow Right": "右方向键",
    "Home": "Home",
    "End": "End",
    "Page Up": "Page Up",
    "Page Down": "Page Down",
    "Short Key": "快捷键",
    "Hotkey": "快捷键",
    "Hot Key": "快捷键",
    "Key Binding": "按键绑定",
    "Mouse Key": "鼠标键",
    "Trigger": "触发",
    "Activate": "激活",
    "Trigger Action": "触发操作",
    "Action Key": "操作键",
    "Modifier": "修饰键",
    "Modifier Key": "修饰键",
    "Combination": "组合",
    "Key Combination": "按键组合",
    "Keypress": "按键",
    "Keystroke": "按键",
    "Shortcut Key": "快捷键",
    "Short Key Name": "快捷键名称",
    "Gesture": "手势",
    "Mouse Gesture": "鼠标手势",
    "Tablet Gesture": "数位板手势",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX38.items():
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
