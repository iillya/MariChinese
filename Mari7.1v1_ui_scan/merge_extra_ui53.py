#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第五十三批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX53 = {
    "Import": "导入",
    "Import File": "导入文件",
    "Import Folder": "导入文件夹",
    "Import Images": "导入图像",
    "Import Image Set": "导入图像集",
    "Import Channel": "导入通道",
    "Import Layer": "导入图层",
    "Import Material": "导入材质",
    "Import Texture": "导入纹理",
    "Import Model": "导入模型",
    "Import Mesh": "导入网格",
    "Import Geometry": "导入几何体",
    "Import Object": "导入对象",
    "Import Project": "导入项目",
    "Import Scene": "导入场景",
    "Import Preset": "导入预设",
    "Import Brush": "导入笔刷",
    "Import Archive": "导入归档",
    "Import Shelf": "导入架子",
    "Import Tag": "导入标签",
    "Import Selection": "导入选择",
    "Import Sequence": "导入序列",
    "Import Options": "导入选项",
    "Import Settings": "导入设置",
    "Import Path": "导入路径",
    "Import Folder Path": "导入文件夹路径",
    "Import File Path": "导入文件路径",
    "Import Format": "导入格式",
    "Import Type": "导入类型",
    "Import Mode": "导入模式",
    "Import Scale": "导入缩放",
    "Import Offset": "导入偏移",
    "Import Rotation": "导入旋转",
    "Import Units": "导入单位",
    "Import Resolution": "导入分辨率",
    "Import Size": "导入大小",
    "Import Color": "导入颜色",
    "Import Color Space": "导入颜色空间",
    "Import Mipmaps": "导入 Mipmap",
    "Import Proxy": "导入代理",
    "Import Padding": "导入内边距",
    "Import as New": "导入为新项目",
    "Import as Copy": "导入为副本",
    "Import as Reference": "导入为参考",
    "Import New Version": "导入新版本",
    "Import Overwrite": "覆盖导入",
    "Import Merge": "合并导入",
    "Import Replace": "替换导入",
    "Import Append": "追加导入",
    "Preserve": "保留",
    "Preserve on Import": "导入时保留",
    "Discard on Import": "导入时丢弃",
    "Import Complete": "导入完成",
    "Import Failed": "导入失败",
    "Import in Progress": "导入进行中",
    "Import Cancelled": "导入已取消",
    "Import Success": "导入成功",
    "Import Error": "导入错误",
    "Import Warning": "导入警告",
    "Import Summary": "导入摘要",
    "Import Details": "导入详情",
    "Import Result": "导入结果",
    "Import Items": "导入项目",
    "Selected for Import": "选择以导入",
    "Files to Import": "要导入的文件",
    "Importing Files": "正在导入文件",
    "Importing Data": "正在导入数据",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX53.items():
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
