#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第二十三批：状态/布局/操作补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX23 = {
    "Active": "活动",
    "Inactive": "非活动",
    "Enabled": "已启用",
    "Disabled": "已禁用",
    "Visible": "可见",
    "Hidden": "已隐藏",
    "Locked": "已锁定",
    "Unlocked": "已解锁",
    "Selected": "已选择",
    "Unselected": "未选择",
    "Current": "当前",
    "Default": "默认",
    "Custom": "自定义",
    "Automatic": "自动",
    "Manual": "手动",
    "Automatic Mode": "自动模式",
    "Manual Mode": "手动模式",
    "Normal Mode": "正常模式",
    "Advanced Mode": "高级模式",
    "Basic Mode": "基本模式",
    "Preview Mode": "预览模式",
    "Edit Mode": "编辑模式",
    "View Mode": "查看模式",
    "Solo Mode": "独奏模式",
    "Mute": "静音",
    "Unmute": "取消静音",
    "Solo": "独奏",
    "Bypass": "旁路",
    "Activate": "激活",
    "Deactivate": "停用",
    "Apply": "应用",
    "Revert": "还原",
    "Commit": "提交",
    "Discard": "丢弃",
    "Undo": "撤销",
    "Redo": "重做",
    "Cut": "剪切",
    "Copy": "复制",
    "Paste": "粘贴",
    "Duplicate": "复制",
    "Delete": "删除",
    "Rename": "重命名",
    "Move": "移动",
    "Resize": "调整大小",
    "Reorder": "重新排序",
    "Move Up": "上移",
    "Move Down": "下移",
    "Move Left": "左移",
    "Move Right": "右移",
    "Bring Forward": "上移一层",
    "Send Backward": "下移一层",
    "Bring to Front": "置于顶层",
    "Send to Back": "置于底层",
    "Group": "编组",
    "Ungroup": "取消编组",
    "Link": "链接",
    "Unlink": "取消链接",
    "Lock": "锁定",
    "Unlock": "解锁",
    "Collapse": "折叠",
    "Expand": "展开",
    "Minimize": "最小化",
    "Maximize": "最大化",
    "Restore": "还原",
    "Close": "关闭",
    "Open": "打开",
    "Save": "保存",
    "Save As": "另存为",
    "Save All": "全部保存",
    "Load": "加载",
    "Reload": "重新加载",
    "Refresh": "刷新",
    "Clear": "清除",
    "Reset": "重置",
    "Cancel": "取消",
    "Confirm": "确认",
    "OK": "确定",
    "Yes": "是",
    "No": "否",
    "Back": "返回",
    "Next": "下一步",
    "Finish": "完成",
    "Done": "完成",
    "Close Dialog": "关闭对话框",
    "Accept": "接受",
    "Reject": "拒绝",
    "Abort": "中止",
    "Skip": "跳过",
    "Retry": "重试",
    "Ignore": "忽略",
    "Help": "帮助",
    "About": "关于",
    "Settings": "设置",
    "Options": "选项",
    "Preferences": "首选项",
    "Properties": "属性",
    "Information": "信息",
    "Warning": "警告",
    "Error": "错误",
    "Success": "成功",
    "Failure": "失败",
    "Ready": "就绪",
    "Busy": "忙碌",
    "Idle": "空闲",
    "Processing": "处理中",
    "Loading": "加载中",
    "Saving": "保存中",
    "Exporting": "导出中",
    "Importing": "导入中",
    "Rendering": "渲染中",
    "Baking": "烘焙中",
    "Completed": "已完成",
    "Cancelled": "已取消",
    "Progress": "进度",
    "Percentage": "百分比",
    "Remaining": "剩余",
    "Elapsed": "已用时间",
    "Duration": "时长",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX23.items():
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
    if existed:
        print("已存在跳过(部分):", existed[:30])


if __name__ == "__main__":
    main()
