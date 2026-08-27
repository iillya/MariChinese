#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第四十五批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX45 = {
    "Apply to": "应用到",
    "Remove from": "从以下移除",
    "Move to": "移动到",
    "Copy to": "复制到",
    "Paste to": "粘贴到",
    "Add to": "添加到",
    "Delete from": "从以下删除",
    "Rename to": "重命名为",
    "Convert to": "转换为",
    "Change to": "更改为",
    "Set to": "设置为",
    "Reset to": "重置为",
    "Restore to": "还原为",
    "Save as": "另存为",
    "Load from": "从以下加载",
    "Import from": "从以下导入",
    "Export to": "导出到",
    "Send to": "发送到",
    "Open in": "在以下中打开",
    "Show in": "在以下中显示",
    "Reveal in": "在以下中显示",
    "Find in": "在以下中查找",
    "Replace with": "替换为",
    "Insert at": "插入到",
    "Go to": "转到",
    "Jump to": "跳转到",
    "Switch to": "切换到",
    "Use as": "用作",
    "Use for": "用于",
    "Use with": "与以下一起使用",
    "Create from": "从以下创建",
    "Generate from": "从以下生成",
    "Derive from": "从以下派生",
    "Override with": "用以下覆盖",
    "Fill with": "用以下填充",
    "Mask with": "用以下蒙版",
    "Blend with": "与以下混合",
    "Combine with": "与以下合并",
    "Merge with": "与以下合并",
    "Apply to Object": "应用到对象",
    "Apply to Layer": "应用到图层",
    "Apply to Channel": "应用到通道",
    "Apply to Image": "应用到图像",
    "Apply to Selection": "应用到所选",
    "Apply to Project": "应用到项目",
    "Apply to All Layers": "应用到所有图层",
    "Apply to All Channels": "应用到所有通道",
    "Apply to All Images": "应用到所有图像",
    "Apply to All Objects": "应用到所有对象",
    "Apply to All Patches": "应用到所有面片",
    "Apply to Selected Layers": "应用到所选图层",
    "Apply to Selected Channels": "应用到所选通道",
    "Apply to Selected Items": "应用到所选项目",
    "Remove from Layer": "从图层移除",
    "Remove from Channel": "从通道移除",
    "Remove from Project": "从项目移除",
    "Remove from Image": "从图像移除",
    "Remove from Group": "从组移除",
    "Remove from Stack": "从堆栈移除",
    "Move to Layer": "移动到图层",
    "Move to Folder": "移动到文件夹",
    "Move to Group": "移动到组",
    "Move to Stack": "移动到堆栈",
    "Move to Project": "移动到项目",
    "Move to Selection": "移动到所选",
    "Copy to Layer": "复制到图层",
    "Copy to Channel": "复制到通道",
    "Copy to Selection": "复制到所选",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX45.items():
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
