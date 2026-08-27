#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第六十八批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX68 = {
    "Create": "创建",
    "Create New": "新建",
    "Create Project": "创建项目",
    "Create Image": "创建图像",
    "Create Channel": "创建通道",
    "Create Layer": "创建图层",
    "Create Group": "创建组",
    "Create Folder": "创建文件夹",
    "Create Material": "创建材质",
    "Create Texture": "创建纹理",
    "Create Object": "创建对象",
    "Create Geometry": "创建几何体",
    "Create Mesh": "创建网格",
    "Create Patch": "创建面片",
    "Create Preset": "创建预设",
    "Create Brush": "创建笔刷",
    "Create Camera": "创建相机",
    "Create Light": "创建灯光",
    "Create Render": "创建渲染",
    "Create Bake": "创建烘焙",
    "Create Filter": "创建滤镜",
    "Create Mask": "创建蒙版",
    "Create Selection": "创建选择",
    "Create Archive": "创建归档",
    "Create File": "创建文件",
    "Create Scene": "创建场景",
    "Create Node": "创建节点",
    "Create Shader": "创建着色器",
    "Create Tool": "创建工具",
    "Create Palettes": "创建面板",
    "Create Panel": "创建面板",
    "Create Tab": "创建标签页",
    "Create Workspace": "创建工作区",
    "Create Library": "创建库",
    "Create Asset": "创建资产",
    "Create Tag": "创建标签",
    "Create Shelf": "创建架子",
    "Create Empty": "创建空项目",
    "Create from": "从以下创建",
    "Create from Template": "从模板创建",
    "Create from Selection": "从选择创建",
    "Create from Image": "从图像创建",
    "Create from Layer": "从图层创建",
    "Create from Channel": "从通道创建",
    "Create from Mesh": "从网格创建",
    "Create from Object": "从对象创建",
    "Create from Path": "从路径创建",
    "Create from File": "从文件创建",
    "Create from Preset": "从预设创建",
    "Create as Copy": "创建为副本",
    "Create as New": "创建为新项目",
    "Create New Version": "创建新版本",
    "Create New Project": "创建新项目",
    "Create New Image": "创建新图像",
    "Create New Channel": "创建新通道",
    "Create New Layer": "创建新图层",
    "Create New Group": "创建新组",
    "Create New Folder": "创建新文件夹",
    "Create New Material": "创建新材质",
    "Create New Texture": "创建新纹理",
    "Create New Brush": "创建新笔刷",
    "Create New Camera": "创建新相机",
    "Create New Light": "创建新灯光",
    "Create New Render": "创建新渲染",
    "Create New Bake": "创建新烘焙",
    "Create New Filter": "创建新滤镜",
    "Create New Mask": "创建新蒙版",
    "Create New Scene": "创建新场景",
    "Create New Node": "创建新节点",
    "Create New Shader": "创建新着色器",
    "Create New Shelf": "创建新架子",
    "Create New Preset": "创建新预设",
    "Create New Tool": "创建新工具",
    "Create New Palette": "创建新面板",
    "Create New Panel": "创建新面板",
    "Create New Tab": "创建新标签页",
    "Create New Workspace": "创建工作区",
    "Create New Library": "创建新库",
    "Create New Asset": "创建新资产",
    "Create New Tag": "创建新标签",
    "Creating": "正在创建",
    "Creating Project": "正在创建项目",
    "Creating Image": "正在创建图像",
    "Creating Channel": "正在创建通道",
    "Creating Layer": "正在创建图层",
    "Creating Group": "正在创建组",
    "Creating Mesh": "正在创建网格",
    "Creating Material": "正在创建材质",
    "Creating Node": "正在创建节点",
    "Creating Shader": "正在创建着色器",
    "Created": "已创建",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX68.items():
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
