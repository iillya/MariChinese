#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第八十批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX80 = {
    "Search": "搜索",
    "Search Box": "搜索框",
    "Search Bar": "搜索栏",
    "Search Field": "搜索字段",
    "Search Query": "搜索查询",
    "Search Term": "搜索词",
    "Search Text": "搜索文本",
    "Search Keyword": "搜索关键词",
    "Search Results": "搜索结果",
    "Search Result": "搜索结果",
    "Search Hits": "搜索命中",
    "Search Count": "搜索数量",
    "Search Options": "搜索选项",
    "Search Settings": "搜索设置",
    "Search Mode": "搜索模式",
    "Search Type": "搜索类型",
    "Search Scope": "搜索范围",
    "Search Range": "搜索范围",
    "Search Filter": "搜索滤镜",
    "Search Sort": "搜索排序",
    "Search Order": "搜索顺序",
    "Search Direction": "搜索方向",
    "Search Case Sensitive": "区分大小写",
    "Case Sensitive": "区分大小写",
    "Case Insensitive": "不区分大小写",
    "Match Case": "匹配大小写",
    "Match Whole Word": "匹配整个单词",
    "Match Whole Words": "匹配整个单词",
    "Use Regex": "使用正则",
    "Regex": "正则表达式",
    "Regular Expression": "正则表达式",
    "Search Text": "搜索文本",
    "Search All": "搜索全部",
    "Search Selected": "搜索所选",
    "Search Here": "在此搜索",
    "Search Folder": "搜索文件夹",
    "Search Project": "搜索项目",
    "Search Library": "搜索库",
    "Search Files": "搜索文件",
    "Search Items": "搜索项目",
    "Search Tags": "搜索标签",
    "Search Layers": "搜索图层",
    "Search Channels": "搜索通道",
    "Search Images": "搜索图像",
    "Search Assets": "搜索资产",
    "Search Assets": "搜索资产",
    "Search Presets": "搜索预设",
    "Search Brushes": "搜索笔刷",
    "Search Materials": "搜索材质",
    "Search Textures": "搜索纹理",
    "Search Filter": "搜索滤镜",
    "Search Shaders": "搜索着色器",
    "Search Nodes": "搜索节点",
    "Search Commands": "搜索命令",
    "Look Up": "查找",
    "Look Up": "查找",
    "Replace": "替换",
    "Replace All": "全部替换",
    "Replace Text": "替换文本",
    "Replace With": "替换为",
    "Replace Found": "替换找到的",
    "Replace First": "替换第一个",
    "Replace Next": "替换下一个",
    "Replace Previous": "替换上一个",
    "Find Next": "查找下一个",
    "Find Previous": "查找上一个",
    "Find All": "查找全部",
    "Find and Replace": "查找并替换",
    "Find Text": "查找文本",
    "Find in": "在以下中查找",
    "Find in File": "在文件中查找",
    "Find in Folder": "在文件夹中查找",
    "Find in Project": "在项目中查找",
    "Find in Library": "在库中查找",
    "Find in Files": "在文件中查找",
    "Find in Selection": "在所选内容中查找",
    "Find in Page": "在页面中查找",
    "Find in Document": "在文档中查找",
    "Find Next": "查找下一个",
    "Find Previous": "查找上一个",
    "Find All": "查找全部",
    "Search and Replace": "搜索并替换",
    "Go to Search": "转到搜索",
    "Show Search": "显示搜索",
    "Hide Search": "隐藏搜索",
    "Clear Search": "清除搜索",
    "Reset Search": "重置搜索",
    "New Search": "新建搜索",
    "Rerun Search": "重新运行搜索",
    "Refine Search": "优化搜索",
    "Search Results Count": "搜索结果数量",
    "Search Complete": "搜索完成",
    "Search Failed": "搜索失败",
    "Searching": "正在搜索",
    "No Results Found": "未找到结果",
    "No Search Results": "没有搜索结果",
    "No Matches Found": "未找到匹配项",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX80.items():
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
