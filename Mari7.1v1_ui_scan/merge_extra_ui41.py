#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第四十一批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX41 = {
    "Confirm Delete": "确认删除",
    "Confirm Remove": "确认移除",
    "Confirm Overwrite": "确认覆盖",
    "Confirm Save": "确认保存",
    "Confirm Close": "确认关闭",
    "Confirm Replace": "确认替换",
    "Confirm Apply": "确认应用",
    "Confirm Reset": "确认重置",
    "Are you sure you want to delete '%1'?": "确定要删除 '%1' 吗？",
    "Are you sure you want to remove '%1'?": "确定要移除 '%1' 吗？",
    "Are you sure you want to overwrite '%1'?": "确定要覆盖 '%1' 吗？",
    "Are you sure you want to save?": "确定要保存吗？",
    "Are you sure you want to close?": "确定要关闭吗？",
    "Are you sure you want to quit?": "确定要退出吗？",
    "Are you sure you want to reset?": "确定要重置吗？",
    "Are you sure you want to replace existing?": "确定要替换现有内容吗？",
    "Do you want to save changes?": "是否保存更改？",
    "Do you want to delete this?": "是否删除此项？",
    "Do you want to continue?": "是否继续？",
    "Do you want to proceed?": "是否继续？",
    "Do you want to apply changes?": "是否应用更改？",
    "Do you want to discard changes?": "是否丢弃更改？",
    "Do you want to exit without saving?": "是否不保存就退出？",
    "Do you want to overwrite?": "是否覆盖？",
    "Do you want to overwrite existing files?": "是否覆盖现有文件？",
    "Do you want to replace the existing file?": "是否替换现有文件？",
    "This action cannot be undone.": "此操作无法撤销。",
    "This action will delete the selected items.": "此操作将删除所选项目。",
    "This action will overwrite the existing data.": "此操作将覆盖现有数据。",
    "This action may take a while.": "此操作可能需要一些时间。",
    "This will replace the current file.": "这将替换当前文件。",
    "This will overwrite the existing file.": "这将覆盖现有文件。",
    "This will update the project.": "这将更新项目。",
    "Please confirm.": "请确认。",
    "Are you sure?": "你确定吗？",
    "Are you sure? This cannot be undone.": "你确定吗？此操作无法撤销。",
    "Continue with the current action?": "继续执行当前操作吗？",
    "Cancel the current action?": "取消当前操作吗？",
    "Discard the current changes?": "丢弃当前更改吗？",
    "Save the current changes?": "保存当前更改吗？",
    "Keep the current version?": "保留当前版本吗？",
    "Use the new version?": "使用新版本吗？",
    "Revert to the previous version?": "还原到上一个版本吗？",
    "Overwrite the old version?": "覆盖旧版本吗？",
    "Create a new version?": "创建新版本吗？",
    "Apply to all items?": "应用到所有项目吗？",
    "Apply to all images?": "应用到所有图像吗？",
    "Apply to all layers?": "应用到所有图层吗？",
    "Apply to all selected?": "应用到所有所选吗？",
    "Apply to matching items?": "应用到匹配的项目吗？",
    "Select all matching?": "选择所有匹配项吗？",
    "Search all?" : "搜索全部吗？",
    "Close without saving?": "不保存就关闭吗？",
    "Quit without saving?": "不保存就退出吗？",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX41.items():
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
