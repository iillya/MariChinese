#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第八十一批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX81 = {
    "Brush": "笔刷",
    "Brush Settings": "笔刷设置",
    "Brush Options": "笔刷选项",
    "Brush Properties": "笔刷属性",
    "Brush Name": "笔刷名称",
    "Brush Type": "笔刷类型",
    "Brush Mode": "笔刷模式",
    "Brush Size": "笔刷大小",
    "Brush Opacity": "笔刷不透明度",
    "Brush Flow": "笔刷流量",
    "Brush Hardness": "笔刷硬度",
    "Brush Softness": "笔刷柔和度",
    "Brush Spacing": "笔刷间距",
    "Brush Angle": "笔刷角度",
    "Brush Rotation": "笔刷旋转",
    "Brush Scale": "笔刷缩放",
    "Brush Aspect": "笔刷纵横比",
    "Brush Roundness": "笔刷圆度",
    "Brush Dither": "笔刷抖动",
    "Brush Jitter": "笔刷抖动",
    "Brush Tilt": "笔刷倾斜",
    "Brush Pressure": "笔刷压力",
    "Brush Velocity": "笔刷速度",
    "Brush Direction": "笔刷方向",
    "Brush Color": "笔刷颜色",
    "Brush Color Space": "笔刷颜色空间",
    "Brush Flow": "笔刷流量",
    "Brush Falloff": "笔刷衰减",
    "Brush Custom": "自定义笔刷",
    "Brush Default": "默认笔刷",
    "Brush Preset": "笔刷预设",
    "Brush Presets": "笔刷预设",
    "Brush Library": "笔刷库",
    "Brush Browser": "笔刷浏览器",
    "Brush List": "笔刷列表",
    "Brush Stack": "笔刷堆叠",
    "Brush Group": "笔刷组",
    "Brush Category": "笔刷类别",
    "Brush Pack": "笔刷包",
    "Brush Packaged": "笔刷已打包",
    "Brush Settings Panel": "笔刷设置面板",
    "Brush Settings Tab": "笔刷设置标签页",
    "Brush Preview": "笔刷预览",
    "Brush Preview Size": "笔刷预览大小",
    "Brush Preview Opacity": "笔刷预览不透明度",
    "Brush Cursor": "笔刷光标",
    "Brush Cursor Size": "笔刷光标大小",
    "Brush Cursor Color": "笔刷光标颜色",
    "Brush Cursor Opacity": "笔刷光标不透明度",
    "Brush Hint": "笔刷提示",
    "Brush Tip": "笔刷笔尖",
    "Brush Tip Settings": "笔刷笔尖设置",
    "Brush Tip Shape": "笔刷笔尖形状",
    "Brush Tip Size": "笔刷笔尖大小",
    "Brush Tip Angle": "笔刷笔尖角度",
    "Brush Tip Spacing": "笔刷笔尖间距",
    "Brush Stroke": "笔刷笔画",
    "Brush Stroke Settings": "笔刷笔画设置",
    "Brush Stroke Width": "笔画宽度",
    "Brush Stroke Opacity": "笔画不透明度",
    "Brush Stroke Flow": "笔画流量",
    "Brush Stroke Spacing": "笔画间距",
    "Brush Stroke Hardness": "笔画硬度",
    "Add Brush": "添加笔刷",
    "Remove Brush": "移除笔刷",
    "Delete Brush": "删除笔刷",
    "Rename Brush": "重命名笔刷",
    "Duplicate Brush": "复制笔刷",
    "Copy Brush": "复制笔刷",
    "Paste Brush": "粘贴笔刷",
    "Move Brush": "移动笔刷",
    "Edit Brush": "编辑笔刷",
    "Create Brush": "创建笔刷",
    "Select Brush": "选择笔刷",
    "Save Brush": "保存笔刷",
    "Load Brush": "加载笔刷",
    "Import Brush": "导入笔刷",
    "Export Brush": "导出笔刷",
    "Reset Brush": "重置笔刷",
    "Restore Brush": "还原笔刷",
    "Enable Brush": "启用笔刷",
    "Disable Brush": "禁用笔刷",
    "Show Brush": "显示笔刷",
    "Hide Brush": "隐藏笔刷",
    "Brush Size": "笔刷大小",
    "Brush Opacity": "笔刷不透明度",
    "Brush Flow": "笔刷流量",
    "Brush Hardness": "笔刷硬度",
    "Brush Spacing": "笔刷间距",
    "Brush Angle": "笔刷角度",
    "Brush Rotation": "笔刷旋转",
    "Brush Scale": "笔刷缩放",
    "Brush Jitter": "笔刷抖动",
    "Brush Shape": "笔刷形状",
    "Brush Roundness": "笔刷圆度",
    "Brush Orientation": "笔刷方向",
    "Brush Texture": "笔刷纹理",
    "Brush Dynamics": "笔刷动态",
    "Brush Dynamic": "笔刷动态",
    "Brush Wetness": "笔刷湿度",
    "Brush Mixing": "笔刷混合",
    "Brush Airbrush": "笔刷喷枪",
    "Brush Stamp": "笔刷印章",
    "Brush Clone": "笔刷克隆",
    "Brush Eraser": "笔刷橡皮擦",
    "Brush Smudge": "笔刷涂抹",
    "Brush Projects": "笔刷投影",
    "Brush Grain": "笔刷颗粒",
    "Brush Smoothing": "笔刷平滑",
    "Brush Stabilizer": "笔刷稳定器",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX81.items():
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
