#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第八批：用户可见状态/提示/节点校验句，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX8 = {
    "Coding Error": "编码错误",
    "Colorspace index is out of range": "颜色空间索引超出范围",
    "Connected to Nuke": "已连接到 Nuke",
    "Custom font size in points.": "自定义字体大小（单位：点）。",
    "Decompress failed": "解压失败",
    "Diffuse node must carry _diffuse tag": "漫反射节点必须带有 _diffuse 标签",
    "Skipped installing one or more licenses": "跳过了部分许可证的安装",
    "Sorry, Cannot copy Data": "抱歉，无法复制数据",
    "Sorry, Could not copy Data": "抱歉，无法复制数据",
    "System clock has been set back": "系统时钟已被回拨",
    "Tag '%1' is invalid": "标签 '%1' 无效",
    "Tags can only be added to node archives, materials & smart masks.": "标签只能添加到节点归档、材质和智能蒙版。",
    "Target already exists": "目标已存在",
    "Tool not found": "未找到工具",
    "User cancelled color selection": "用户取消了颜色选择",
    "User choose to resize channels linked via shared layers.": "用户选择调整通过共享层链接的通道大小。",
    "User choose to resize locked layers.": "用户选择调整锁定图层的大小。",
    "User choose to resize shared layers.": "用户选择调整共享图层的大小。",
    "Windows Server 2008 R2": "Windows Server 2008 R2",
    "Writing into the mask stack on": "正在向蒙版堆栈写入（对象：）",
    "XML is empty": "XML 为空",
    "Zero length set named passed": "传入的集合名称为空",
    "Scaling cancelled": "缩放已取消",
    "Scaling complete": "缩放完成",
    "Smooth Normals Cmds": "平滑法线命令",
    "Sort Term is empty": "排序条件为空",
    "Sorted by": "排序依据",
    "Step size when raymarching volume": "体积光线步进的步长",
    "Sub-Menu Timeout": "子菜单超时",
    "Success": "成功",
    "Unable to create shader.": "无法创建着色器。",
    "Unable to find shader input node for channel.": "无法找到通道的着色器输入节点。",
    "Unsupported DDS format": "不支持的 DDS 格式",
    "Unsupported format": "不支持的格式",
    "Unsupported image data type": "不支持的图像数据类型",
    "Unsupported object type": "不支持的对象类型",
    "Unsupported texture type": "不支持的纹理类型",
    "Unsupported type": "不支持的类型",
    "View Image": "查看图像",
    "View Summary": "查看摘要",
    "Upgrading Brushes": "正在升级笔刷",
    "No node was created with key : Misc/Empty": "未创建键为 Misc/Empty 的节点",
    "No node was created with key : Misc/EmptyWithSkip": "未创建键为 Misc/EmptyWithSkip 的节点",
    "Node to duplicate is invalid": "要复制的节点无效",
    "Node to group is invalid": "要编组的节点无效",
    "Nothing to bake": "没有可烘焙的内容",
    "Nothing to save": "没有可保存的内容",
    "Object cannot be duplicated": "无法复制对象",
    "Object is already in the group": "对象已在组中",
    "Only one project can be loaded at a time.": "一次只能加载一个项目。",
    "Patch to duplicate is invalid": "要复制的面片无效",
    "Please choose a valid project location": "请选择有效的项目位置",
    "Please choose an output file": "请选择一个输出文件",
    "Please enter a name for the new tab": "请为新标签页输入名称",
    "Please select a face": "请选择一个面",
    "Please select a patch": "请选择一个面片",
    "Please select an object": "请选择一个对象",
    "Project already has a backup location": "项目已有备份位置",
    "Project location not found": "未找到项目位置",
    "Replace the current layer?": "是否替换当前图层？",
    "Rename Failed": "重命名失败",
    "Restart Mari to apply this change": "重启 Mari 以应用此更改",
    "Save Operation Failed": "保存操作失败",
    "Shader to duplicate is not valid.": "要复制的着色器无效。",
    "Shortcut already exists for given item": "给定项目已存在快捷键",
    "Specified index is out of range": "指定的索引超出范围",
    "SplineAPI is not correctly initialized": "SplineAPI 未正确初始化",
    "Stream blend node has no over input": "流混合节点没有叠加输入",
    "Target layer is not paintable": "目标图层不可绘制",
    "Too many lut filters to give a unique name": "LUT 滤镜过多，无法提供唯一名称",
    "Undo Failed": "撤销失败",
    "Unknown error": "未知错误",
    "Unload of plugin failed": "卸载插件失败",
    "Upgrade cancelled, via environment variable MARI_AUTOUPGRADE_CONFIGURATION set to False": "升级已取消，因为环境变量 MARI_AUTOUPGRADE_CONFIGURATION 设置为 False",
    "Upgrade cancelled": "升级已取消",
    "Version is invalid": "版本无效",
    "Warning: It is highly recomended that you use Mari with a virtual memory system.": "警告：强烈建议你配合虚拟内存系统使用 Mari。",
    "Width and height are different": "宽度和高度不同",
    "Would you like to overwrite the existing file?": "是否要覆盖现有文件？",
    "Your changes have been saved.": "你的更改已保存。",
    "Zoom to 100%": "缩放到 100%",
    "Zoom to Fit": "缩放至适应",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX8.items():
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
        print("已存在跳过:", existed)


if __name__ == "__main__":
    main()
