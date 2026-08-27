#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第三十批：归档/版本/工程辅助补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX30 = {
    "Archive": "归档",
    "Archives": "归档",
    "Create Archive": "创建归档",
    "Export Archive": "导出归档",
    "Import Archive": "导入归档",
    "Package": "打包",
    "Repackage": "重新打包",
    "Unpackage": "解包",
    "Extract": "提取",
    "Extract To": "提取到",
    "Compress": "压缩",
    "Decompress": "解压",
    "Zip": "压缩",
    "Unzip": "解压",
    "Version": "版本",
    "Versions": "版本",
    "New Version": "新版本",
    "Old Version": "旧版本",
    "Current Version": "当前版本",
    "Previous Version": "上一版本",
    "Next Version": "下一版本",
    "Version History": "版本历史",
    "Version Name": "版本名称",
    "Version Number": "版本号",
    "Add Version": "添加版本",
    "Remove Version": "移除版本",
    "Rename Version": "重命名版本",
    "Set Current Version": "设为当前版本",
    "Make Current": "设为当前",
    "Restore Version": "还原版本",
    "Rollback": "回滚",
    "Rollback Version": "回滚版本",
    "Compare Versions": "比较版本",
    "Diff": "差异",
    "Diff Tool": "差异工具",
    "Project Version": "项目版本",
    "Object Version": "对象版本",
    "Versioning": "版本管理",
    "File Version": "文件版本",
    "Compatibility": "兼容性",
    "Compatible": "兼容",
    "Incompatible": "不兼容",
    "Backup": "备份",
    "Backup File": "备份文件",
    "Create Backup": "创建备份",
    "Restore Backup": "还原备份",
    "Delete Backup": "删除备份",
    "Backup Location": "备份位置",
    "Backup Folder": "备份文件夹",
    "Save Backup": "保存备份",
    "Load Backup": "加载备份",
    "Autosave": "自动保存",
    "Auto Save": "自动保存",
    "Enable Autosave": "启用自动保存",
    "Disable Autosave": "禁用自动保存",
    "Autosave Interval": "自动保存间隔",
    "Recover": "恢复",
    "Recovery": "恢复",
    "Recover File": "恢复文件",
    "Data Recovery": "数据恢复",
    "Temp File": "临时文件",
    "Temporary File": "临时文件",
    "Save to Temp": "保存到临时文件",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX30.items():
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
