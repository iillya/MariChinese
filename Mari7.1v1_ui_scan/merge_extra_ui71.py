#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第七十一批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX71 = {
    "Add": "添加",
    "Add New": "新建",
    "Add New Item": "新建项目",
    "Add New Layer": "新建图层",
    "Add New Channel": "新建通道",
    "Add New Image": "新建图像",
    "Add New Material": "新建材质",
    "Add New Texture": "新建纹理",
    "Add New Object": "新建对象",
    "Add New Group": "新建组",
    "Add New Folder": "新建文件夹",
    "Add New Node": "新建节点",
    "Add New Shader": "新建着色器",
    "Add New Filter": "新建滤镜",
    "Add New Mask": "新建蒙版",
    "Add New Selection": "新建选择",
    "Add New Brush": "新建笔刷",
    "Add New Camera": "新建相机",
    "Add New Light": "新建灯光",
    "Add New Preset": "新建预设",
    "Add New Tab": "新建标签页",
    "Add New Panel": "新建面板",
    "Add New Palette": "新建面板",
    "Add New Tool": "新建工具",
    "Add New Shelf": "新建架子",
    "Add New Tag": "新建标签",
    "Add New Workspace": "新建工作区",
    "Add New Library": "新建库",
    "Add New Asset": "新建资产",
    "Add New Scene": "新建场景",
    "Add New Project": "新建项目",
    "Add New File": "新建文件",
    "Add New Folder Here": "在此新建文件夹",
    "Add New Group Here": "在此新建组",
    "Add New Layer Here": "在此新建图层",
    "Add New Channel Here": "在此新建通道",
    "Add Item Here": "在此添加项目",
    "Add Layer Here": "在此添加图层",
    "Add Channel Here": "在此添加通道",
    "Add Node Here": "在此添加节点",
    "Add to": "添加到",
    "Add to Project": "添加到项目",
    "Add to Image": "添加到图像",
    "Add to Layer": "添加到图层",
    "Add to Channel": "添加到通道",
    "Add to Material": "添加到材质",
    "Add to Texture": "添加到纹理",
    "Add to Object": "添加到对象",
    "Add to Group": "添加到组",
    "Add to Folder": "添加到文件夹",
    "Add to Node Graph": "添加到节点图",
    "Add to Shader": "添加到着色器",
    "Add to Filter": "添加到滤镜",
    "Add to Mask": "添加到蒙版",
    "Add to Selection": "添加到选择",
    "Add to Brush": "添加到笔刷",
    "Add to Camera": "添加到相机",
    "Add to Scene": "添加到场景",
    "Add to Library": "添加到库",
    "Add to Shelf": "添加到架子",
    "Add to Preset": "添加到预设",
    "Add to Assets": "添加到资产",
    "Add to Workspace": "添加到工作区",
    "Add to Render": "添加到渲染",
    "Add to Bake": "添加到烘焙",
    "Add to Tag": "添加到标签",
    "Add to Tab": "添加到标签页",
    "Add to Panel": "添加到面板",
    "Add to Palette": "添加到面板",
    "Add to Toolbar": "添加到工具栏",
    "Add to Menu": "添加到菜单",
    "Add to Viewport": "添加到视口",
    "Add to Viewer": "添加到查看器",
    "Add to Stack": "添加到堆栈",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX71.items():
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
