#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第六十三批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX63 = {
    "Filter": "滤镜",
    "Filters": "滤镜",
    "Filter Settings": "滤镜设置",
    "Filter Options": "滤镜选项",
    "Filter Properties": "滤镜属性",
    "Filter Name": "滤镜名称",
    "Filter Type": "滤镜类型",
    "Filter Mode": "滤镜模式",
    "Filter Strength": "滤镜强度",
    "Filter Opacity": "滤镜不透明度",
    "Filter Intensity": "滤镜强度",
    "Filter Amount": "滤镜量",
    "Filter Scale": "滤镜缩放",
    "Filter Offset": "滤镜偏移",
    "Filter Radius": "滤镜半径",
    "Filter Angle": "滤镜角度",
    "Filter Range": "滤镜范围",
    "Filter Order": "滤镜顺序",
    "Filter Stack": "滤镜堆栈",
    "Filter Chain": "滤镜链",
    "Filter List": "滤镜列表",
    "Filter Browser": "滤镜浏览器",
    "Filter Library": "滤镜库",
    "Filter Category": "滤镜类别",
    "Filter Group": "滤镜组",
    "Filter Preset": "滤镜预设",
    "Filter Preview": "滤镜预览",
    "Filter Preview Mode": "滤镜预览模式",
    "Filter Preview Size": "滤镜预览大小",
    "Filter Preview Opacity": "滤镜预览不透明度",
    "Apply Filter": "应用滤镜",
    "Apply Filter To": "将滤镜应用到",
    "Apply Filter To Layer": "将滤镜应用到图层",
    "Apply Filter To Channel": "将滤镜应用到通道",
    "Apply Filter To Image": "将滤镜应用到图像",
    "Apply Filter To Bake Point": "将滤镜应用到烘焙点",
    "Apply Filter To Baked Result": "将滤镜应用到烘焙结果",
    "Remove Filter": "移除滤镜",
    "Delete Filter": "删除滤镜",
    "Duplicate Filter": "复制滤镜",
    "Rename Filter": "重命名滤镜",
    "Edit Filter": "编辑滤镜",
    "Reset Filter": "重置滤镜",
    "Restore Filter": "还原滤镜",
    "Enable Filter": "启用滤镜",
    "Disable Filter": "禁用滤镜",
    "Bypass Filter": "旁路滤镜",
    "Toggle Filter": "切换滤镜",
    "Insert Filter": "插入滤镜",
    "Add Filter": "添加滤镜",
    "Remove Filters": "移除滤镜",
    "Clear Filters": "清除滤镜",
    "Move Filter Up": "上移滤镜",
    "Move Filter Down": "下移滤镜",
    "Reorder Filters": "重新排序滤镜",
    "Filter Application": "滤镜应用",
    "Filter Baking": "滤镜烘焙",
    "Filter Processing": "滤镜处理",
    "Filter Result": "滤镜结果",
    "Filter Output": "滤镜输出",
    "Filter Mask": "滤镜蒙版",
    "Filter Enabled": "滤镜已启用",
    "Filter Disabled": "滤镜已禁用",
    "Filter Applied": "滤镜已应用",
    "Filter Removed": "滤镜已移除",
    "Filter Baked": "滤镜已烘焙",
    "Filter in Progress": "滤镜处理中",
    "Filter Complete": "滤镜处理完成",
    "Filter Failed": "滤镜处理失败",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX63.items():
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
