#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第六十九批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX69 = {
    "Open": "打开",
    "Open Project": "打开项目",
    "Open Image": "打开图像",
    "Open File": "打开文件",
    "Open Folder": "打开文件夹",
    "Open Channel": "打开通道",
    "Open Layer": "打开图层",
    "Open Material": "打开材质",
    "Open Texture": "打开纹理",
    "Open Object": "打开对象",
    "Open Geometry": "打开几何体",
    "Open Mesh": "打开网格",
    "Open Scene": "打开场景",
    "Open in": "在以下中打开",
    "Open in Viewport": "在视口中打开",
    "Open in Editor": "在编辑器中打开",
    "Open in Browser": "在浏览器中打开",
    "Open in New Window": "在新窗口中打开",
    "Open in New Tab": "在新标签页中打开",
    "Open Location": "打开位置",
    "Open Path": "打开路径",
    "Open Current": "打开当前",
    "Open Recent": "打开最近",
    "Open Recent Project": "打开最近项目",
    "Open Recent File": "打开最近文件",
    "Open Recent Image": "打开最近图像",
    "Open Recent Session": "打开最近会话",
    "Open As Copy": "以副本打开",
    "Open As New": "以新项目打开",
    "Open As Read-Only": "以只读打开",
    "Open With": "用以下方式打开",
    "Open With Default": "用默认方式打开",
    "Open Location in": "在以下中打开位置",
    "Opening": "正在打开",
    "Opening Project": "正在打开项目",
    "Opening Image": "正在打开图像",
    "Opening File": "正在打开文件",
    "Opening Scene": "正在打开场景",
    "Opened": "已打开",
    "Opened Successfully": "成功打开",
    "Opened Project": "已打开项目",
    "Recently Opened": "最近打开",
    "Open Items": "打开的项目",
    "Open Files": "打开的文件",
    "Open Documents": "打开的文档",
    "Open Windows": "打开的窗口",
    "Open Arrays": "打开的数组",
    "Open Set": "打开集合",
    "Open Batch": "打开批次",
    "Open Batch File": "打开批次文件",
    "Open Session": "打开会话",
    "Open Workspace": "打开工作区",
    "Open Library": "打开库",
    "Open Asset": "打开资产",
    "Open Preset": "打开预设",
    "Open Brush": "打开笔刷",
    "Open Camera": "打开相机",
    "Open Viewport": "打开视口",
    "Open Viewer": "打开查看器",
    "Open Panel": "打开面板",
    "Open Palette": "打开面板",
    "Open Tab": "打开标签页",
    "Open Archive": "打开归档",
    "Open Backup": "打开备份",
    "Open Cache": "打开缓存",
    "Open Config": "打开配置",
    "Open Settings": "打开设置",
    "Open Options": "打开选项",
    "Open Help": "打开帮助",
    "Open Documentation": "打开文档",
    "Open Examples": "打开示例",
    "Open Templates": "打开模板",
    "Open Download": "打开下载",
    "Open Log": "打开日志",
    "Open Log File": "打开日志文件",
    "Open Readme": "打开自述文件",
    "Open Release Notes": "打开发行说明",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX69.items():
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
