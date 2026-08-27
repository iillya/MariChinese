#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第三批：从全量候选挑出明确的用户可见提示/状态/对话框，翻译后并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX3 = {
    # ---- 用户可见提示 / 状态 / 错误对话框 ----
    "Affects how the image data is displayed.": "影响图像数据的显示方式。",
    "All files must have the same extension": "所有文件必须具有相同的扩展名",
    "All files must have the same extension: '.%1' and '.%2' were selected": "所有文件必须具有相同的扩展名：选择了 '.%1' 和 '.%2'",
    "All licenses are currently in use.": "所有许可证都正在使用中。",
    "All rights reserved.": "保留所有权利。",
    "An attribute with that name already exists, please pick a unique name": "已存在同名属性，请选择唯一的名称",
    "An error occurred during logout.": "登出时发生错误。",
    "An error occurred during thumbnail generation.": "生成缩略图时发生错误。",
    "An error occurred while returning your licenses.": "退回许可证时发生错误。",
    "An error occurred while writing to the destination file.": "写入目标文件时发生错误。",
    "Any language": "任何语言",
    "Are you sure you want to delete '%1'": "确定要删除 '%1' 吗",
    "Are you sure you want to remove": "确定要移除",
    "As such, the preview may appear incorrect or incomplete.": "因此，预览可能显示不正确或不完整。",
    "Background jobs are running": "后台任务正在运行",
    "Busy processing background jobs, please wait and try again": "后台任务正在处理中，请稍候再试",
    "Cannot group locked shelves or groups.": "无法对锁定的架子或组进行分组。",
    "Cannot import on this shelf as the latter is locked.": "无法导入到此架子，因为它已锁定。",
    "Cannot import multiple files for the file type '.%1'": "无法为文件类型 '.%1' 导入多个文件",
    "Cannot initialize Tool": "无法初始化工具",
    "Cannot initialize brush": "无法初始化笔刷",
    "Cannot link an image to itself": "无法将图像链接到自身",
    "Cannot link knobs of different types.": "无法链接不同类型的控件。",
    "Cannot load incoming image": "无法加载传入图像",
    "Cannot load item on this shelf as the latter is locked.": "无法加载此架子上的项目，因为它已锁定。",
    "Cannot load on this shelf as the latter is locked.": "无法加载到此架子，因为它已锁定。",
    "Cannot load reference image": "无法加载参考图像",
    "Cannot load texture": "无法加载纹理",
    "Cannot merge locked groups.": "无法合并锁定的组。",
    "Cannot open a project when one is already open.": "已有项目打开时，无法再打开其他项目。",
    "Cannot open file": "无法打开文件",
    "Cannot open input license file for installation.": "无法打开要安装的许可证文件。",
    "Choose another directory": "选择另一个目录",
    "Choose another project directory": "选择另一个项目目录",
    "Close the current project": "关闭当前项目",
    "Continue Anyway": "仍然继续",
    "Create a new project": "创建新项目",
    "Create a new shelf": "创建新架子",
    "Default Resolution": "默认分辨率",
    "Do not convert the data. For most": "不要转换数据。对于大多数",
    "Do this for all images": "对所有图像执行此操作",
    "Don't show again": "不再显示",
    "Don't show this again": "不再显示此内容",
    "File name:": "文件名：",
    "File of type:": "文件类型：",
    "Files to overwrite:": "要覆盖的文件：",
    "Folders to create:": "要创建的文件夹：",
    "No valid selection group has been passed.": "未传入有效的选择组。",
    "Only one project can be loaded at a time.": "一次只能加载一个项目。",
    "Please check the log file for details.": "请查看日志文件了解详情。",
    "Please choose another project directory": "请选择另一个项目目录",
    "Please choose another project directory.": "请选择另一个项目目录。",
    "Please choose one of the following operations:": "请选择以下操作之一：",
    "Please enter a new name for the current project:": "请为当前项目输入一个新名称：",
    "Please provide a mesh file path": "请提供网格文件路径",
    "Please provide a name for the new attribute": "请为新属性提供名称",
    "Please provide a name for the project": "请为项目提供名称",
    "Please provide a unique name for the shelf": "请为架子提供唯一的名称",
    "Please provide a valid name for the new channel": "请为新通道提供有效名称",
    "Please provide a valid name for the new tab": "请为新标签页提供有效名称",
    "Please provide an object to set as current": "请提供要设为当前的对象",
    "Please restart Mari": "请重启 Mari",
    "Please save the image before adding it to the shelf": "在添加到架子前请先保存图像",
    "Please set a valid export path on the node": "请在节点上设置有效的导出路径",
    "Please supply a valid path and template to export from": "请提供有效的路径和模板以进行导出",
    "Please supply a valid path and template to import from": "请提供有效的路径和模板以进行导入",
    "Please uncache it before importing.": "导入前请取消其缓存。",
    "Please unlock or uncache it and try again.": "请先解锁或取消缓存然后再试。",
    "Please update your drivers to version %2, or later.": "请将驱动程序更新为 %2 或更高版本。",
    "Save the current project": "保存当前项目",
    "Save the current settings as a preset": "将当前设置保存为预设",
    "Save the shelf to file": "将架子保存到文件",
    "There are no layers to export.": "没有可导出的图层。",
    "There are no patches currently selected.": "当前没有选中的面片。",
    "There are no selected layers to export.": "没有选中的图层可导出。",
    "There is no baked result to export": "没有可导出的烘焙结果",
    "There is no baked result to export.": "没有可导出的烘焙结果。",
    "There is no current layer to export.": "没有当前图层可导出。",
    "There is no project directory": "没有项目目录",
    "This change will take effect when you restart Mari": "此更改将在重启 Mari 后生效",
    "This is the Mari Non-commercial version.": "这是 Mari 非商业版。",
    "This is the first time you are running Mari %1.%2v%3": "这是你第一次运行 Mari %1.%2v%3",
    "This layer stack is locked.  Please unlock it to continue.": "此图层堆栈已锁定。请解锁后继续。",
    "This palette provides a view onto the undo / redo history": "此面板提供撤销/重做历史视图",
    "This project is owned by '%1'": "此项目由 '%1' 拥有",
    "To work around this issue, see the log for details": "要解决此问题，请查看日志了解详情",
    "To work around this issue, try:": "要解决此问题，请尝试：",
    "Unwritable Files": "不可写文件",
    "Unwritable files:": "不可写文件：",
    "You are running %1 %2": "你正在运行 %1 %2",
    "You must enter a unique collection name.": "你必须输入唯一的集合名称。",
    "Your system only has %2 GB of memory.": "你的系统只有 %2 GB 内存。",
    "You will typically want to select the": "你通常需要选择",
    "Would you like to rename the Material node to : %1": "是否要将材质节点重命名为：%1",
    "Would you like to rename the Smart Mask node to : %1": "是否要将智能蒙版节点重命名为：%1",
    "The Painting is currently blank": "当前绘制为空白",
    "The Painting was not saved correctly.": "绘制未正确保存。",
    "The UV data is missing from this geometry": "此几何体缺少 UV 数据",
    "The UV index data is missing from this geometry": "此几何体缺少 UV 索引数据",
    "The destination layer is locked and/or cached.": "目标图层已锁定和/或已缓存。",
    "The following features are disabled:": "以下功能已禁用：",
    "The following files are not writable:": "以下文件不可写：",
    "The following folders do not exist:": "以下文件夹不存在：",
    "The following will be replaced with attributes:": "以下内容将被属性替换：",
    "The missing filters were:": "缺失的滤镜有：",
    "The selected channel contains %1.": "所选通道包含 %1。",
    "The selection contains no editable items.": "所选内容包含不可编辑的项目。",
    "The smart mask group contains paint nodes.": "智能蒙版组包含绘制节点。",
    "The material group contains paint nodes.": "材质组包含绘制节点。",
    "The graphics card has limited number of texture units.": "显卡的纹理单元数量有限。",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX3.items():
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
