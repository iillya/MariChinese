#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第六十五批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX65 = {
    "Channel": "通道",
    "Channels": "通道",
    "Channel Settings": "通道设置",
    "Channel Options": "通道选项",
    "Channel Properties": "通道属性",
    "Channel Name": "通道名称",
    "Channel Type": "通道类型",
    "Channel Mode": "通道模式",
    "Channel Depth": "通道深度",
    "Channel Size": "通道大小",
    "Channel Resolution": "通道分辨率",
    "Channel Scale": "通道缩放",
    "Channel Offset": "通道偏移",
    "Channel Color Space": "通道颜色空间",
    "Channel Blend Mode": "通道混合模式",
    "Channel Opacity": "通道不透明度",
    "Channel Alpha": "通道 Alpha",
    "Channel Mask": "通道蒙版",
    "Channel Selection": "通道选择",
    "Channel List": "通道列表",
    "Channel Stack": "通道堆栈",
    "Channel Group": "通道组",
    "Channel Folder": "通道文件夹",
    "Channel Browser": "通道浏览器",
    "Channel Library": "通道库",
    "Channel Category": "通道类别",
    "Channel Preset": "通道预设",
    "Channel Preview": "通道预览",
    "Channel Solo": "通道独奏",
    "Channel Mute": "通道静音",
    "Channel Lock": "通道锁定",
    "Channel Hide": "通道隐藏",
    "Channel Show": "通道显示",
    "Channel Visible": "通道可见",
    "Channel Invisible": "通道不可见",
    "Channel Active": "通道活动",
    "Channel Inactive": "通道非活动",
    "Channel Current": "当前通道",
    "Channel Enabled": "通道已启用",
    "Channel Disabled": "通道已禁用",
    "Add Channel": "添加通道",
    "Remove Channel": "移除通道",
    "Delete Channel": "删除通道",
    "Duplicate Channel": "复制通道",
    "Rename Channel": "重命名通道",
    "Copy Channel": "复制通道",
    "Paste Channel": "粘贴通道",
    "Move Channel": "移动通道",
    "Reorder Channel": "重新排序通道",
    "Set Channel": "设置通道",
    "Reset Channel": "重置通道",
    "Clear Channel": "清除通道",
    "Flatten Channel": "展平通道",
    "Bake Channel": "烘焙通道",
    "Cache Channel": "缓存通道",
    "Uncache Channel": "取消缓存通道",
    "Convert Channel": "转换通道",
    "Create Channel": "创建通道",
    "Select Channel": "选择通道",
    "Deselect Channel": "取消选择通道",
    "Edit Channel": "编辑通道",
    "Save Channel": "保存通道",
    "Load Channel": "加载通道",
    "Export Channel": "导出通道",
    "Import Channel": "导入通道",
    "Insert Channel": "插入通道",
    "Show Channel": "显示通道",
    "Hide Channel": "隐藏通道",
    "Enable Channel": "启用通道",
    "Disable Channel": "禁用通道",
    "Lock Channel": "锁定通道",
    "Unlock Channel": "解锁通道",
    "Channel Sort": "通道排序",
    "Channel Search": "通道搜索",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX65.items():
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
