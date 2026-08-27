#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第七十七批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX77 = {
    "Info": "信息",
    "Information": "信息",
    "Information Panel": "信息面板",
    "Information Dialog": "信息对话框",
    "Information Icon": "信息图标",
    "Information Message": "信息消息",
    "Information Text": "信息文本",
    "Information Details": "信息详情",
    "Information More": "更多信息",
    "Information About": "关于信息",
    "Information on": "相关信息",
    "Information for": "关于以下信息",
    "Show Info": "显示信息",
    "Hide Info": "隐藏信息",
    "More Info": "更多信息",
    "Less Info": "更少信息",
    "Info Icon": "信息图标",
    "Info Message": "信息消息",
    "Info Text": "信息文本",
    "Info Details": "信息详情",
    "Info Tooltip": "信息提示",
    "Info Bubble": "信息气泡",
    "Info Popup": "信息弹出",
    "Info Tip": "信息提示",
    "Info Hint": "信息提示",
    "Info Number": "信息编号",
    "Info Code": "信息代码",
    "Info ID": "信息 ID",
    "Info Name": "信息名称",
    "Info Value": "信息值",
    "Info Type": "信息类型",
    "Info Status": "信息状态",
    "Info State": "信息状态",
    "Info Level": "信息级别",
    "Info Category": "信息类别",
    "Info Order": "信息顺序",
    "Info List": "信息列表",
    "Info Group": "信息组",
    "Info Section": "信息分区",
    "Info Field": "信息字段",
    "Info Item": "信息项",
    "Info Items": "信息项",
    "Info Fieldset": "信息字段集",
    "Info Toolbar": "信息工具栏",
    "Info Bar": "信息栏",
    "Info Banner": "信息横幅",
    "Info Box": "信息框",
    "Info Message Box": "信息消息框",
    "Info Notification": "信息通知",
    "Info Indicator": "信息指示器",
    "Info Status Bar": "信息状态栏",
    "Info Readout": "信息读数",
    "Info Readout Field": "信息读数字段",
    "New Info": "新信息",
    "Add Info": "添加信息",
    "Edit Info": "编辑信息",
    "Update Info": "更新信息",
    "Clear Info": "清除信息",
    "Delete Info": "删除信息",
    "Remove Info": "移除信息",
    "Save Info": "保存信息",
    "Load Info": "加载信息",
    "Refresh Info": "刷新信息",
    "Reset Info": "重置信息",
    "Restore Info": "还原信息",
    "Get Info": "获取信息",
    "Gather Info": "收集信息",
    "Collect Info": "收集信息",
    "Show Info Panel": "显示信息面板",
    "Hide Info Panel": "隐藏信息面板",
    "Open Info Panel": "打开信息面板",
    "Close Info Panel": "关闭信息面板",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX77.items():
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
