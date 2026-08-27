#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第七十三批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX73 = {
    "Rename": "重命名",
    "Rename Selected": "重命名所选",
    "Rename All": "全部重命名",
    "Rename Item": "重命名项目",
    "Rename Items": "重命名项目",
    "Rename Layer": "重命名图层",
    "Rename Channel": "重命名通道",
    "Rename Image": "重命名图像",
    "Rename Material": "重命名材质",
    "Rename Texture": "重命名纹理",
    "Rename Object": "重命名对象",
    "Rename Geometry": "重命名几何体",
    "Rename Mesh": "重命名网格",
    "Rename Node": "重命名节点",
    "Rename Shader": "重命名着色器",
    "Rename Filter": "重命名滤镜",
    "Rename Mask": "重命名蒙版",
    "Rename Selection": "重命名选择",
    "Rename Brush": "重命名笔刷",
    "Rename Camera": "重命名相机",
    "Rename Light": "重命名灯光",
    "Rename Preset": "重命名预设",
    "Rename Tab": "重命名标签页",
    "Rename Panel": "重命名面板",
    "Rename Palette": "重命名面板",
    "Rename Tool": "重命名工具",
    "Rename Shelf": "重命名架子",
    "Rename Tag": "重命名标签",
    "Rename File": "重命名文件",
    "Rename Folder": "重命名文件夹",
    "Rename Directory": "重命名目录",
    "Rename to": "重命名为",
    "Rename to New Name": "重命名为新名称",
    "Rename with Prefix": "添加前缀重命名",
    "Rename with Suffix": "添加后缀重命名",
    "Rename Sequence": "重命名序列",
    "Rename Using Pattern": "按模式重命名",
    "Rename in Bulk": "批量重命名",
    "Rename All Items": "重命名所有项目",
    "Rename Selected Items": "重命名所选项目",
    "Rename Group": "重命名组",
    "Rename Folder Group": "重命名文件夹组",
    "Rename Node Graph": "重命名节点图",
    "Rename Shader Network": "重命名着色器网络",
    "Rename Scene": "重命名场景",
    "Rename Project": "重命名项目",
    "Rename Workspace": "重命名工作区",
    "Rename Library": "重命名库",
    "Rename Asset": "重命名资产",
    "Rename Layer Group": "重命名图层组",
    "Rename Image Set": "重命名图像集",
    "Rename Channel Stack": "重命名通道堆栈",
    "Rename Mask Stack": "重命名蒙版堆栈",
    "Rename Project Directory": "重命名项目目录",
    "Rename Path": "重命名路径",
    "Rename Alias": "重命名别名",
    "Rename Shortcut": "重命名快捷键",
    "Rename Macro": "重命名宏",
    "Rename Command": "重命名命令",
    "Rename Option": "重命名选项",
    "Rename Setting": "重命名设置",
    "Rename Attribute": "重命名属性",
    "Rename Property": "重命名属性",
    "Rename Upload": "重命名上传",
    "Rename Download": "重命名下载",
    "Rename Render": "重命名渲染",
    "Rename Bake": "重命名烘焙",
    "Rename Result": "重命名结果",
    "Rename Output": "重命名输出",
    "Rename View": "重命名视图",
    "Rename Viewport": "重命名视口",
    "Rename Viewer": "重命名查看器",
    "Renaming": "正在重命名",
    "Renamed": "已重命名",
    "Rename Complete": "重命名完成",
    "Rename Failed": "重命名失败",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX73.items():
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
