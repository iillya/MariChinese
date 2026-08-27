#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第十二批：通用状态/查找类界面词，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX12 = {
    "No Image Set": "无图像集",
    "No Layer selected": "未选择图层",
    "No Channel selected": "未选择通道",
    "No Object selected": "未选择对象",
    "No Patch selected": "未选择面片",
    "No Face selected": "未选择面",
    "No path set": "未设置路径",
    "No backup location": "无备份位置",
    "No geometry": "无几何体",
    "No shader": "无着色器",
    "No material": "无材质",
    "No texture": "无纹理",
    "No cache": "无缓存",
    "No version": "无版本",
    "No image": "无图像",
    "No brush": "无笔刷",
    "No camera": "无相机",
    "No light": "无灯光",
    "No layer": "无图层",
    "Invalid Layer": "无效的图层",
    "Invalid Object": "无效的对象",
    "Invalid Patch": "无效的面片",
    "Invalid Channel": "无效的通道",
    "Invalid Image": "无效的图像",
    "Invalid Brush": "无效的笔刷",
    "Invalid Project": "无效的项目",
    "Invalid Shelf": "无效的架子",
    "Invalid Path": "无效的路径",
    "Invalid Name": "无效的名称",
    "Invalid Value": "无效的值",
    "Layer not found": "未找到图层",
    "Channel not found": "未找到通道",
    "Object not found": "未找到对象",
    "Image not found": "未找到图像",
    "Project not found": "未找到项目",
    "Brush not found": "未找到笔刷",
    "Camera not found": "未找到相机",
    "Material not found": "未找到材质",
    "Layer already exists": "图层已存在",
    "Channel already exists": "通道已存在",
    "Object already exists": "对象已存在",
    "Image already exists": "图像已存在",
    "Shelf already exists": "架子已存在",
    "Name in use": "名称已被使用",
    "Path in use": "路径已被使用",
    "Cannot load": "无法加载",
    "Cannot save": "无法保存",
    "Cannot create": "无法创建",
    "Cannot open": "无法打开",
    "Cannot delete": "无法删除",
    "Cannot rename": "无法重命名",
    "Cannot export": "无法导出",
    "Cannot import": "无法导入",
    "Operation failed": "操作失败",
    "Operation cancelled": "操作已取消",
    "Operation completed": "操作已完成",
    "Operation in progress": "操作进行中",
    "Loading...": "正在加载...",
    "Saving...": "正在保存...",
    "Rendering...": "正在渲染...",
    "Processing...": "正在处理...",
    "Exporting...": "正在导出...",
    "Importing...": "正在导入...",
    "Finished": "已完成",
    "Failure": "失败",
    "Error": "错误",
    "Debug": "调试",
    "Trace": "跟踪",
    "Log": "日志",
    "Console": "控制台",
    "Untitled Project": "未命名项目",
    "Untitled Layer": "未命名图层",
    "Untitled Channel": "未命名通道",
    "Untitled Image": "未命名图像",
    "Untitled Shelf": "未命名架子",
    "Project Name": "项目名称",
    "Layer Name": "图层名称",
    "Channel Name": "通道名称",
    "File Name": "文件名",
    "Object Name": "对象名称",
    "Brush Name": "笔刷名称",
    "Shelf Name": "架子名称",
    "Enter Layer Name": "输入图层名称",
    "Enter Channel Name": "输入通道名称",
    "Enter Shelf Name": "输入架子名称",
    "Choose a Folder": "选择文件夹",
    "Choose a File": "选择文件",
    "Choose a Project": "选择项目",
    "Choose an Image": "选择图像",
    "Choose a Brush": "选择笔刷",
    "Create Folder": "创建文件夹",
    "Create Channel": "创建通道",
    "Create Layer": "创建图层",
    "Create Brush": "创建笔刷",
    "Create Camera": "创建相机",
    "Create Light": "创建灯光",
    "Create Material": "创建材质",
    "Create Image": "创建图像",
    "Create Project": "创建项目",
    "Create Preset": "创建预设",
    "Create Shortcut": "创建快捷键",
    "Add to Project": "添加到项目",
    "Add to Library": "添加到库",
    "Remove from Project": "从项目中移除",
    "Remove from Library": "从库中移除",
    "Open Library": "打开库",
    "Open Palette": "打开面板",
    "Close Palette": "关闭面板",
    "New Palette": "新建面板",
    "Show Palette": "显示面板",
    "Hide Palette": "隐藏面板",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX12.items():
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
