#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第十五批：浏览器/编辑器/账户许可类界面词，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX15 = {
    "Project Browser": "项目浏览器",
    "Asset Browser": "资产浏览器",
    "Library Browser": "库浏览器",
    "Node Browser": "节点浏览器",
    "Shader Browser": "着色器浏览器",
    "Shelf Browser": "架子浏览器",
    "Preset Browser": "预设浏览器",
    "Channel Editor": "通道编辑器",
    "Shader Editor": "着色器编辑器",
    "Node Editor": "节点编辑器",
    "Geometry Editor": "几何体编辑器",
    "Image Editor": "图像编辑器",
    "Color Editor": "颜色编辑器",
    "Layer Editor": "图层编辑器",
    "Attribute Editor": "属性编辑器",
    "Property Editor": "属性编辑器",
    "Object Editor": "对象编辑器",
    "Brush Editor": "笔刷编辑器",
    "Filter Editor": "滤镜编辑器",
    "Alias Editor": "别名编辑器",
    "Project Settings Dialog": "项目设置对话框",
    "Preferences Dialog": "首选项对话框",
    "Export Dialog": "导出对话框",
    "Import Dialog": "导入对话框",
    "Render Dialog": "渲染对话框",
    "Bake Dialog": "烘焙对话框",
    "About Dialog": "关于对话框",
    "Confirm": "确认",
    "Warning Dialog": "警告对话框",
    "Error Dialog": "错误对话框",
    "Information Dialog": "信息对话框",
    "Open File Dialog": "打开文件对话框",
    "Save File Dialog": "保存文件对话框",
    "Choose Directory Dialog": "选择目录对话框",
    "License Key": "许可证密钥",
    "License Type": "许可证类型",
    "License Server": "许可证服务器",
    "Activate License": "激活许可证",
    "Deactivate License": "停用许可证",
    "Transfer License": "转移许可证",
    "Return License": "退回许可证",
    "Sign In": "登录",
    "Sign Out": "登出",
    "Account": "账户",
    "Account Settings": "账户设置",
    "User": "用户",
    "Admin": "管理员",
    "Close All Documents": "关闭所有文档",
    "Close All Windows": "关闭所有窗口",
    "Close All Tabs": "关闭所有标签页",
    "Workspace": "工作区",
    "Workspace Manager": "工作区管理器",
    "Layout": "布局",
    "Save Workspace": "保存工作区",
    "Reset Workspace": "重置工作区",
    "Default Workspace": "默认工作区",
    "Customize Workspace": "自定义工作区",
    "Tabs": "标签页",
    "Tool Tabs": "工具标签页",
    "Palette Tabs": "面板标签页",
    "Show Tabs": "显示标签页",
    "Hide Tabs": "隐藏标签页",
    "Menu Bar": "菜单栏",
    "Tool Bar": "工具栏",
    "Status Bar": "状态栏",
    "Title Bar": "标题栏",
    "Watch": "监视",
    "Watch Folder": "监视文件夹",
    "Refresh Folder": "刷新文件夹",
    "Import Folder": "导入文件夹",
    "Export Folder": "导出文件夹",
    "Project Folder": "项目文件夹",
    "Asset Folder": "资产文件夹",
    "Library Folder": "库文件夹",
    "Browse": "浏览",
    "Browse Files": "浏览文件",
    "Browse Folder": "浏览文件夹",
    "Choose Folder": "选择文件夹",
    "Choose File": "选择文件",
    "Select File": "选择文件",
    "Select Folder": "选择文件夹",
    "Search Files": "搜索文件",
    "Search Folders": "搜索文件夹",
    "New Search": "新建搜索",
    "Clear Search": "清除搜索",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX15.items():
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
