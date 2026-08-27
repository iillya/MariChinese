#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第二十五批：操作面板/常用短语补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX25 = {
    "Panel": "面板",
    "Tool Panel": "工具面板",
    "Layers Panel": "图层面板",
    "Channels Panel": "通道面板",
    "Masks Panel": "蒙版面板",
    "Shader Panel": "着色器面板",
    "Node Graph Panel": "节点图面板",
    "Project Panel": "项目面板",
    "Image Panel": "图像面板",
    "Properties Panel": "属性面板",
    "Attribute Panel": "属性面板",
    "Details Panel": "详情面板",
    "Preview Panel": "预览面板",
    "Viewport Panel": "视口面板",
    "Color Panel": "颜色面板",
    "Brush Panel": "笔刷面板",
    "Tools Panel": "工具面板",
    "Shelf Panel": "架子面板",
    "Library Panel": "库面板",
    "History Panel": "历史面板",
    "Timeline Panel": "时间线面板",
    "Curve Panel": "曲线面板",
    "Export Panel": "导出面板",
    "Import Panel": "导入面板",
    "Render Panel": "渲染面板",
    "Bake Panel": "烘焙面板",
    "Settings Panel": "设置面板",
    "Options Panel": "选项面板",
    "Info Panel": "信息面板",
    "Log Panel": "日志面板",
    "Console Panel": "控制台面板",
    "Icons": "图标",
    "Icon": "图标",
    "Spacing": "间距",
    "Alignment": "对齐",
    "Orientation": "方向",
    "Position": "位置",
    "Rotation": "旋转",
    "Scale": "缩放",
    "Transformation": "变换",
    "Show Tools": "显示工具",
    "Hide Tools": "隐藏工具",
    "Show Viewport": "显示视口",
    "Hide Viewport": "隐藏视口",
    "Show Project": "显示项目",
    "Hide Project": "隐藏项目",
    "Show Panels": "显示面板",
    "Hide Panels": "隐藏面板",
    "Restore Panels": "还原面板",
    "Reset Layout": "重置布局",
    "Save Layout": "保存布局",
    "Load Layout": "加载布局",
    "Delete Layout": "删除布局",
    "Arrange": "排列",
    "Arrange Panels": "排列面板",
    "Dock Panel": "停靠面板",
    "Undock Panel": "取消停靠面板",
    "Float Panel": "浮动面板",
    "Close Panel": "关闭面板",
    "Open Panel": "打开面板",
    "Resize Panel": "调整面板大小",
    "Collapse Panel": "折叠面板",
    "Expand Panel": "展开面板",
    "Maximize Panel": "最大化面板",
    "Minimize Panel": "最小化面板",
    "Panel Settings": "面板设置",
    "Show Panel Options": "显示面板选项",
    "Hide Panel Options": "隐藏面板选项",
    "Docking": "停靠",
    "Floating": "浮动",
    "Locked Panel": "锁定面板",
    "Unlocked Panel": "解锁面板",
    "Panel Tabs": "面板标签页",
    "Panel View": "面板视图",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX25.items():
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
        print("已存在跳过: 部分")


if __name__ == "__main__":
    main()
