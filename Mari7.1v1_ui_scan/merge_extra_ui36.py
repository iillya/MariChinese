#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第三十六批：网络/许可/更新类界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX36 = {
    "Internet": "互联网",
    "Connection": "连接",
    "Connect": "连接",
    "Disconnect": "断开连接",
    "Connected": "已连接",
    "Disconnected": "已断开",
    "Reconnect": "重新连接",
    "Connection Settings": "连接设置",
    "Connection Status": "连接状态",
    "Connection Type": "连接类型",
    "Connection Lost": "连接已断开",
    "Connection Restored": "连接已恢复",
    "Connection Timeout": "连接超时",
    "Connection Refused": "连接被拒绝",
    "Server": "服务器",
    "Server Address": "服务器地址",
    "Server Port": "服务器端口",
    "Server Name": "服务器名称",
    "Server Settings": "服务器设置",
    "Server Status": "服务器状态",
    "Server Timeout": "服务器超时",
    "Server Connection": "服务器连接",
    "Client": "客户端",
    "Client Address": "客户端地址",
    "Client Application": "客户端应用程序",
    "Network": "网络",
    "Network Settings": "网络设置",
    "Network Status": "网络状态",
    "Network Error": "网络错误",
    "Network Timeout": "网络超时",
    "Network Unavailable": "网络不可用",
    "Proxy": "代理",
    "Proxy Settings": "代理设置",
    "Use Proxy": "使用代理",
    "Proxy Address": "代理地址",
    "Proxy Port": "代理端口",
    "Offline": "离线",
    "Online": "在线",
    "Local": "本地",
    "Remote": "远程",
    "Cloud": "云端",
    "Upload": "上传",
    "Upload File": "上传文件",
    "Upload Complete": "上传完成",
    "Upload Failed": "上传失败",
    "Download": "下载",
    "Download File": "下载文件",
    "Download Complete": "下载完成",
    "Download Failed": "下载失败",
    "Sync with Cloud": "与云端同步",
    "Cloud Sync": "云端同步",
    "Save to Cloud": "保存到云端",
    "Load from Cloud": "从云端加载",
    "License": "许可证",
    "Licenses": "许可证",
    "Activate": "激活",
    "Activation": "激活",
    "Update": "更新",
    "Update Available": "可用更新",
    "Update Required": "必须更新",
    "Check For Updates": "检查更新",
    "Download Update": "下载更新",
    "Install Update": "安装更新",
    "Latest Version": "最新版本",
    "New Version Available": "有新版本可用",
    "Update Now": "立即更新",
    "Update Later": "稍后更新",
    "Updates": "更新",
    "Release": "版本",
    "Release Date": "发布日期",
    "Build": "构建",
    "Build Number": "构建号",
    "Build Date": "构建日期",
    "Version Information": "版本信息",
    "Version Info": "版本信息",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX36.items():
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
