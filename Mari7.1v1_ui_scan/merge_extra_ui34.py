#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第三十四批：快捷键/命令/撤销补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX34 = {
    "Shortcut Settings": "快捷键设置",
    "Shortcut Editor": "快捷键编辑器",
    "Shortcut List": "快捷键列表",
    "Shortcut Name": "快捷键名称",
    "Shortcut Key": "快捷键",
    "Shortcut Binding": "快捷键绑定",
    "Edit Shortcut": "编辑快捷键",
    "Add Shortcut": "添加快捷键",
    "Remove Shortcut": "移除快捷键",
    "Delete Shortcut": "删除快捷键",
    "Duplicate Shortcut": "复制快捷键",
    "Reset Shortcut": "重置快捷键",
    "Restore Shortcut": "还原快捷键",
    "Assign Shortcut": "分配快捷键",
    "Unassign Shortcut": "取消快捷键",
    "Clear Shortcut": "清除快捷键",
    "Shortcut Already In Use": "快捷键已被使用",
    "Shortcut Not Found": "未找到快捷键",
    "Shortcut Invalid": "快捷键无效",
    "Keyboard Shortcut": "键盘快捷键",
    "Keyboard Shortcuts": "键盘快捷键",
    "Command": "命令",
    "Commands": "命令",
    "Command List": "命令列表",
    "Command Name": "命令名称",
    "Command Line": "命令行",
    "Run Command": "运行命令",
    "Execute Command": "执行命令",
    "Command Failed": "命令失败",
    "Command Successful": "命令成功",
    "Command History": "命令历史",
    "Command Palette": "命令面板",
    "Command Options": "命令选项",
    "Macro": "宏",
    "Macros": "宏",
    "Macro Editor": "宏编辑器",
    "Macro Name": "宏名称",
    "Record Macro": "录制宏",
    "Play Macro": "播放宏",
    "Stop Macro": "停止宏",
    "Edit Macro": "编辑宏",
    "Delete Macro": "删除宏",
    "Duplicate Macro": "复制宏",
    "Export Macro": "导出宏",
    "Import Macro": "导入宏",
    "Undo History": "撤销历史",
    "Undo Stack": "撤销堆栈",
    "Redo Stack": "重做堆栈",
    "Undo All": "全部撤销",
    "Redo All": "全部重做",
    "Undo Last": "撤销上一步",
    "Redo Last": "重做上一步",
    "Clear Undo History": "清除撤销历史",
    "Undo Limit": "撤销上限",
    "Persistent Undo": "持久撤销",
    "History": "历史",
    "History List": "历史列表",
    "History Item": "历史项",
    "History Panel": "历史面板",
    "Show History": "显示历史",
    "Hide History": "隐藏历史",
    "Clear History": "清除历史",
    "Purge History": "清理历史",
    "History Depth": "历史深度",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX34.items():
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
