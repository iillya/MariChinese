#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第四十二批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX42 = {
    "Error Details": "错误详情",
    "Error Message": "错误消息",
    "Error Code": "错误代码",
    "Error Type": "错误类型",
    "Error Description": "错误说明",
    "Error Information": "错误信息",
    "Error Report": "错误报告",
    "Error Log": "错误日志",
    "Show Error": "显示错误",
    "Hide Error": "隐藏错误",
    "View Error": "查看错误",
    "Report Error": "报告错误",
    "Submit Error": "提交错误",
    "Send Error": "发送错误",
    "Copy Error": "复制错误",
    "Copy Error Details": "复制错误详情",
    "Copy Error Message": "复制错误消息",
    "Dismiss": "关闭",
    "Dismiss Error": "关闭错误",
    "Ignore Error": "忽略错误",
    "Retry Operation": "重试操作",
    "Retry Failed": "重试失败",
    "Abort Operation": "中止操作",
    "Cancel Operation": "取消操作",
    "Skip Operation": "跳过操作",
    "Proceed": "继续",
    "Proceed Anyway": "仍然继续",
    "Continue Anyway": "仍然继续",
    "Try Again": "重试",
    "Try Again Later": "稍后重试",
    "Try Another": "尝试其他",
    "Use Another": "使用其他",
    "Choose Another": "选择其他",
    "Select Another": "选择其他",
    "Pick Another": "选择其他",
    "Do Nothing": "不做任何操作",
    "Take No Action": "不采取操作",
    "Take Action": "采取操作",
    "Action Required": "需要操作",
    "Action Needed": "需要操作",
    "No Action Needed": "无需操作",
    "No Action Required": "无需操作",
    "Needs Attention": "需要关注",
    "Requires Attention": "需要关注",
    "Warning Message": "警告消息",
    "Warning Details": "警告详情",
    "Warning Code": "警告代码",
    "Warning Type": "警告类型",
    "Show Warning": "显示警告",
    "Hide Warning": "隐藏警告",
    "Dismiss Warning": "关闭警告",
    "Acknowledge": "确认",
    "Acknowledge Warning": "确认警告",
    "Acknowledge Error": "确认错误",
    "Acknowledge All": "全部确认",
    "Mark as Read": "标为已读",
    "Mark as Unread": "标为未读",
    "Mark as Resolved": "标为已解决",
    "Mark as Unresolved": "标为未解决",
    "Resolve": "解决",
    "Unresolve": "取消解决",
    "Resolved": "已解决",
    "Unresolved": "未解决",
    "Conflicts": "冲突",
    "Conflict": "冲突",
    "Resolve Conflict": "解决冲突",
    "Conflict Detected": "检测到冲突",
    "Conflict Resolution": "冲突解决",
    "Resolve Conflicts": "解决冲突",
    "Choose Resolution": "选择解决方案",
    "Skip Conflict": "跳过冲突",
    "Keep Both": "全部保留",
    "Keep Mine": "保留我的",
    "Keep Theirs": "保留对方的",
    "Overwrite Existing": "覆盖现有",
    "Replace Existing": "替换现有",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX42.items():
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
