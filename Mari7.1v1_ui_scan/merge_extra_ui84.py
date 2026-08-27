#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第八十四批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX84 = {
    "Render": "渲染",
    "Rendering": "渲染中",
    "Renderer": "渲染器",
    "Render Now": "立即渲染",
    "Render Again": "重新渲染",
    "Render Preview": "渲染预览",
    "Render Final": "最终渲染",
    "Render Quick": "快速渲染",
    "Render Viewport": "渲染视口",
    "Render Window": "渲染窗口",
    "Render Panel": "渲染面板",
    "Render Tab": "渲染标签页",
    "Render Pass": "渲染通道",
    "Render Passes": "渲染通道",
    "Render Channel": "渲染通道",
    "Render Output": "渲染输出",
    "Render Result": "渲染结果",
    "Render Frame": "渲染帧",
    "Render Sequence": "渲染序列",
    "Render Still": "渲染静帧",
    "Render Animation": "渲染动画",
    "Render Range": "渲染范围",
    "Render Time": "渲染时间",
    "Render Duration": "渲染时长",
    "Render Progress": "渲染进度",
    "Render Status": "渲染状态",
    "Render State": "渲染状态",
    "Render Settings": "渲染设置",
    "Render Options": "渲染选项",
    "Render Properties": "渲染属性",
    "Render Engine": "渲染引擎",
    "Render Device": "渲染设备",
    "Render CPU": "渲染 CPU",
    "Render GPU": "渲染 GPU",
    "Render Samples": "渲染采样",
    "Render Quality": "渲染质量",
    "Render Speed": "渲染速度",
    "Render Resolution": "渲染分辨率",
    "Render Size": "渲染大小",
    "Render Scale": "渲染缩放",
    "Render Threads": "渲染线程",
    "Render Bucket": "渲染桶",
    "Render Tile": "渲染瓦片",
    "Render Tiles": "渲染瓦片",
    "Render Pass": "渲染通道",
    "Render Grain": "渲染颗粒",
    "Render Denoise": "渲染降噪",
    "Render In Background": "后台渲染",
    "Render On Save": "保存时渲染",
    "Render On Export": "导出时渲染",
    "Render In Progress": "渲染进行中",
    "Render Complete": "渲染完成",
    "Render Failed": "渲染失败",
    "Render Cancelled": "渲染已取消",
    "Render Success": "渲染成功",
    "Render Error": "渲染错误",
    "Render Warning": "渲染警告",
    "Render Stats": "渲染统计",
    "Render Statistics": "渲染统计",
    "Render Info": "渲染信息",
    "Render Details": "渲染详情",
    "Render Summary": "渲染摘要",
    "Render Log": "渲染日志",
    "Render Cache": "渲染缓存",
    "Render Cache Clear": "清除渲染缓存",
    "Render Cache Size": "渲染缓存大小",
    "Render Debug": "渲染调试",
    "Render Simulate": "渲染模拟",
    "Render Output Path": "渲染输出路径",
    "Render Output File": "渲染输出文件",
    "Render Output Folder": "渲染输出文件夹",
    "Render Output Format": "渲染输出格式",
    "Render Output Size": "渲染输出大小",
    "Render Output Scale": "渲染输出缩放",
    "Render Output Name": "渲染输出名称",
    "Render Output Type": "渲染输出类型",
    "Render Output Resolution": "渲染输出分辨率",
    "Render Output Color Space": "渲染输出颜色空间",
    "Render Output Settings": "渲染输出设置",
    "Render Output Options": "渲染输出选项",
    "Render Setup": "渲染设置",
    "Render Setup Dialog": "渲染设置对话框",
    "Render Setup Panel": "渲染设置面板",
    "Render Setup Tab": "渲染设置标签页",
    "Render Configuration": "渲染配置",
    "Render Config": "渲染配置",
    "Render Config File": "渲染配置文件",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX84.items():
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
