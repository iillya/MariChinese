#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第八十六批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX86 = {
    "Project": "项目",
    "Project Settings": "项目设置",
    "Project Options": "项目选项",
    "Project Properties": "项目属性",
    "Project Name": "项目名称",
    "Project Type": "项目类型",
    "Project Location": "项目位置",
    "Project Path": "项目路径",
    "Project Folder": "项目文件夹",
    "Project Directory": "项目目录",
    "Project File": "项目文件",
    "Project Size": "项目大小",
    "Project Resolution": "项目分辨率",
    "Project Scale": "项目缩放",
    "Project Units": "项目单位",
    "Project Color Space": "项目颜色空间",
    "Project Color Management": "项目色彩管理",
    "Project Status": "项目状态",
    "Project State": "项目状态",
    "Project Visibility": "项目可见性",
    "Project Locked": "项目已锁定",
    "Project Unlocked": "项目已解锁",
    "Project Saved": "项目已保存",
    "Project Unsaved": "项目未保存",
    "Project Modified": "项目已修改",
    "Project Clean": "项目干净",
    "Project Dirty": "项目已修改",
    "Project History": "项目历史",
    "Project Version": "项目版本",
    "Project Versions": "项目版本",
    "Project Version History": "项目版本历史",
    "Project Backup": "项目备份",
    "Project Backups": "项目备份",
    "Project Archive": "项目归档",
    "Project Archives": "项目归档",
    "Project Cache": "项目缓存",
    "Project Cache Size": "项目缓存大小",
    "Project Cache Clear": "清除项目缓存",
    "Project Load": "加载项目",
    "Project Save": "保存项目",
    "Project Close": "关闭项目",
    "Project New": "新建项目",
    "Project Open": "打开项目",
    "Project Duplicate": "复制项目",
    "Project Rename": "重命名项目",
    "Project Delete": "删除项目",
    "Project Export": "导出项目",
    "Project Import": "导入项目",
    "Project Convert": "转换项目",
    "Project Upgrade": "升级项目",
    "Project Revert": "还原项目",
    "Project Purge": "清理项目",
    "Project Cleanup": "项目清理",
    "Project Optimize": "优化项目",
    "Project Validate": "校验项目",
    "Project Verify": "验证项目",
    "Project Repair": "修复项目",
    "Project Rebuild": "重建项目",
    "Project Reload": "重新加载项目",
    "Project Refresh": "刷新项目",
    "Project Sync": "同步项目",
    "Project Sync to Cloud": "项目同步到云端",
    "Project Save As": "项目另存为",
    "Project Save Copy": "项目另存副本",
    "Project Save As Template": "项目另存为模板",
    "Project New From Template": "从模板新建项目",
    "Project Copy To": "项目复制到",
    "Project Move To": "项目移动到",
    "Project Create Backup": "项目创建备份",
    "Project Restore Backup": "项目还原备份",
    "Project Create Archive": "项目创建归档",
    "Project Export Archive": "项目导出归档",
    "Project Import Archive": "项目导入归档",
    "Project Open Recent": "打开最近项目",
    "Project Recent List": "最近项目列表",
    "Project Info": "项目信息",
    "Project Information": "项目信息",
    "Project Details": "项目详情",
    "Project Summary": "项目摘要",
    "Project Overview": "项目概览",
    "Project Panel": "项目面板",
    "Project Window": "项目窗口",
    "Project Browser": "项目浏览器",
    "Project Library": "项目库",
    "Project Manager": "项目管理器",
    "Project Management": "项目管理",
    "Project Navigation": "项目导航",
    "Project Breadcrumbs": "项目路径",
    "Project Tree": "项目树",
    "Project List": "项目列表",
    "Project Data": "项目数据",
    "Project Metadata": "项目元数据",
    "Project Tags": "项目标签",
    "Project Notes": "项目备注",
    "Project Comments": "项目注释",
    "Project Description": "项目说明",
    "Project Template": "项目模板",
    "Project Preset": "项目预设",
    "Project Default": "默认项目",
    "Project Custom": "自定义项目",
    "Project Group": "项目组",
    "Project Category": "项目类别",
    "Project Order": "项目顺序",
    "Project Sort": "项目排序",
    "Project Search": "项目搜索",
    "Project Filter": "项目筛选",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX86.items():
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
