#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第四十八批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX48 = {
    "Toggle": "切换",
    "Show/Hide": "显示/隐藏",
    "Enable/Disable": "启用/禁用",
    "Lock/Unlock": "锁定/解锁",
    "On/Off": "开/关",
    "Open/Close": "打开/关闭",
    "Play/Stop": "播放/停止",
    "Expand/Collapse": "展开/折叠",
    "Show All": "显示全部",
    "Hide All": "隐藏全部",
    "Show Selected": "显示所选",
    "Hide Selected": "隐藏所选",
    "Show Unselected": "显示未选择",
    "Hide Unselected": "隐藏未选择",
    "Show Hidden": "显示隐藏",
    "Hide Hidden": "隐藏隐藏",
    "Show Locked": "显示锁定",
    "Hide Locked": "隐藏锁定",
    "Show Inactive": "显示非活动",
    "Hide Inactive": "隐藏非活动",
    "Show All Layers": "显示所有图层",
    "Hide All Layers": "隐藏所有图层",
    "Show All Channels": "显示所有通道",
    "Hide All Channels": "隐藏所有通道",
    "Show All Masks": "显示所有蒙版",
    "Hide All Masks": "隐藏所有蒙版",
    "Show All Objects": "显示所有对象",
    "Hide All Objects": "隐藏所有对象",
    "Expand All": "全部展开",
    "Collapse All": "全部折叠",
    "Expand Selected": "展开所选",
    "Collapse Selected": "折叠所选",
    "Expand All Groups": "展开所有组",
    "Collapse All Groups": "折叠所有组",
    "Expand All Folders": "展开所有文件夹",
    "Collapse All Folders": "折叠所有文件夹",
    "Select All": "全选",
    "Deselect All": "取消全选",
    "Invert All": "全部反转",
    "Clear All": "全部清除",
    "Remove All": "全部移除",
    "Delete All": "全部删除",
    "Apply All": "全部应用",
    "Reset All": "全部重置",
    "Restore All": "全部还原",
    "Reveal All": "全部显示",
    "Hide Others": "隐藏其他",
    "Show Others": "显示其他",
    "Solo This": "独奏此项",
    "Solo All": "全部独奏",
    "Unsolo All": "全部取消独奏",
    "Mute All": "全部静音",
    "Unmute All": "全部取消静音",
    "Bypass All": "全部旁路",
    "Enable All": "全部启用",
    "Disable All": "全部禁用",
    "Lock All": "全部锁定",
    "Unlock All": "全部解锁",
    "Clear All Selection": "清除所有选择",
    "Invert All Selection": "反转所有选择",
    "Select All Items": "选择所有项目",
    "Deselect All Items": "取消选择所有项目",
    "Clear All Items": "清除所有项目",
    "Remove All Items": "移除所有项目",
    "Delete All Items": "删除所有项目",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX48.items():
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
