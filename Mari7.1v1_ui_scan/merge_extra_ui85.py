#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第八十五批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX85 = {
    "Bake": "烘焙",
    "Baking": "烘焙中",
    "Bake Now": "立即烘焙",
    "Bake Selected": "烘焙所选",
    "Bake All": "全部烘焙",
    "Bake Layer": "烘焙图层",
    "Bake Channel": "烘焙通道",
    "Bake Point": "烘焙点",
    "Bake Result": "烘焙结果",
    "Bake Output": "烘焙输出",
    "Bake Settings": "烘焙设置",
    "Bake Options": "烘焙选项",
    "Bake Properties": "烘焙属性",
    "Bake Type": "烘焙类型",
    "Bake Mode": "烘焙模式",
    "Bake Resolution": "烘焙分辨率",
    "Bake Size": "烘焙大小",
    "Bake Scale": "烘焙缩放",
    "Bake Offset": "烘焙偏移",
    "Bake Padding": "烘焙内边距",
    "Bake Margin": "烘焙边距",
    "Bake Bleed": "烘焙渗色",
    "Bake Dither": "烘焙抖动",
    "Bake Quality": "烘焙质量",
    "Bake Samples": "烘焙采样",
    "Bake Tile": "烘焙瓦片",
    "Bake Tiles": "烘焙瓦片",
    "Bake Bucket": "烘焙桶",
    "Bake In Background": "后台烘焙",
    "Bake In Progress": "烘焙进行中",
    "Bake Complete": "烘焙完成",
    "Bake Failed": "烘焙失败",
    "Bake Cancelled": "烘焙已取消",
    "Bake Success": "烘焙成功",
    "Bake Error": "烘焙错误",
    "Bake Warning": "烘焙警告",
    "Bake Stats": "烘焙统计",
    "Bake Duration": "烘焙时长",
    "Bake Time": "烘焙时间",
    "Bake Progress": "烘焙进度",
    "Bake Status": "烘焙状态",
    "Bake Output Path": "烘焙输出路径",
    "Bake Output File": "烘焙输出文件",
    "Bake Output Format": "烘焙输出格式",
    "Bake Output Size": "烘焙输出大小",
    "Bake Output Color Space": "烘焙输出颜色空间",
    "Bake Output Resolution": "烘焙输出分辨率",
    "Bake On": "烘焙开启",
    "Bake Off": "烘焙关闭",
    "Bake Setup": "烘焙设置",
    "Bake Setup Panel": "烘焙设置面板",
    "Bake Setup Tab": "烘焙设置标签页",
    "Bake Configuration": "烘焙配置",
    "Bake Config": "烘焙配置",
    "Bake Preview": "烘焙预览",
    "Bake Preview Size": "烘焙预览大小",
    "Bake Preview Quality": "烘焙预览质量",
    "Bake Clear": "清除烘焙",
    "Clear Bake": "清除烘焙",
    "Cancel Bake": "取消烘焙",
    "Stop Bake": "停止烘焙",
    "Restart Bake": "重新烘焙",
    "Resume Bake": "继续烘焙",
    "Pause Bake": "暂停烘焙",
    "Start Bake": "开始烘焙",
    "Bake Refresh": "刷新烘焙",
    "Bake Update": "更新烘焙",
    "Bake Cache": "烘焙缓存",
    "Bake Cache Clear": "清除烘焙缓存",
    "Bake Cache Size": "烘焙缓存大小",
    "Bake Type Diffuse": "烘焙类型：漫反射",
    "Bake Type Normal": "烘焙类型：法线",
    "Bake Type Ambient Occlusion": "烘焙类型：环境光遮蔽",
    "Bake Type Specular": "烘焙类型：高光",
    "Bake Type Roughness": "烘焙类型：粗糙度",
    "Bake Type Metallic": "烘焙类型：金属度",
    "Bake Type Displacement": "烘焙类型：置换",
    "Bake Type Height": "烘焙类型：高度",
    "Bake Type Id": "烘焙类型：ID",
    "Bake Type Curvature": "烘焙类型：曲率",
    "Bake Type Thickness": "烘焙类型：厚度",
    "Bake Type Emission": "烘焙类型：自发光",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX85.items():
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
