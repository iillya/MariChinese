#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第十一批：常用界面标签/操作组合，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX11 = {
    "Default Brush": "默认笔刷",
    "Duplicate Selected": "复制所选",
    "Enabled": "已启用",
    "Fast Export": "快速导出",
    "Fast Import": "快速导入",
    "Float Window": "浮动窗口",
    "Grid": "网格",
    "Grid Size": "网格大小",
    "Import Settings": "导入设置",
    "Locked layer": "已锁定的图层",
    "Manage Shelves": "管理架子",
    "Manage Tags": "管理标签",
    "Paste Values": "粘贴值",
    "Recent Items": "最近的项目",
    "Select All Layers": "选择所有图层",
    "Select All Objects": "选择所有对象",
    "Set To": "设置为",
    "Show Properties": "显示属性",
    "Text": "文本",
    "Texture Size": "纹理大小",
    "Use as Default": "设为默认",
    "Zoom Level": "缩放级别",
    "Apply to selected": "应用到所选",
    "Apply to all layers": "应用到所有图层",
    "Apply filter": "应用滤镜",
    "Save As": "另存为",
    "Save Copy": "另存副本",
    "Save Selected": "保存所选",
    "Load Shelf": "加载架子",
    "Save Shelf": "保存架子",
    "Delete Shelf": "删除架子",
    "Rename Shelf": "重命名架子",
    "New Brush": "新建笔刷",
    "Show Brush Settings": "显示笔刷设置",
    "Reset Brush": "重置笔刷",
    "Duplicate Tag": "复制标签",
    "Delete Tag": "删除标签",
    "Rename Tag": "重命名标签",
    "Show/Hide": "显示/隐藏",
    "Show/Hide all": "显示/隐藏全部",
    "Import into current project": "导入到当前项目",
    "Import into new project": "导入到新项目",
    "Open in new window": "在新窗口中打开",
    "Open in Main Window": "在主窗口中打开",
    "Open Window": "打开窗口",
    "New Window": "新建窗口",
    "Close Window": "关闭窗口",
    "Maximize": "最大化",
    "Minimize": "最小化",
    "Restore": "还原",
    "Move Up": "上移",
    "Move Down": "下移",
    "Bring Forward": "上移一层",
    "Send Backward": "下移一层",
    "Bring to Front": "置于顶层",
    "Send to Back": "置于底层",
    "Align Left": "左对齐",
    "Align Right": "右对齐",
    "Align Top": "顶部对齐",
    "Align Bottom": "底部对齐",
    "Align Center": "居中对齐",
    "Distribute Horizontally": "水平分布",
    "Distribute Vertically": "垂直分布",
    "Flip Horizontal": "水平翻转",
    "Flip Vertical": "垂直翻转",
    "Rotate 90": "旋转 90 度",
    "Rotate 180": "旋转 180 度",
    "Rotate 270": "旋转 270 度",
    "Reset Rotation": "重置旋转",
    "Reset Scale": "重置缩放",
    "Reset Position": "重置位置",
    "Lock Position": "锁定位置",
    "Lock Scale": "锁定缩放",
    "Lock Rotation": "锁定旋转",
    "Unlock All": "全部解锁",
    "Lock All": "全部锁定",
    "Layers": "图层",
    "Channels": "通道",
    "Masks": "蒙版",
    "Graph": "图",
    "Timeline": "时间线",
    "Properties": "属性",
    "Toolbar": "工具栏",
    "Status Bar": "状态栏",
    "Menu Bar": "菜单栏",
    "Title Bar": "标题栏",
    "Dock Area": "停靠区",
    "Viewport": "视口",
    "Canvas": "画布",
    "Node Graph": "节点图",
    "Curve Editor": "曲线编辑器",
    "Shelf": "架子",
    "Shelf Search": "架子搜索",
    "Presets": "预设",
    "Library": "库",
    "Asset": "资产",
    "Assets": "资产",
    "Resource": "资源",
    "Resources": "资源",
    "Folder": "文件夹",
    "Folders": "文件夹",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX11.items():
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
