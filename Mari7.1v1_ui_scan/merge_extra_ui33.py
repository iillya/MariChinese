#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第三十三批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX33 = {
    "File Name": "文件名",
    "Folder Name": "文件夹名",
    "Project Folder Name": "项目文件夹名",
    "Import File Name": "导入文件名",
    "Export File Name": "导出文件名",
    "Save File Name": "保存文件名",
    "New File Name": "新文件名",
    "Current File Name": "当前文件名",
    "File Extension": "文件扩展名",
    "Browse For": "浏览",
    "Browse Files...": "浏览文件...",
    "Browse Folders...": "浏览文件夹...",
    "Choose Browser": "选择浏览器",
    "Output File": "输出文件",
    "Input File": "输入文件",
    "Source File": "源文件",
    "Target File": "目标文件",
    "Destination File": "目标文件",
    "File Type": "文件类型",
    "File Format": "文件格式",
    "File Path": "文件路径",
    "Content Type": "内容类型",
    "File Size": "文件大小",
    "File History": "文件历史",
    "Open As": "打开方式",
    "Open With": "用以下方式打开",
    "Save As Type": "另存为类型",
    "Save In": "保存在",
    "File List": "文件列表",
    "Recent Files": "最近文件",
    "Recent Folders": "最近文件夹",
    "Recent Projects": "最近项目",
    "Recent Images": "最近图像",
    "Recent Sessions": "最近会话",
    "Clear Recent": "清除最近记录",
    "Clear All Recent": "清除所有最近记录",
    "Reset Recent": "重置最近记录",
    "File Information": "文件信息",
    "Folder Information": "文件夹信息",
    "Project Information": "项目信息",
    "Image Information": "图像信息",
    "Channel Information": "通道信息",
    "Layer Information": "图层信息",
    "Object Information": "对象信息",
    "Geometry Information": "几何体信息",
    "Brush Information": "笔刷信息",
    "Show Information": "显示信息",
    "Hide Information": "隐藏信息",
    "Information Panel": "信息面板",
    "Information Dialog": "信息对话框",
    "Information Message": "信息消息",
    "Information Required": "需要信息",
    "More Information": "更多信息",
    "Additional Information": "附加信息",
    "Detailed Information": "详细信息",
    "Brief Information": "简要信息",
    "General Information": "常规信息",
    "System Information": "系统信息",
    "Technical Information": "技术信息",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX33.items():
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
