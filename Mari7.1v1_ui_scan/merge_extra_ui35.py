#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第三十五批：通用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX35 = {
    "Count": "数量",
    "Number": "数量",
    "Amount": "数量",
    "Quantity": "数量",
    "Total Count": "总数量",
    "Count of Items": "项目数量",
    "Index": "索引",
    "Index Value": "索引值",
    "List Index": "列表索引",
    "Order": "顺序",
    "Order By": "排序方式",
    "Sort Order": "排序顺序",
    "Sort Direction": "排序方向",
    "Ascending": "升序",
    "Descending": "降序",
    "Alphabetical": "按字母顺序",
    "Numerical": "按数字",
    "By Name": "按名称",
    "By Type": "按类型",
    "By Size": "按大小",
    "By Date": "按日期",
    "By Modified Date": "按修改日期",
    "By Resolution": "按分辨率",
    "By Color Space": "按颜色空间",
    "Sort By": "排序依据",
    "Group By": "分组依据",
    "Filter By": "筛选依据",
    "Showing": "正在显示",
    "Showing All": "显示全部",
    "Showing Selected": "显示所选",
    "Showing Hidden": "显示隐藏",
    "Viewing": "正在查看",
    "Items": "项目",
    "Item": "项目",
    "Items Selected": "已选择项目",
    "Items Found": "找到的项目",
    "Items Filtered": "已过滤项目",
    "Items Hidden": "隐藏的项目",
    "Items Locked": "锁定的项目",
    "Items Visible": "可见项目",
    "No Items Found": "未找到项目",
    "No Items Selected": "未选择任何项目",
    "Select Items": "选择项目",
    "Deselect Items": "取消选择项目",
    "Invert Items": "反转项目选择",
    "Show Items": "显示项目",
    "Hide Items": "隐藏项目",
    "Lock Items": "锁定项目",
    "Unlock Items": "解锁项目",
    "Rename Items": "重命名项目",
    "Move Items": "移动项目",
    "Copy Items": "复制项目",
    "Delete Items": "删除项目",
    "Duplicate Items": "复制项目",
    "Clear Items": "清除项目",
    "Expand All": "全部展开",
    "Collapse All": "全部折叠",
    "Show Expand": "显示展开",
    "Hide Expand": "隐藏展开",
    "Open All": "全部打开",
    "Close All": "全部关闭",
    "Apply to All": "应用到全部",
    "Apply to Selected": "应用到所选",
    "Apply to None": "不应用",
    "Apply All Changes": "应用全部更改",
    "Discard All Changes": "丢弃全部更改",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX35.items():
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
