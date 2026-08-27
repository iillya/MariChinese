#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第七十四批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX74 = {
    "Preview": "预览",
    "Preview Mode": "预览模式",
    "Preview On": "预览开启",
    "Preview Off": "预览关闭",
    "Preview All": "全部预览",
    "Preview Selected": "预览所选",
    "Preview In": "在以下中预览",
    "Preview In Viewport": "在视口中预览",
    "Preview In Viewer": "在查看器中预览",
    "Preview In Editor": "在编辑器中预览",
    "Preview In Browser": "在浏览器中预览",
    "Preview In Window": "在窗口中预览",
    "Preview Image": "预览图像",
    "Preview Result": "预览结果",
    "Preview Output": "预览输出",
    "Preview Layer": "预览图层",
    "Preview Channel": "预览通道",
    "Preview Mask": "预览蒙版",
    "Preview Filter": "预览滤镜",
    "Preview Shader": "预览着色器",
    "Preview Material": "预览材质",
    "Preview Texture": "预览纹理",
    "Preview Object": "预览对象",
    "Preview Geometry": "预览几何体",
    "Preview Mesh": "预览网格",
    "Preview Brush": "预览笔刷",
    "Preview Preset": "预览预设",
    "Preview Camera": "预览相机",
    "Preview Light": "预览灯光",
    "Preview Render": "预览渲染",
    "Preview Bake": "预览烘焙",
    "Preview Settings": "预览设置",
    "Preview Options": "预览选项",
    "Preview Properties": "预览属性",
    "Preview Size": "预览大小",
    "Preview Resolution": "预览分辨率",
    "Preview Scale": "预览缩放",
    "Preview Zoom": "预览缩放",
    "Preview Opacity": "预览不透明度",
    "Preview Quality": "预览质量",
    "Preview Time": "预览时间",
    "Preview Frame": "预览帧",
    "Preview Range": "预览范围",
    "Preview Region": "预览区域",
    "Preview Area": "预览区域",
    "Preview Bounds": "预览范围",
    "Preview Extent": "预览范围",
    "Preview Update": "预览更新",
    "Preview Auto": "自动预览",
    "Preview Manual": "手动预览",
    "Preview Refresh": "刷新预览",
    "Preview Generate": "生成预览",
    "Preview Update On": "预览自动更新",
    "Preview Update Off": "关闭预览自动更新",
    "Enable Preview": "启用预览",
    "Disable Preview": "禁用预览",
    "Toggle Preview": "切换预览",
    "Show Preview": "显示预览",
    "Hide Preview": "隐藏预览",
    "Cancel Preview": "取消预览",
    "Stop Preview": "停止预览",
    "Start Preview": "开始预览",
    "Play Preview": "播放预览",
    "Pause Preview": "暂停预览",
    "Refresh Preview": "刷新预览",
    "Generate Preview": "生成预览",
    "Update Preview": "更新预览",
    "Preview Complete": "预览完成",
    "Preview Failed": "预览失败",
    "Preview in Progress": "预览进行中",
    "Preview Ready": "预览就绪",
    "Previewing": "正在预览",
    "Preview Panel": "预览面板",
    "Preview Window": "预览窗口",
    "Preview Viewport": "预览视口",
    "Preview Viewer": "预览查看器",
    "Preview Tab": "预览标签页",
    "Preview Tools": "预览工具",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX74.items():
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
