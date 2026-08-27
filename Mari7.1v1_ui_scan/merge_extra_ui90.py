#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第九十批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX90 = {
    "Light": "灯光",
    "Lighting": "灯光",
    "Light Settings": "灯光设置",
    "Light Options": "灯光选项",
    "Light Properties": "灯光属性",
    "Light Name": "灯光名称",
    "Light Type": "灯光类型",
    "Light Color": "灯光颜色",
    "Light Intensity": "灯光强度",
    "Light Power": "灯光功率",
    "Light Temperature": "灯光色温",
    "Light Angle": "灯光角度",
    "Light Radius": "灯光半径",
    "Light Size": "灯光大小",
    "Light Falloff": "灯光衰减",
    "Light Decay": "灯光衰减",
    "Light Shadow": "灯光阴影",
    "Light Shadows": "灯光阴影",
    "Light Softness": "灯光柔和度",
    "Light Direction": "灯光方向",
    "Light Position": "灯光位置",
    "Light Rotation": "灯光旋转",
    "Light Target": "灯光目标",
    "Light Visibility": "灯光可见性",
    "Light Visible": "灯光可见",
    "Light Hidden": "灯光隐藏",
    "Light Enabled": "灯光已启用",
    "Light Disabled": "灯光已禁用",
    "Light Selected": "灯光已选择",
    "Light List": "灯光列表",
    "Light Group": "灯光组",
    "Light Library": "灯光库",
    "Light Browser": "灯光浏览器",
    "Light Preset": "灯光预设",
    "Light Default": "默认灯光",
    "Light Custom": "自定义灯光",
    "Light Preview": "灯光预览",
    "Light Preview Mode": "灯光预览模式",
    "Light Thumbnail": "灯光缩略图",
    "Light Icon": "灯光图标",
    "Light Label": "灯光标签",
    "Light Add": "添加灯光",
    "Light Remove": "移除灯光",
    "Light Delete": "删除灯光",
    "Light Rename": "重命名灯光",
    "Light Duplicate": "复制灯光",
    "Light Copy": "复制灯光",
    "Light Paste": "粘贴灯光",
    "Light Edit": "编辑灯光",
    "Light Create": "创建灯光",
    "Light Select": "选择灯光",
    "Light Save": "保存灯光",
    "Light Load": "加载灯光",
    "Light Import": "导入灯光",
    "Light Export": "导出灯光",
    "Light Reset": "重置灯光",
    "Light Show": "显示灯光",
    "Light Hide": "隐藏灯光",
    "Light Enable": "启用灯光",
    "Light Disable": "禁用灯光",
    "Light Lock": "锁定灯光",
    "Light Unlock": "解锁灯光",
    "Light Sort": "灯光排序",
    "Light Search": "灯光搜索",
    "Light Notes": "灯光备注",
    "Light Tags": "灯光标签",
    "Light Info": "灯光信息",
    "Camera": "相机",
    "Camera Settings": "相机设置",
    "Camera Options": "相机选项",
    "Camera Properties": "相机属性",
    "Camera Name": "相机名称",
    "Camera Type": "相机类型",
    "Camera Position": "相机位置",
    "Camera Rotation": "相机旋转",
    "Camera Target": "相机目标",
    "Camera Focal Length": "相机焦距",
    "Camera Field of View": "相机视野",
    "Camera Near": "相机近裁剪",
    "Camera Far": "相机远裁剪",
    "Camera Clip": "相机裁剪",
    "Camera Distance": "相机距离",
    "Camera Angle": "相机角度",
    "Camera Zoom": "相机缩放",
    "Camera Speed": "相机速度",
    "Camera Visibility": "相机可见性",
    "Camera List": "相机列表",
    "Camera Group": "相机组",
    "Camera Library": "相机库",
    "Camera Browser": "相机浏览器",
    "Camera Preset": "相机预设",
    "Camera Default": "默认相机",
    "Camera Custom": "自定义相机",
    "Camera Preview": "相机预览",
    "Camera Thumbnail": "相机缩略图",
    "Camera Icon": "相机图标",
    "Camera Label": "相机标签",
    "Camera Add": "添加相机",
    "Camera Remove": "移除相机",
    "Camera Delete": "删除相机",
    "Camera Rename": "重命名相机",
    "Camera Duplicate": "复制相机",
    "Camera Copy": "复制相机",
    "Camera Paste": "粘贴相机",
    "Camera Edit": "编辑相机",
    "Camera Create": "创建相机",
    "Camera Select": "选择相机",
    "Camera Set": "设置相机",
    "Camera Save": "保存相机",
    "Camera Load": "加载相机",
    "Camera Import": "导入相机",
    "Camera Export": "导出相机",
    "Camera Reset": "重置相机",
    "Camera Show": "显示相机",
    "Camera Hide": "隐藏相机",
    "Camera Lock": "锁定相机",
    "Camera Unlock": "解锁相机",
    "Camera Sort": "相机排序",
    "Camera Search": "相机搜索",
    "Camera Notes": "相机备注",
    "Camera Info": "相机信息",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX90.items():
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
