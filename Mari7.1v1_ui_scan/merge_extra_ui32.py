#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第三十二批：通用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX32 = {
    "Auto": "自动",
    "Manual": "手动",
    "Off": "关闭",
    "On": "开启",
    "Always": "始终",
    "Never": "从不",
    "Once": "一次",
    "Sometimes": "有时",
    "Ask": "询问",
    "Ask Every Time": "每次询问",
    "Ask Once": "询问一次",
    "Prompt": "提示",
    "Prompt Me": "提示我",
    "Do Not Ask Again": "不再询问",
    "Do Not Show Again": "不再显示",
    "Show Again": "再次显示",
    "Remember": "记住",
    "Remember Me": "记住我",
    "Forget": "忘记",
    "Auto Detect": "自动检测",
    "Detect": "检测",
    "Choose Automatically": "自动选择",
    "Select Automatically": "自动选择",
    "Recommended": "推荐",
    "Not Recommended": "不推荐",
    "Optional": "可选",
    "Required": "必填",
    "Required Field": "必填项",
    "Enabled": "已启用",
    "Disabled": "已禁用",
    "In Use": "使用中",
    "Available": "可用",
    "Unavailable": "不可用",
    "In Progress": "进行中",
    "Not Started": "未开始",
    "Completed": "已完成",
    "Queued": "已排队",
    "Paused": "已暂停",
    "Resumed": "已恢复",
    "Blocked": "已阻止",
    "Waiting": "等待中",
    "Done": "完成",
    "Failed": "失败",
    "Succeeded": "成功",
    "Error": "错误",
    "Warning": "警告",
    "Info": "信息",
    "Tip": "提示",
    "Hint": "提示",
    "Notice": "通知",
    "Success": "成功",
    "Failure": "失败",
    "Unknown": "未知",
    "New": "新建",
    "Open": "打开",
    "Save": "保存",
    "Close": "关闭",
    "Apply": "应用",
    "Cancel": "取消",
    "OK": "确定",
    "Yes": "是",
    "No": "否",
    "Exit": "退出",
    "Quit": "退出",
    "Restart": "重启",
    "Restart Now": "立即重启",
    "Restart Later": "稍后重启",
    "Continue": "继续",
    "Skip": "跳过",
    "Next": "下一步",
    "Back": "返回",
    "Finish": "完成",
    "Complete": "完成",
    "Accept": "接受",
    "Decline": "拒绝",
    "Confirm": "确认",
    "Reject": "拒绝",
    "Abort": "中止",
    "Retry": "重试",
    "Ignore": "忽略",
    "Details": "详情",
    "More": "更多",
    "Less": "更少",
    "Advanced": "高级",
    "Basic": "基本",
    "General": "通用",
    "Standard": "标准",
    "Compact": "紧凑",
    "Expanded": "展开",
    "Collapsed": "折叠",
    "Reset": "重置",
    "Restore": "还原",
    "Recover": "恢复",
    "Synced": "已同步",
    "Not Synced": "未同步",
    "Syncing": "同步中",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX32.items():
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
