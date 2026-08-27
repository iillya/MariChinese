#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第二十九批：设置项/状态辅助补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX29 = {
    "Show All": "全部显示",
    "Hide All": "全部隐藏",
    "Show Visible": "显示可见",
    "Hide Visible": "隐藏可见",
    "Show Unselected": "显示未选择",
    "Hide Unselected": "隐藏未选择",
    "Show Only Selected": "仅显示所选",
    "Hide Others": "隐藏其他",
    "Show Others": "显示其他",
    "Solo This": "独奏此项",
    "Unsolo": "取消独奏",
    "Solo All": "全部独奏",
    "Select All": "全选",
    "Select None": "全不选",
    "Invert Selection": "反转选择",
    "Deselect All": "取消全选",
    "Reselect": "重新选择",
    "Clear Selection": "清除选择",
    "Keep Selection": "保留选择",
    "Restore Selection": "恢复选择",
    "Save Selection As": "将选择另存为",
    "Load Selection From": "从以下位置加载选择",
    "Selection Name": "选择名称",
    "Selection Color": "选择颜色",
    "Selection Opacity": "选择不透明度",
    "Selection Preview": "选择预览",
    "Setup Selection": "设置选择",
    "Set Current": "设为当前",
    "Clear Current": "清除当前",
    "Current Selection": "当前选择",
    "Previous Selection": "上一个选择",
    "Next Selection": "下一个选择",
    "First": "第一个",
    "Last": "最后一个",
    "Previous": "上一个",
    "Next": "下一个",
    "Beginning": "开头",
    "End": "结尾",
    "Remove All": "全部移除",
    "Remove Selected": "移除所选",
    "Remove Unselected": "移除未选择",
    "Clear All": "全部清除",
    "Clear Selected": "清除所选",
    "Apply Changes": "应用更改",
    "Discard Changes": "丢弃更改",
    "Save Changes": "保存更改",
    "Cancel Changes": "取消更改",
    "Undo Changes": "撤销更改",
    "Redo Changes": "重做更改",
    "Confirm Changes": "确认更改",
    "Revert Changes": "还原更改",
    "Commit Changes": "提交更改",
    "Changes Pending": "待保存更改",
    "Unsaved Changes": "未保存的更改",
    "Dirty": "已修改",
    "Clean": "干净",
    "Modified": "已修改",
    "New": "新建",
    "Updated": "已更新",
    "Deleted": "已删除",
    "Added": "已添加",
    "Renamed": "已重命名",
    "Moved": "已移动",
    "Copied": "已复制",
    "Pasted": "已粘贴",
    "Duplicated": "已复制",
    "Untitled": "未命名",
    "Unnamed": "未命名",
    "Empty": "空",
    "Not Empty": "非空",
    "None": "无",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX29.items():
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
