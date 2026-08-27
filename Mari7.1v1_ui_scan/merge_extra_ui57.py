#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第五十七批：生僻/补充界面词，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX57 = {
    "Unnamed": "未命名",
    "Untitled": "未命名",
    "Unknown": "未知",
    "Mixed": "混合",
    "Auto Detect": "自动检测",
    "Detected": "已检测",
    "Custom": "自定义",
    "Preset": "预设",
    "Standard": "标准",
    "Legacy": "旧版",
    "Beta": "测试版",
    "Preview": "预览",
    "Draft": "草稿",
    "Final": "最终版",
    "Stable": "稳定版",
    "Experimental": "实验性",
    "Hidden": "隐藏",
    "Advanced": "高级",
    "Basic": "基本",
    "Pro": "专业版",
    "Lite": "轻量版",
    "Standard Edition": "标准版",
    "Professional Edition": "专业版",
    "Enterprise Edition": "企业版",
    "Community Edition": "社区版",
    "Educational": "教育版",
    "Commercial": "商业版",
    "Personal": "个人版",
    "Free": "免费",
    "Paid": "付费",
    "Trial": "试用版",
    "Demo": "演示版",
    "Full Version": "完整版",
    "Pro Version": "专业版",
    "Lite Version": "轻量版",
    "Starter": "入门版",
    "Progression": "进度",
    "Sequence": "序列",
    "File Sequence": "文件序列",
    "Image Sequence": "图像序列",
    "Sequence Start": "序列起点",
    "Sequence End": "序列终点",
    "Sequence Length": "序列长度",
    "Sequence Step": "序列步长",
    "Sequence Padding": "序列填充",
    "Sequence Format": "序列格式",
    "Sequence Path": "序列路径",
    "Sequence Name": "序列名称",
    "Sequence Type": "序列类型",
    "Sequence Size": "序列大小",
    "Sequence Resolution": "序列分辨率",
    "Sequence Range": "序列范围",
    "Sequence Settings": "序列设置",
    "Sequence Options": "序列选项",
    "Sequence Loader": "序列加载器",
    "Sequence Importer": "序列导入器",
    "Sequence Exporter": "序列导出器",
    "Sequence Preview": "序列预览",
    "Sequence Playback": "序列播放",
    "Sequence Frame": "序列帧",
    "Sequence Frames": "序列帧",
    "Sequence Count": "序列数量",
    "Image Frame": "图像帧",
    "Frame Offset": "帧偏移",
    "First Image": "第一张图像",
    "Last Image": "最后一张图像",
    "Frame Padding": "帧填充",
    "Frame Scale": "帧缩放",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX57.items():
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
