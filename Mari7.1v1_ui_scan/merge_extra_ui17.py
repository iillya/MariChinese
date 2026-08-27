#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第十七批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX17 = {
    "Add Node": "添加节点",
    "Remove Node": "移除节点",
    "Duplicate Node": "复制节点",
    "Connect Node": "连接节点",
    "Disconnect Node": "断开节点",
    "Rename Node": "重命名节点",
    "Collapse Node": "折叠节点",
    "Expand Node": "展开节点",
    "Group Node": "编组节点",
    "Ungroup Node": "取消节点编组",
    "Detach Node": "分离节点",
    "Attach Node": "附加节点",
    "Select Node": "选择节点",
    "Search Node": "搜索节点",
    "Insert Node": "插入节点",
    "Move Node": "移动节点",
    "Create Input": "创建输入",
    "Create Output": "创建输出",
    "Add Input": "添加输入",
    "Add Output": "添加输出",
    "Remove Input": "移除输入",
    "Remove Output": "移除输出",
    "Connect Input": "连接输入",
    "Connect Output": "连接输出",
    "Node Inputs": "节点输入",
    "Node Outputs": "节点输出",
    "Node Properties": "节点属性",
    "Node Type": "节点类型",
    "Node Name": "节点名称",
    "Node Label": "节点标签",
    "Node Description": "节点说明",
    "Node Position": "节点位置",
    "Node Size": "节点大小",
    "Show Node Options": "显示节点选项",
    "Hide Node Options": "隐藏节点选项",
    "Set Node Properties": "设置节点属性",
    "Align Nodes": "对齐节点",
    "Arrange Nodes": "排列节点",
    "Distribute Nodes": "分布节点",
    "Rank Nodes": "排序节点",
    "Reroute": "改线",
    "Tee": "分接",
    "Mix": "混合",
    "Mixer": "混合器",
    "Add Layer Mask": "添加图层蒙版",
    "Remove Layer Mask": "移除图层蒙版",
    "Enable Layer Mask": "启用图层蒙版",
    "Disable Layer Mask": "禁用图层蒙版",
    "Invert Layer Mask": "反转图层蒙版",
    "Apply Layer Mask": "应用图层蒙版",
    "Move Layer Mask": "移动图层蒙版",
    "Select Layer Mask": "选择图层蒙版",
    "Deselect Layer Mask": "取消选择图层蒙版",
    "Mask Attributes": "蒙版属性",
    "Mask Type": "蒙版类型",
    "Mask Name": "蒙版名称",
    "Mask Color": "蒙版颜色",
    "Mask Opacity": "蒙版不透明度",
    "Mask Mode": "蒙版模式",
    "Mask Blur": "蒙版模糊",
    "Mask Feather": "蒙版羽化",
    "Mask Density": "蒙版密度",
    "Mask Strength": "蒙版强度",
    "Mask Invert": "蒙版反转",
    "Show Mask": "显示蒙版",
    "Hide Mask": "隐藏蒙版",
    "Mask Alone": "单独显示蒙版",
    "Mask Preview": "蒙版预览",
    "Masked": "已遮罩",
    "Unmasked": "未遮罩",
    "Selection Mask": "选择蒙版",
    "Procedural Mask": "程序化蒙版",
    "Smart Mask": "智能蒙版",
    "Layer Mask": "图层蒙版",
    "Group Mask": "组蒙版",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX17.items():
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
