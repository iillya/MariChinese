#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第二十八批：纹理/贴图/图像处理补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX28 = {
    "Texture Map": "纹理贴图",
    "Diffuse": "漫反射",
    "Diffuse Map": "漫反射贴图",
    "Albedo": "反照率",
    "Albedo Map": "反照率贴图",
    "Base Color": "基础颜色",
    "Base Color Map": "基础颜色贴图",
    "Normal": "法线",
    "Normal Map": "法线贴图",
    "Normal Strength": "法线强度",
    "Bump": "凹凸",
    "Bump Map": "凹凸贴图",
    "Bump Strength": "凹凸强度",
    "Specular": "高光",
    "Specular Map": "高光贴图",
    "Roughness": "粗糙度",
    "Roughness Map": "粗糙度贴图",
    "Metallic": "金属度",
    "Metallic Map": "金属度贴图",
    "Metalness": "金属度",
    "Metalness Map": "金属度贴图",
    "Glossiness": "光泽度",
    "Glossiness Map": "光泽度贴图",
    "Opacity": "不透明度",
    "Opacity Map": "不透明度贴图",
    "Transparency": "透明",
    "Transparency Map": "透明贴图",
    "Transmission": "透射",
    "Transmission Map": "透射贴图",
    "Emission": "自发光",
    "Emission Map": "自发光贴图",
    "Emissive": "自发光",
    "Emissive Map": "自发光贴图",
    "Displacement": "置换",
    "Displacement Map": "置换贴图",
    "Height": "高度",
    "Height Map": "高度贴图",
    "Ambient Occlusion": "环境光遮蔽",
    "Ambient Occlusion Map": "环境光遮蔽贴图",
    "AO": "AO",
    "AO Map": "AO 贴图",
    "Mask Map": "蒙版贴图",
    "ID Map": "ID 贴图",
    "Curvature": "曲率",
    "Curvature Map": "曲率贴图",
    "Thickness": "厚度",
    "Thickness Map": "厚度贴图",
    "Subsurface": "次表面",
    "Subsurface Map": "次表面贴图",
    "Reflection": "反射",
    "Reflection Map": "反射贴图",
    "Refraction": "折射",
    "Refraction Map": "折射贴图",
    "Cavity": "凹痕",
    "Cavity Map": "凹痕贴图",
    "Color Map": "颜色贴图",
    "PBR": "PBR",
    "PBR Map": "PBR 贴图",
    "Painter": "绘色",
    "Texel Density": "纹理元素密度",
    "Texture Density": "纹理密度",
    "Texture Quality": "纹理质量",
    "Texture Preview": "纹理预览",
    "Downsample": "降采样",
    "Upsample": "升采样",
    "Extend": "扩展",
    "Wrap": "循环",
    "Clamp": "钳制",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX28.items():
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
