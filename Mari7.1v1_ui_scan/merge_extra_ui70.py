#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第七十批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX70 = {
    "Close": "关闭",
    "Close Project": "关闭项目",
    "Close Image": "关闭图像",
    "Close File": "关闭文件",
    "Close Folder": "关闭文件夹",
    "Close Channel": "关闭通道",
    "Close Layer": "关闭图层",
    "Close Material": "关闭材质",
    "Close Texture": "关闭纹理",
    "Close Object": "关闭对象",
    "Close Geometry": "关闭几何体",
    "Close Mesh": "关闭网格",
    "Close Scene": "关闭场景",
    "Close Tab": "关闭标签页",
    "Close Window": "关闭窗口",
    "Close Panel": "关闭面板",
    "Close Palette": "关闭面板",
    "Close Viewport": "关闭视口",
    "Close Viewer": "关闭查看器",
    "Close Session": "关闭会话",
    "Close Workspace": "关闭工作区",
    "Close Library": "关闭库",
    "Close Asset": "关闭资产",
    "Close Preset": "关闭预设",
    "Close Brush": "关闭笔刷",
    "Close Camera": "关闭相机",
    "Close All": "全部关闭",
    "Close All Projects": "关闭所有项目",
    "Close All Images": "关闭所有图像",
    "Close All Files": "关闭所有文件",
    "Close All Windows": "关闭所有窗口",
    "Close All Panels": "关闭所有面板",
    "Close All Tabs": "关闭所有标签页",
    "Close All Documents": "关闭所有文档",
    "Close Others": "关闭其他",
    "Close Selected": "关闭所选",
    "Close Current": "关闭当前",
    "Close on Save": "保存后关闭",
    "Close without Saving": "不保存关闭",
    "Ask on Close": "关闭时询问",
    "Closing": "正在关闭",
    "Closing Project": "正在关闭项目",
    "Closing Image": "正在关闭图像",
    "Closing File": "正在关闭文件",
    "Closing Scene": "正在关闭场景",
    "Closed": "已关闭",
    "Closed Successfully": "成功关闭",
    "Exit": "退出",
    "Exit Project": "退出项目",
    "Exit Application": "退出应用程序",
    "Exit App": "退出应用",
    "Exit Without Saving": "不保存退出",
    "Quit": "退出",
    "Quit Application": "退出应用程序",
    "Quit App": "退出应用",
    "Quit without Saving": "不保存退出",
    "Quit All": "全部退出",
    "Exit All": "全部退出",
    "Exiting": "正在退出",
    "Exit Confirmation": "退出确认",
    "Exit Confirm": "退出确认",
    "Exit Warning": "退出警告",
    "Exit Code": "退出代码",
    "Exit Status": "退出状态",
    "Exit Reason": "退出原因",
    "Exit Message": "退出消息",
    "Exit Whole Application": "退出整个应用程序",
    "Exit Current Session": "退出当前会话",
    "Exit All Instances": "退出所有实例",
    "Exit on Done": "完成后退出",
    "Exit on Error": "出错时退出",
    "Exit on Warning": "警告时退出",
    "Force Exit": "强制退出",
    "Graceful Exit": "正常退出",
    "Save on Exit": "退出时保存",
    "Prompt on Exit": "退出时提示",
    "Dont Exit": "不退出",
    "Dont Quit": "不退出",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX70.items():
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
