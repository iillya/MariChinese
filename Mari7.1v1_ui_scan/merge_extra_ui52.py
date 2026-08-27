#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第五十二批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX52 = {
    "Display": "显示",
    "Display Settings": "显示设置",
    "Display Options": "显示选项",
    "Display Mode": "显示模式",
    "Display Color": "显示颜色",
    "Display Gamma": "显示伽马",
    "Display Resolution": "显示分辨率",
    "Display Scale": "显示缩放",
    "Display Brightness": "显示亮度",
    "Display Contrast": "显示对比度",
    "Display Contrast Adjustment": "显示对比度调整",
    "Display Size": "显示大小",
    "Display Area": "显示区域",
    "Display Region": "显示区域",
    "Display Border": "显示边框",
    "Display Frame": "显示边框",
    "Display Background": "显示背景",
    "Display Grid": "显示网格",
    "Display Rules": "显示规则",
    "Display Format": "显示格式",
    "Display Language": "显示语言",
    "Display Units": "显示单位",
    "Display Theme": "显示主题",
    "Display Update": "显示更新",
    "Display Refresh": "显示刷新",
    "Display Performance": "显示性能",
    "Display Quality": "显示质量",
    "Display Level": "显示级别",
    "Display Detail": "显示细节",
    "Display Layer": "显示图层",
    "Display Order": "显示顺序",
    "Display Items": "显示项目",
    "Display Value": "显示值",
    "Display Values": "显示值",
    "Display Properties": "显示属性",
    "Display Information": "显示信息",
    "Display Stats": "显示统计",
    "Display Metrics": "显示指标",
    "Show Display": "显示显示",
    "Hide Display": "隐藏显示",
    "Enable Display": "启用显示",
    "Disable Display": "禁用显示",
    "Toggle Display": "切换显示",
    "Display All": "全部显示",
    "Display None": "全部不显示",
    "Display Selected": "显示所选",
    "Display Only": "仅显示",
    "Display Only Selected": "仅显示所选",
    "Display Only Visible": "仅显示可见",
    "Display Only Active": "仅显示活动",
    "Display Filter": "显示滤镜",
    "Display Clamp": "显示钳制",
    "Display Color Space": "显示颜色空间",
    "Display Gamma Correction": "显示伽马校正",
    "Display Correction": "显示校正",
    "Display Rotation": "显示旋转",
    "Display Zoom": "显示缩放",
    "Display Fit": "显示适应",
    "Display Center": "显示居中",
    "Display Origin": "显示原点",
    "Display Cursor": "显示光标",
    "Display Selection": "显示选择",
    "Display Highlight": "显示高亮",
    "Display Overlay": "显示覆盖层",
    "Display Safe Area": "显示安全区域",
    "Display Guide": "显示参考线",
    "Display Axis": "显示坐标轴",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX52.items():
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
