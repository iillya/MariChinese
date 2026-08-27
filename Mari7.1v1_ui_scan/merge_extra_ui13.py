#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第十三批：工具/笔刷/合成/视图类界面词，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX13 = {
    "Smudge": "涂抹",
    "Sculpt": "雕刻",
    "Clone": "克隆",
    "Erase": "擦除",
    "Dodge": "减淡",
    "Burn": "加深",
    "Sharpen": "锐化",
    "Blur": "模糊",
    "Recompose": "重新合成",
    "Play Again": "再次播放",
    "Total": "总计",
    "No Layers": "无图层",
    "No channels": "无通道",
    "No images": "无图像",
    "No object": "无对象",
    "No paint": "无绘制",
    "No patches": "无面片",
    "No project": "无项目",
    "Generating Catalog": "正在生成目录",
    "Generating Custom Imagemaps": "正在生成自定义图像贴图",
    "Gather Scale": "收集缩放",
    "Gather Type": "收集类型",
    "Feature is active": "功能已启用",
    "Add Preset": "添加预设",
    "Remove Preset": "移除预设",
    "Save Preset": "保存预设",
    "Load Preset": "加载预设",
    "Apply Preset": "应用预设",
    "Reset Preset": "重置预设",
    "Preset Name": "预设名称",
    "New Preset": "新建预设",
    "Default Preset": "默认预设",
    "Layer Blend Mode": "图层混合模式",
    "Layer Opacity": "图层不透明度",
    "Layer Visibility": "图层可见性",
    "Channel Layer": "通道图层",
    "Paint Buffer": "绘制缓冲区",
    "Paint Mode": "绘制模式",
    "Paint Opacity": "绘制不透明度",
    "Bake Mode": "烘焙模式",
    "Bake Resolution": "烘焙分辨率",
    "Bake Point": "烘焙点",
    "Bake Active": "烘焙激活",
    "Projection": "投影",
    "Projection Type": "投影类型",
    "Projector": "投影器",
    "Projector Mode": "投影器模式",
    "View Mode": "视图模式",
    "View Transform": "视图变换",
    "Viewport Mode": "视口模式",
    "Camera View": "相机视图",
    "Top View": "顶视图",
    "Front View": "前视图",
    "Side View": "侧视图",
    "Perspective View": "透视视图",
    "Orthographic View": "正交视图",
    "Wireframe": "线框",
    "Shaded": "着色",
    "Textured": "纹理",
    "Solid": "实体",
    "Lighting": "灯光",
    "Shadows": "阴影",
    "Background": "背景",
    "Foreground": "前景",
    "Overlay": "覆盖层",
    "Grid Overlay": "网格覆盖层",
    "Safe Area": "安全区域",
    "Locked": "已锁定",
    "Unlocked": "已解锁",
    "Hidden": "已隐藏",
    "Muted": "已静音",
    "Solo": "独奏",
    "In Progress": "进行中",
    "Completed": "已完成",
    "Canceled": "已取消",
    "Pending": "待处理",
    "Failed": "失败",
    "Succeeded": "成功",
    "Available": "可用",
    "Unavailable": "不可用",
    "Optional": "可选",
    "Required": "必填",
    "Read Only": "只读",
    "Editable": "可编辑",
    "Modifiable": "可修改",
    "Hidden Items": "隐藏的项目",
    "Locked Items": "锁定的项目",
    "Selected Items": "选中的项目",
    "All Items": "所有项目",
    "Open Items": "打开的项目",
    "Recent Items": "最近的项目",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX13.items():
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
