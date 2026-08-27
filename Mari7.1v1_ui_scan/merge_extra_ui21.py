#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第二十一批：相机/灯光/渲染/材质/导入导出类界面词，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX21 = {
    "Camera Settings": "相机设置",
    "Camera Properties": "相机属性",
    "Camera Name": "相机名称",
    "Camera Type": "相机类型",
    "Camera Position": "相机位置",
    "Camera Rotation": "相机旋转",
    "Camera Target": "相机目标",
    "Camera Focal Length": "相机焦距",
    "Camera Field of View": "相机视野",
    "Camera Near": "相机近裁剪",
    "Camera Far": "相机远裁剪",
    "Camera Clip": "相机裁剪",
    "New Camera": "新建相机",
    "Add Camera": "添加相机",
    "Remove Camera": "移除相机",
    "Set Camera": "设置相机",
    "Reset Camera": "重置相机",
    "Camera View": "相机视图",
    "Lighting Settings": "灯光设置",
    "Light Settings": "灯光设置",
    "Light Properties": "灯光属性",
    "Light Name": "灯光名称",
    "Light Type": "灯光类型",
    "Light Color": "灯光颜色",
    "Light Intensity": "灯光强度",
    "Light Temperature": "灯光色温",
    "Light Angle": "灯光角度",
    "Light Radius": "灯光半径",
    "Light Falloff": "灯光衰减",
    "Add Light": "添加灯光",
    "Remove Light": "移除灯光",
    "New Light": "新建灯光",
    "Environment Light": "环境灯光",
    "Environment Map": "环境贴图",
    "Environment Settings": "环境设置",
    "Environment Intensity": "环境强度",
    "Environment Rotation": "环境旋转",
    "Show Environment": "显示环境",
    "Hide Environment": "隐藏环境",
    "Render Settings": "渲染设置",
    "Render Engine": "渲染引擎",
    "Render Device": "渲染设备",
    "Render Resolution": "渲染分辨率",
    "Render Samples": "渲染采样数",
    "Render Quality": "渲染质量",
    "Render Mode": "渲染模式",
    "Render Time": "渲染时间",
    "Render Progress": "渲染进度",
    "Render Output": "渲染输出",
    "Render Path": "渲染路径",
    "Render Frame": "渲染帧",
    "Material": "材质",
    "Material Settings": "材质设置",
    "Material Properties": "材质属性",
    "Material Name": "材质名称",
    "Material Type": "材质类型",
    "Material Color": "材质颜色",
    "Material Preview": "材质预览",
    "New Material": "新建材质",
    "Create Material": "创建材质",
    "Edit Material": "编辑材质",
    "Delete Material": "删除材质",
    "Duplicate Material": "复制材质",
    "Material Library": "材质库",
    "Export Material": "导出材质",
    "Import Material": "导入材质",
    "Texture Settings": "纹理设置",
    "Texture Properties": "纹理属性",
    "Texture Preview": "纹理预览",
    "Texture Size": "纹理大小",
    "Texture Format": "纹理格式",
    "Texture Filtering": "纹理过滤",
    "Texture Wrap": "纹理循环",
    "Import Settings": "导入设置",
    "Export Settings": "导出设置",
    "Import Path": "导入路径",
    "Export Path": "导出路径",
    "Import Format": "导入格式",
    "Export Format": "导出格式",
    "Import Scale": "导入缩放",
    "Export Scale": "导出缩放",
    "Import Options": "导入选项",
    "Export Options": "导出选项",
    "Import All": "全部导入",
    "Export All": "全部导出",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX21.items():
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
