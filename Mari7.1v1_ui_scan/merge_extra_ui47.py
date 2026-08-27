#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第四十七批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX47 = {
    "Reference": "参考",
    "Reference Image": "参考图像",
    "Reference Layer": "参考图层",
    "Reference Object": "参考对象",
    "Reference Path": "参考路径",
    "Reference File": "参考文件",
    "Reference Mode": "参考模式",
    "Reference View": "参考视图",
    "Reference Settings": "参考设置",
    "Use as Reference": "用作参考",
    "Set as Reference": "设为参考",
    "Clear Reference": "清除参考",
    "Update Reference": "更新参考",
    "Load Reference": "加载参考",
    "Remove Reference": "移除参考",
    "Show Reference": "显示参考",
    "Hide Reference": "隐藏参考",
    "Compare with Reference": "与参考比较",
    "Match Reference": "匹配参考",
    "Align to Reference": "对齐到参考",
    "Fit Reference": "适应参考",
    "Snap to Reference": "吸附到参考",
    "Reference Color": "参考颜色",
    "Reference Scale": "参考缩放",
    "Reference Offset": "参考偏移",
    "Reference Rotation": "参考旋转",
    "Reference Position": "参考位置",
    "Reference Opacity": "参考不透明度",
    "Reference Visibility": "参考可见性",
    "Reference Lock": "参考锁定",
    "Lock Reference": "锁定参考",
    "Unlock Reference": "解锁参考",
    "Reference Preset": "参考预设",
    "Reference Preview": "参考预览",
    "Reference Data": "参考数据",
    "Reference Geometry": "参考几何体",
    "Reference Mesh": "参考网格",
    "Reference UV": "参考 UV",
    "Reference Map": "参考贴图",
    "Reference Texture": "参考纹理",
    "Reference Material": "参考材质",
    "Reference Style": "参考样式",
    "Reference Layout": "参考布局",
    "Reference Grid": "参考网格",
    "Reference Axis": "参考轴",
    "Reference Plane": "参考平面",
    "Reference Point": "参考点",
    "Reference Frame": "参考帧",
    "Reference Time": "参考时间",
    "Reference Date": "参考日期",
    "Reference Name": "参考名称",
    "Reference ID": "参考 ID",
    "Reference Number": "参考编号",
    "Reference Code": "参考代码",
    "Reference Type": "参考类型",
    "Reference Size": "参考大小",
    "Reference Count": "参考数量",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX47.items():
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
