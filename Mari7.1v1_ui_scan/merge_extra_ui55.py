#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第五十五批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX55 = {
    "Save": "保存",
    "Save File": "保存文件",
    "Save As": "另存为",
    "Save Copy": "另存副本",
    "Save Current": "保存当前",
    "Save Project": "保存项目",
    "Save Image": "保存图像",
    "Save Channel": "保存通道",
    "Save Layer": "保存图层",
    "Save Material": "保存材质",
    "Save Texture": "保存纹理",
    "Save Result": "保存结果",
    "Save Output": "保存输出",
    "Save Selection": "保存选择",
    "Save Settings": "保存设置",
    "Save Options": "保存选项",
    "Save Preset": "保存预设",
    "Save Brush": "保存笔刷",
    "Save Tag": "保存标签",
    "Save Archive": "保存归档",
    "Save All": "全部保存",
    "Save Selected": "保存所选",
    "Save Visible": "保存可见",
    "Save As Copy": "另存为副本",
    "Save As New": "另存为新文件",
    "Save As Template": "另存为模板",
    "Save Overwrite": "覆盖保存",
    "Save Compressed": "压缩保存",
    "Save in Background": "后台保存",
    "Save on Close": "关闭时保存",
    "Save on Export": "导出时保存",
    "Save Path": "保存路径",
    "Save Folder": "保存文件夹",
    "Save Folder Path": "保存文件夹路径",
    "Save File Path": "保存文件路径",
    "Save Format": "保存格式",
    "Save Type": "保存类型",
    "Save Mode": "保存模式",
    "Save Resolution": "保存分辨率",
    "Save Size": "保存大小",
    "Save Quality": "保存质量",
    "Save Complete": "保存完成",
    "Save Failed": "保存失败",
    "Save in Progress": "保存进行中",
    "Save Cancelled": "保存已取消",
    "Save Success": "保存成功",
    "Save Error": "保存错误",
    "Ask to Save": "询问是否保存",
    "Save Changes": "保存更改",
    "Save Changes Before Exit": "退出前保存更改",
    "Save Changes Before Close": "关闭前保存更改",
    "Discard Changes": "丢弃更改",
    "Do Not Save": "不保存",
    "Save & Quit": "保存并退出",
    "Save & Continue": "保存并继续",
    "Save & Close": "保存并关闭",
    "Save & Exit": "保存并退出",
    "Save and Bake": "保存并烘焙",
    "Save and Export": "保存并导出",
    "Save and Archive": "保存并归档",
    "Save and Close Project": "保存并关闭项目",
    "Save before proceeding": "继续前保存",
    "Save Warning": "保存警告",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX55.items():
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
