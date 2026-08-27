#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第三十九批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX39 = {
    "New File": "新建文件",
    "New Image": "新建图像",
    "New Channel": "新建通道",
    "New Layer": "新建图层",
    "New Group": "新建组",
    "New Folder": "新建文件夹",
    "New Shelf": "新建架子",
    "New Preset": "新建预设",
    "New Viewport": "新建视口",
    "New Tab": "新建标签页",
    "New Window": "新建窗口",
    "New Workspace": "新建工作区",
    "New Library": "新建库",
    "New Asset": "新建资产",
    "New Material": "新建材质",
    "New Brush": "新建笔刷",
    "New Camera": "新建相机",
    "New Light": "新建灯光",
    "New Scene": "新建场景",
    "New Archive": "新建归档",
    "New Item": "新建项目",
    "New Selection": "新建选择",
    "New Set": "新建集合",
    "Add Item": "添加项目",
    "Add Image": "添加图像",
    "Add File": "添加文件",
    "Add Folder": "添加文件夹",
    "Add Group": "添加组",
    "Add Tag": "添加标签",
    "Add Tag To": "向以下对象添加标签",
    "Remove Tag": "移除标签",
    "Remove Tags": "移除标签",
    "Create Tag": "创建标签",
    "Edit Tag": "编辑标签",
    "Delete Tag": "删除标签",
    "Rename Tag": "重命名标签",
    "Apply Tag": "应用标签",
    "Filter Tag": "筛选标签",
    "Tag Name": "标签名称",
    "Tag Color": "标签颜色",
    "Tag Description": "标签说明",
    "All Tags": "所有标签",
    "No Tags": "无标签",
    "Untagged": "未标记",
    "Tagged": "已标记",
    "Add Tags": "添加标签",
    "Edit Tags": "编辑标签",
    "Clear Tags": "清除标签",
    "Show Tags": "显示标签",
    "Hide Tags": "隐藏标签",
    "Filter by Tags": "按标签筛选",
    "Search Tags": "搜索标签",
    "Select by Tags": "按标签选择",
    "Tags Applied": "已应用标签",
    "Remove All Tags": "移除所有标签",
    "Remove Empty Tags": "移除空标签",
    "Rename Tag To": "将标签重命名为",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX39.items():
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
