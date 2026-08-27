#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第二十六批：图层/通道/蒙版操作补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX26 = {
    "Layer Group": "图层组",
    "Layer Group Properties": "图层组属性",
    "Layer List": "图层列表",
    "Layer Stack": "图层堆栈",
    "Layer Type": "图层类型",
    "Layer Color": "图层颜色",
    "Layer Opacity": "图层不透明度",
    "Layer Blend": "图层混合",
    "Layer Mode": "图层模式",
    "Layer Preset": "图层预设",
    "Move Layer Up": "上移图层",
    "Move Layer Down": "下移图层",
    "Reorder Layers": "重新排序图层",
    "Duplicate Layer Below": "在下方复制图层",
    "Duplicate Layer Above": "在上方复制图层",
    "Add Layer Above": "在上方添加图层",
    "Add Layer Below": "在下方添加图层",
    "Select Layer Below": "选择下方图层",
    "Select Layer Above": "选择上方图层",
    "Next Layer": "下一图层",
    "Previous Layer": "上一图层",
    "Collapse Layer Group": "折叠图层组",
    "Expand Layer Group": "展开图层组",
    "Flatten Layer": "展平图层",
    "Merge Layers": "合并图层",
    "Merge Down": "向下合并",
    "Merge Visible": "合并可见",
    "Merge All": "全部合并",
    "Apply Layer": "应用图层",
    "Remove Layer": "移除图层",
    "Clear Layer": "清除图层",
    "Bake Layer": "烘焙图层",
    "Cache Layer": "缓存图层",
    "Uncache Layer": "取消缓存图层",
    "Solo Layer": "独奏图层",
    "Mute Layer": "静音图层",
    "Unmute Layer": "取消静音图层",
    "Select Mask": "选择蒙版",
    "Select Alpha": "选择 Alpha",
    "Select Color": "选择颜色",
    "Select Bump": "选择凹凸",
    "Select Specular": "选择高光",
    "Select Roughness": "选择粗糙度",
    "Select Displacement": "选择置换",
    "Select Custom Channel": "选择自定义通道",
    "Channel Type": "通道类型",
    "Channel Color": "通道颜色",
    "Channel Opacity": "通道不透明度",
    "Channel List": "通道列表",
    "Channel Properties": "通道属性",
    "Channel Settings": "通道设置",
    "Add Channel": "添加通道",
    "Copy Channel": "复制通道",
    "Delete Channel": "删除通道",
    "Rename Channel": "重命名通道",
    "Revert Channel": "还原通道",
    "Flatten Channel": "展平通道",
    "Bake Channel": "烘焙通道",
    "Convert Channel": "转换通道",
    "Channel Color Space": "通道颜色空间",
    "Channel Depth": "通道深度",
    "Channel Resolution": "通道分辨率",
    "Channel Size": "通道大小",
    "Channel Information": "通道信息",
    "Use Channel Settings": "使用通道设置",
    "Reset Channel Settings": "重置通道设置",
    "Load Channel Settings": "加载通道设置",
    "Save Channel Settings": "保存通道设置",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX26.items():
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
