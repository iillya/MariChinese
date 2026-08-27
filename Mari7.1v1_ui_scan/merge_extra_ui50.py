#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第五十批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX50 = {
    "Convert": "转换",
    "Convert To": "转换为",
    "Convert Layer": "转换图层",
    "Convert Channel": "转换通道",
    "Convert Image": "转换图像",
    "Convert Color Space": "转换颜色空间",
    "Convert Data": "转换数据",
    "Convert to Paintable": "转换为可绘制",
    "Convert to Material": "转换为材质",
    "Convert to Shader": "转换为着色器",
    "Convert to Procedural": "转换为程序化",
    "Convert to Mask": "转换为蒙版",
    "Convert to Normal Map": "转换为法线贴图",
    "Convert to Displacement": "转换为置换贴图",
    "Convert to Height Map": "转换为高度贴图",
    "Convert to Diffuse": "转换为漫反射",
    "Convert to Specular": "转换为高光",
    "Convert to Roughness": "转换为粗糙度",
    "Convert to Metallic": "转换为金属度",
    "Convert to Opacity": "转换为不透明度",
    "Convert to Alpha": "转换为 Alpha",
    "Convert Selection": "转换选择",
    "Convert to Selection": "转换为选择",
    "Selection to Mask": "选择转蒙版",
    "Mask to Selection": "蒙版转选择",
    "Convert to Mesh": "转换为网格",
    "Convert to Patches": "转换为面片",
    "Convert to Geometry": "转换为几何体",
    "Convert to Object": "转换为对象",
    "Convert to Image Set": "转换为图像集",
    "Convert to Tiled": "转换为平铺",
    "Convert to Non-Tiled": "转换为非平铺",
    "Convert to Ptex": "转换为 Ptex",
    "Convert to Dense": "转换为稠密",
    "Convert to Raw": "转换为原始数据",
    "Convert to Float": "转换为浮点",
    "Convert to Half": "转换为半精度",
    "Convert to Byte": "转换为字节",
    "Convert to 8-bit": "转换为 8 位",
    "Convert to 16-bit": "转换为 16 位",
    "Convert to 32-bit": "转换为 32 位",
    "Convert Colors": "转换颜色",
    "Convert Layers": "转换图层",
    "Convert Channels": "转换通道",
    "Convert All": "全部转换",
    "Convert Selected": "转换所选",
    "Convert on Bake": "烘焙时转换",
    "Convert on Export": "导出时转换",
    "Convert on Import": "导入时转换",
    "Convert Options": "转换选项",
    "Convert Settings": "转换设置",
    "Convert Mode": "转换模式",
    "Convert Result": "转换结果",
    "Conversion Complete": "转换完成",
    "Conversion Failed": "转换失败",
    "Conversion Cancelled": "转换已取消",
    "Conversion in Progress": "转换进行中",
    "Conversion Type": "转换类型",
    "Conversion Settings": "转换设置",
    "Conversion Details": "转换详情",
    "Conversion Options": "转换选项",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX50.items():
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
