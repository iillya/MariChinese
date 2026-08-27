#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第四十批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX40 = {
    "Rendering": "渲染中",
    "Rendered": "已渲染",
    "Render Layer": "渲染图层",
    "Render Channel": "渲染通道",
    "Render Pass": "渲染通道",
    "Render Result": "渲染结果",
    "Render Preview": "渲染预览",
    "Render Cache": "渲染缓存",
    "Render Time": "渲染时间",
    "Render Duration": "渲染时长",
    "Render Progress": "渲染进度",
    "Render Status": "渲染状态",
    "Render Settings": "渲染设置",
    "Render Options": "渲染选项",
    "Render Area": "渲染区域",
    "Render Region": "渲染区域",
    "Render View": "渲染视图",
    "Render Window": "渲染窗口",
    "Render Buffer": "渲染缓冲区",
    "Render Frame": "渲染帧",
    "Render Still": "渲染静帧",
    "Render Animation": "渲染动画",
    "Render Sequence": "渲染序列",
    "Render Time Range": "渲染时间范围",
    "Render Bounds": "渲染范围",
    "Render Output Path": "渲染输出路径",
    "Render Output Format": "渲染输出格式",
    "Render Output Size": "渲染输出大小",
    "Render Engine": "渲染引擎",
    "Render Device": "渲染设备",
    "Render Threads": "渲染线程",
    "Render CPU": "渲染 CPU",
    "Render GPU": "渲染 GPU",
    "Render Low": "低渲染",
    "Render Medium": "中渲染",
    "Render High": "高渲染",
    "Render Tiles": "渲染瓦片",
    "Render Bucket": "渲染桶",
    "Render Samples": "渲染采样",
    "Render Quality": "渲染质量",
    "Render Speed": "渲染速度",
    "Render In Background": "后台渲染",
    "Render On Save": "保存时渲染",
    "Quick Render": "快速渲染",
    "Final Render": "最终渲染",
    "Preview Render": "预览渲染",
    "Bake Render": "烘焙渲染",
    "Render Statistics": "渲染统计",
    "Render Stats": "渲染统计",
    "Render Info": "渲染信息",
    "Render Log": "渲染日志",
    "Render Debug": "渲染调试",
    "Render Cleanup": "渲染清理",
    "Cancel Render": "取消渲染",
    "Abort Render": "中止渲染",
    "Restart Render": "重新渲染",
    "Resume Render": "继续渲染",
    "Pause Render": "暂停渲染",
    "Render Complete": "渲染完成",
    "Render Failed": "渲染失败",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX40.items():
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
