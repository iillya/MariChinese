#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第六十二批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX62 = {
    "Panel": "面板",
    "Panels": "面板",
    "Palette": "面板",
    "Palettes": "面板",
    "Panel Settings": "面板设置",
    "Panel Options": "面板选项",
    "Panel Properties": "面板属性",
    "Panel Name": "面板名称",
    "Panel Title": "面板标题",
    "Panel Icon": "面板图标",
    "Panel Type": "面板类型",
    "Panel Mode": "面板模式",
    "Panel Size": "面板大小",
    "Panel Position": "面板位置",
    "Panel Layout": "面板布局",
    "Panel Group": "面板组",
    "Panel Tabs": "面板标签页",
    "Panel Tab": "面板标签页",
    "Panel Stack": "面板堆叠",
    "Panel Dock": "面板停靠",
    "Panel Float": "面板浮动",
    "Panel Show": "显示面板",
    "Panel Hide": "隐藏面板",
    "Panel Close": "关闭面板",
    "Panel Open": "打开面板",
    "Panel Reset": "重置面板",
    "Panel Restore": "还原面板",
    "Panel Maximize": "最大化面板",
    "Panel Minimize": "最小化面板",
    "Panel Collapse": "折叠面板",
    "Panel Expand": "展开面板",
    "Panel Scroll": "面板滚动",
    "Panel Scale": "面板缩放",
    "Panel Opacity": "面板不透明度",
    "Panel Background": "面板背景",
    "Panel Color": "面板颜色",
    "Panel Border": "面板边框",
    "Panel Padding": "面板内边距",
    "Panel Margin": "面板边距",
    "Panel Header": "面板标题栏",
    "Panel Footer": "面板页脚",
    "Panel Content": "面板内容",
    "Panel Area": "面板区域",
    "Panel Width": "面板宽度",
    "Panel Height": "面板高度",
    "Panel Visibility": "面板可见性",
    "Show Panel": "显示面板",
    "Hide Panel": "隐藏面板",
    "Open Panel": "打开面板",
    "Close Panel": "关闭面板",
    "Dock Panel": "停靠面板",
    "Undock Panel": "取消停靠面板",
    "Float Panel": "浮动面板",
    "Pin Panel": "固定面板",
    "Unpin Panel": "取消固定面板",
    "Reset Panels": "重置面板",
    "Restore Panels": "还原面板",
    "Close All Panels": "关闭所有面板",
    "Open All Panels": "打开所有面板",
    "Show All Panels": "显示所有面板",
    "Hide All Panels": "隐藏所有面板",
    "Float All Panels": "浮动所有面板",
    "Dock All Panels": "停靠所有面板",
    "Reset Panel Layout": "重置面板布局",
    "Save Panel Layout": "保存面板布局",
    "Load Panel Layout": "加载面板布局",
    "Customize Panels": "自定义面板",
    "Panel Settings Dialog": "面板设置对话框",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX62.items():
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
