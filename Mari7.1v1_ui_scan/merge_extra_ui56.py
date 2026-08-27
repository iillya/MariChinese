#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第五十六批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX56 = {
    "New": "新建",
    "Create": "创建",
    "Add": "添加",
    "Edit": "编辑",
    "Delete": "删除",
    "Remove": "移除",
    "Rename": "重命名",
    "Copy": "复制",
    "Duplicate": "复制",
    "Move": "移动",
    "Select": "选择",
    "Open": "打开",
    "Close": "关闭",
    "Save": "保存",
    "Load": "加载",
    "Import": "导入",
    "Export": "导出",
    "Convert": "转换",
    "Apply": "应用",
    "Reset": "重置",
    "Undo": "撤销",
    "Redo": "重做",
    "Refresh": "刷新",
    "Update": "更新",
    "Change": "更改",
    "Modify": "修改",
    "Adjust": "调整",
    "Set": "设置",
    "Enable": "启用",
    "Disable": "禁用",
    "Show": "显示",
    "Hide": "隐藏",
    "Lock": "锁定",
    "Unlock": "解锁",
    "Clear": "清除",
    "Cancel": "取消",
    "Confirm": "确认",
    "Accept": "接受",
    "Reject": "拒绝",
    "Skip": "跳过",
    "Retry": "重试",
    "Abort": "中止",
    "Ignore": "忽略",
    "Cancel All": "全部取消",
    "Clear All": "全部清除",
    "Apply All": "全部应用",
    "Remove All": "全部移除",
    "Delete All": "全部删除",
    "Select All": "全选",
    "Deselect All": "取消全选",
    "Show All": "全部显示",
    "Hide All": "全部隐藏",
    "Enable All": "全部启用",
    "Disable All": "全部禁用",
    "Lock All": "全部锁定",
    "Unlock All": "全部解锁",
    "Expand All": "全部展开",
    "Collapse All": "全部折叠",
    "Reset All": "全部重置",
    "Restore All": "全部还原",
    "Update All": "全部更新",
    "Refresh All": "全部刷新",
    "Change All": "全部更改",
    "Convert All": "全部转换",
    "Export All": "全部导出",
    "Import All": "全部导入",
    "Save All": "全部保存",
    "Load All": "全部加载",
    "Apply to All": "应用到全部",
    "Apply to Selected": "应用到所选",
    "Apply to Others": "应用到其他",
    "Apply to Matching": "应用到匹配项",
    "Apply to All Items": "应用到所有项目",
    "Apply to All Layers": "应用到所有图层",
    "Apply to All Channels": "应用到所有通道",
    "Apply to All Images": "应用到所有图像",
    "Apply to All Objects": "应用到所有对象",
    "Do for All": "对所有执行",
    "Do for All Selected": "对所有所选执行",
    "Do for All Remaining": "对所有剩余执行",
    "Do Not Show Again": "不再显示",
    "Do Not Ask Again": "不再询问",
    "Never Ask Again": "不再询问",
    "Always Show": "始终显示",
    "Always Ask": "始终询问",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX56.items():
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
