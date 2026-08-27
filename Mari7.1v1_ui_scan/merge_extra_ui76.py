#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第七十六批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX76 = {
    "Help": "帮助",
    "Help Center": "帮助中心",
    "Help Contents": "帮助内容",
    "Help Topics": "帮助主题",
    "Help Files": "帮助文件",
    "Help File": "帮助文件",
    "Help Menu": "帮助菜单",
    "Help Options": "帮助选项",
    "Help Settings": "帮助设置",
    "Help Panel": "帮助面板",
    "Help Window": "帮助窗口",
    "Help View": "帮助视图",
    "Help Documentation": "帮助文档",
    "Help Manual": "帮助手册",
    "Help Guide": "帮助指南",
    "Help Tutorial": "帮助教程",
    "Help Tutorials": "帮助教程",
    "Help Examples": "帮助示例",
    "Help Suggestions": "帮助建议",
    "Help Search": "帮助搜索",
    "Help Search Results": "帮助搜索结果",
    "Help About": "帮助关于",
    "Help Contact": "帮助联系",
    "Help Support": "帮助支持",
    "Help Feedback": "帮助反馈",
    "Help Resources": "帮助资源",
    "Help Links": "帮助链接",
    "Help Shortcuts": "帮助快捷键",
    "Help Shortcut": "帮助快捷键",
    "Help Tips": "帮助提示",
    "Help Tip": "帮助提示",
    "Show Help": "显示帮助",
    "Hide Help": "隐藏帮助",
    "Open Help": "打开帮助",
    "Close Help": "关闭帮助",
    "Get Help": "获取帮助",
    "Need Help?": "需要帮助？",
    "Need Help": "需要帮助",
    "Contact Support": "联系支持",
    "Support": "支持",
    "Support Center": "支持中心",
    "Support Contact": "支持联系",
    "Support Resources": "支持资源",
    "Support Options": "支持选项",
    "Support Settings": "支持设置",
    "Community": "社区",
    "Community Forum": "社区论坛",
    "Forum": "论坛",
    "Forums": "论坛",
    "FAQ": "常见问题",
    "FAQs": "常见问题",
    "Frequently Asked Questions": "常见问题",
    "Known Issues": "已知问题",
    "Bug Reports": "错误报告",
    "Report a Bug": "报告错误",
    "Report Bug": "报告错误",
    "Submit Feedback": "提交反馈",
    "Send Feedback": "发送反馈",
    "Feedback": "反馈",
    "Feedback Form": "反馈表单",
    "Feedback Details": "反馈详情",
    "Send": "发送",
    "Send Message": "发送消息",
    "Send to Support": "发送给支持",
    "Request": "请求",
    "Requests": "请求",
    "Request Support": "请求支持",
    "Submit Request": "提交请求",
    "Contact Us": "联系我们",
    "Contact": "联系",
    "Contact Information": "联系信息",
    "Email Support": "邮件支持",
    "Email": "邮件",
    "Email Address": "邮箱地址",
    "Email Support": "邮件支持",
    "Visit Website": "访问网站",
    "Website": "网站",
    "Download": "下载",
    "Downloads": "下载",
    "Download Center": "下载中心",
    "Download Page": "下载页面",
    "Install": "安装",
    "Install Now": "立即安装",
    "Install Later": "稍后安装",
    "Uninstall": "卸载",
    "Uninstall Now": "立即卸载",
    "Reinstall": "重新安装",
    "Repair": "修复",
    "Repair Installation": "修复安装",
    "Installation Complete": "安装完成",
    "Installation Failed": "安装失败",
    "Installation in Progress": "安装进行中",
    "Uninstallation Complete": "卸载完成",
    "Uninstallation Failed": "卸载失败",
    "License Agreement": "许可协议",
    "Terms of Service": "服务条款",
    "Privacy Policy": "隐私政策",
    "Privacy": "隐私",
    "EULA": "最终用户许可协议",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX76.items():
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
