#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第七十五批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX75 = {
    "Settings": "设置",
    "Settings Panel": "设置面板",
    "Settings Window": "设置窗口",
    "Settings Dialog": "设置对话框",
    "Settings Menu": "设置菜单",
    "Settings Tab": "设置标签页",
    "Settings Tab Page": "设置标签页",
    "Settings Category": "设置类别",
    "Settings Group": "设置组",
    "Settings Section": "设置分区",
    "Settings Item": "设置项",
    "Settings Items": "设置项",
    "Settings Field": "设置字段",
    "Settings Option": "设置选项",
    "Settings Options": "设置选项",
    "Settings Value": "设置值",
    "Settings Name": "设置名称",
    "Settings Label": "设置标签",
    "Settings Description": "设置说明",
    "Settings Tooltip": "设置提示",
    "Settings Default": "默认设置",
    "Settings Custom": "自定义设置",
    "Settings Preset": "设置预设",
    "Settings Save": "保存设置",
    "Settings Load": "加载设置",
    "Settings Reset": "重置设置",
    "Settings Restore": "还原设置",
    "Settings Apply": "应用设置",
    "Settings Cancel": "取消设置",
    "Settings Enable": "启用设置",
    "Settings Disable": "禁用设置",
    "Settings Show": "显示设置",
    "Settings Hide": "隐藏设置",
    "Settings Lock": "锁定设置",
    "Settings Unlock": "解锁设置",
    "Settings Changed": "设置已更改",
    "Settings Unsaved": "设置有未保存更改",
    "Settings Saved": "设置已保存",
    "Settings Applied": "设置已应用",
    "Settings Reset to Default": "设置重置为默认",
    "Settings Restore Defaults": "设置还原默认值",
    "Settings Export": "导出设置",
    "Settings Import": "导入设置",
    "Settings Advanced": "高级设置",
    "Settings Basic": "基本设置",
    "Settings General": "通用设置",
    "Settings Performance": "性能设置",
    "Settings Display": "显示设置",
    "Settings Input": "输入设置",
    "Settings Output": "输出设置",
    "Settings Color": "颜色设置",
    "Settings Render": "渲染设置",
    "Settings Bake": "烘焙设置",
    "Settings Paint": "绘制设置",
    "Settings Brush": "笔刷设置",
    "Settings Tool": "工具设置",
    "Settings Camera": "相机设置",
    "Settings Light": "灯光设置",
    "Settings Material": "材质设置",
    "Settings Texture": "纹理设置",
    "Settings Image": "图像设置",
    "Settings Layer": "图层设置",
    "Settings Channel": "通道设置",
    "Settings Mask": "蒙版设置",
    "Settings Node": "节点设置",
    "Settings Shader": "着色器设置",
    "Settings Filter": "滤镜设置",
    "Settings Project": "项目设置",
    "Settings Network": "网络设置",
    "Settings Plugin": "插件设置",
    "Settings Workspace": "工作区设置",
    "Settings Library": "库设置",
    "Settings Shortcut": "快捷键设置",
    "Settings Update": "更新设置",
    "Settings Interface": "界面设置",
    "Settings Theme": "主题设置",
    "Settings Language": "语言设置",
    "Settings Units": "单位设置",
    "Settings Preferences": "首选项设置",
    "Settings Options": "选项设置",
    "Settings Values": "设置值",
    "Settings Cleanup": "清理设置",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX75.items():
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
