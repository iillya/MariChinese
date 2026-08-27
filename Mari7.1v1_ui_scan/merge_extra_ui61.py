#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第六十一批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX61 = {
    "Tools": "工具",
    "Tool": "工具",
    "Toolbar": "工具栏",
    "Toolbars": "工具栏",
    "Tool Options": "工具选项",
    "Tool Settings": "工具设置",
    "Tool Properties": "工具属性",
    "Tool Parameter": "工具参数",
    "Tool Parameter Settings": "工具参数设置",
    "Tool Name": "工具名称",
    "Tool Type": "工具类型",
    "Tool Mode": "工具模式",
    "Tool Size": "工具大小",
    "Tool Color": "工具颜色",
    "Tool Opacity": "工具不透明度",
    "Tool Strength": "工具强度",
    "Tool Flow": "工具流量",
    "Tool Angle": "工具角度",
    "Tool Rotation": "工具旋转",
    "Tool Scale": "工具缩放",
    "Tool Preset": "工具预设",
    "Tool Tip": "工具提示",
    "Tool Shortcut": "工具快捷键",
    "Tool Help": "工具帮助",
    "Tool Description": "工具说明",
    "Tool History": "工具历史",
    "Tool Context": "工具上下文",
    "Tool Group": "工具组",
    "Tool Category": "工具类别",
    "Tool Palette": "工具面板",
    "Tool Manager": "工具管理器",
    "Tool Library": "工具库",
    "Active Tool": "活动工具",
    "Current Tool": "当前工具",
    "Previous Tool": "上一个工具",
    "Next Tool": "下一个工具",
    "Select Tool": "选择工具",
    "Paint Tool": "绘制工具",
    "Brush Tool": "笔刷工具",
    "Move Tool": "移动工具",
    "Rotate Tool": "旋转工具",
    "Scale Tool": "缩放工具",
    "Zoom Tool": "缩放工具",
    "Pan Tool": "平移工具",
    "Orbit Tool": "环绕工具",
    "Project Tool": "投影工具",
    "Fill Tool": "填充工具",
    "Erase Tool": "擦除工具",
    "Clone Tool": "克隆工具",
    "Smudge Tool": "涂抹工具",
    "Crop Tool": "裁剪工具",
    "Measure Tool": "测量工具",
    "Probe Tool": "探测工具",
    "Pick Tool": "拾取工具",
    "Eyedropper Tool": "吸管工具",
    "Color Picker Tool": "颜色选择器工具",
    "Sampler Tool": "采样工具",
    "View Tool": "视图工具",
    "Camera Tool": "相机工具",
    "Grab Tool": "抓取工具",
    "Marquee Tool": "选框工具",
    "Wand Tool": "魔棒工具",
    "Lasso Tool": "套索工具",
    "Selection Tool": "选择工具",
    "Add Tool": "添加工具",
    "Remove Tool": "移除工具",
    "Reset Tool": "重置工具",
    "Restore Tool": "还原工具",
    "Duplicate Tool": "复制工具",
    "Delete Tool": "删除工具",
    "Rename Tool": "重命名工具",
    "Edit Tool": "编辑工具",
    "Save Tool": "保存工具",
    "Load Tool": "加载工具",
    "Export Tool": "导出工具",
    "Import Tool": "导入工具",
    "Show Tool": "显示工具",
    "Hide Tool": "隐藏工具",
    "Enable Tool": "启用工具",
    "Disable Tool": "禁用工具",
    "Toggle Tool": "切换工具",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX61.items():
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
