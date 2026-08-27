#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第十四批：菜单/面板/设置/状态类界面词，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX14 = {
    "File": "文件",
    "Edit": "编辑",
    "View": "视图",
    "Layer": "图层",
    "Object": "对象",
    "Patch": "面片",
    "Geometry": "几何体",
    "Shader": "着色器",
    "Paint": "绘制",
    "Bake": "烘焙",
    "Image": "图像",
    "Textures": "纹理",
    "Tools": "工具",
    "Windows": "窗口",
    "Window": "窗口",
    "Help": "帮助",
    "File Menu": "文件菜单",
    "Edit Menu": "编辑菜单",
    "View Menu": "视图菜单",
    "Object Menu": "对象菜单",
    "Patch Menu": "面片菜单",
    "Layer Menu": "图层菜单",
    "Channel Menu": "通道菜单",
    "Shader Menu": "着色器菜单",
    "Paint Menu": "绘制菜单",
    "Geometry Menu": "几何体菜单",
    "Help Menu": "帮助菜单",
    "Window Menu": "窗口菜单",
    "Export Options": "导出选项",
    "Import Options": "导入选项",
    "Bake Options": "烘焙选项",
    "Render Options": "渲染选项",
    "Render Settings": "渲染设置",
    "Project Options": "项目选项",
    "Layer Options": "图层选项",
    "Channel Options": "通道选项",
    "Brush Options": "笔刷选项",
    "Camera Options": "相机选项",
    "View Options": "视图选项",
    "General Options": "常规选项",
    "Display Options": "显示选项",
    "Performance Options": "性能选项",
    "Color Options": "颜色选项",
    "Color Management Settings": "色彩管理设置",
    "Display Settings": "显示设置",
    "Input Settings": "输入设置",
    "Shortcut Settings": "快捷键设置",
    "License Settings": "许可证设置",
    "Plugins": "插件",
    "Plugin Manager": "插件管理器",
    "Extensions": "扩展",
    "Extensions Manager": "扩展管理器",
    "About": "关于",
    "About Mari": "关于 Mari",
    "Check for Updates": "检查更新",
    "Help Center": "帮助中心",
    "Documentation": "文档",
    "Release Notes": "发行说明",
    "Keyboard Shortcuts": "键盘快捷键",
    "Keyboard": "键盘",
    "Mouse": "鼠标",
    "Tablet": "数位板",
    "Pressure": "压力",
    "Tilt": "倾斜",
    "Rotation": "旋转",
    "Velocity": "速度",
    "Spacing": "间距",
    "Flow": "流量",
    "Hardness": "硬度",
    "Size": "大小",
    "Opacity": "不透明度",
    "Angle": "角度",
    "Scale": "缩放",
    "Mirroring": "镜像",
    "Alignment": "对齐",
    "Offset": "偏移",
    "Jitter": "抖动",
    "Smoothness": "平滑度",
    "Roundness": "圆度",
    "Rotation": "旋转",
    "Aspect": "纵横比",
    "Gather": "收集",
    "Cleanup": "清理",
    "Optimize": "优化",
    "Validate": "校验",
    "Verify": "验证",
    "Repair": "修复",
    "Rebuild": "重建",
    "Regenerate": "重新生成",
    "Refresh": "刷新",
    "Recalculate": "重新计算",
    "Recount": "重新统计",
    "Sync": "同步",
    "Compare": "比较",
    "Merge": "合并",
    "Flatten": "展平",
    "Convert": "转换",
    "Cache": "缓存",
    "Uncache": "取消缓存",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX14.items():
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
