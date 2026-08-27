#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第七十二批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX72 = {
    "Remove": "移除",
    "Remove Selected": "移除所选",
    "Remove All": "全部移除",
    "Remove Item": "移除项目",
    "Remove Items": "移除项目",
    "Remove Layer": "移除图层",
    "Remove Channel": "移除通道",
    "Remove Image": "移除图像",
    "Remove Material": "移除材质",
    "Remove Texture": "移除纹理",
    "Remove Object": "移除对象",
    "Remove Geometry": "移除几何体",
    "Remove Mesh": "移除网格",
    "Remove Node": "移除节点",
    "Remove Shader": "移除着色器",
    "Remove Filter": "移除滤镜",
    "Remove Mask": "移除蒙版",
    "Remove Selection": "移除选择",
    "Remove Brush": "移除笔刷",
    "Remove Camera": "移除相机",
    "Remove Light": "移除灯光",
    "Remove Preset": "移除预设",
    "Remove Tab": "移除标签页",
    "Remove Panel": "移除面板",
    "Remove Palette": "移除面板",
    "Remove Tool": "移除工具",
    "Remove Shelf": "移除架子",
    "Remove Tag": "移除标签",
    "Remove Task": "移除任务",
    "Remove Job": "移除任务",
    "Remove Data": "移除数据",
    "Remove File": "移除文件",
    "Remove Folder": "移除文件夹",
    "Remove Directory": "移除目录",
    "Remove Documents": "移除文档",
    "Remove Assets": "移除资产",
    "Remove from": "从以下移除",
    "Remove from Project": "从项目移除",
    "Remove from Image": "从图像移除",
    "Remove from Layer": "从图层移除",
    "Remove from Channel": "从通道移除",
    "Remove from Material": "从材质移除",
    "Remove from Texture": "从纹理移除",
    "Remove from Object": "从对象移除",
    "Remove from Geometry": "从几何体移除",
    "Remove from Mesh": "从网格移除",
    "Remove from Node": "从节点移除",
    "Remove from Shader": "从着色器移除",
    "Remove from Filter": "从滤镜移除",
    "Remove from Mask": "从蒙版移除",
    "Remove from Selection": "从选择移除",
    "Remove from Group": "从组移除",
    "Remove from Folder": "从文件夹移除",
    "Remove from Library": "从库移除",
    "Remove from Shelf": "从架子移除",
    "Remove from Preset": "从预设移除",
    "Remove from Brush": "从笔刷移除",
    "Remove from Camera": "从相机移除",
    "Remove from Scene": "从场景移除",
    "Remove from Viewport": "从视口移除",
    "Remove from Viewer": "从查看器移除",
    "Remove from Stack": "从堆栈移除",
    "Remove from List": "从列表移除",
    "Remove from Array": "从数组移除",
    "Remove from Batch": "从批次移除",
    "Remove from Map": "从映射移除",
    "Remove from Render": "从渲染移除",
    "Remove from Bake": "从烘焙移除",
    "Remove from Workspace": "从工作区移除",
    "Remove from Menu": "从菜单移除",
    "Remove from Toolbar": "从工具栏移除",
    "Remove from Tab": "从标签页移除",
    "Remove from Panel": "从面板移除",
    "Remove from Palette": "从面板移除",
    "Remove from Tag": "从标签移除",
    "Removing": "正在移除",
    "Removed": "已移除",
    "Remove Complete": "移除完成",
    "Remove Failed": "移除失败",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX72.items():
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
