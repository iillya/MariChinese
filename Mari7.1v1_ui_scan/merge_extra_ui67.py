#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第六十七批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX67 = {
    "Object": "对象",
    "Objects": "对象",
    "Object Settings": "对象设置",
    "Object Options": "对象选项",
    "Object Properties": "对象属性",
    "Object Name": "对象名称",
    "Object Type": "对象类型",
    "Object Mode": "对象模式",
    "Object Position": "对象位置",
    "Object Rotation": "对象旋转",
    "Object Scale": "对象缩放",
    "Object Bounds": "对象范围",
    "Object Pivot": "对象枢轴",
    "Object Origin": "对象原点",
    "Object Center": "对象中心",
    "Object Visibility": "对象可见性",
    "Object Visible": "对象可见",
    "Object Invisible": "对象不可见",
    "Object Locked": "对象已锁定",
    "Object Unlocked": "对象已解锁",
    "Object Selectable": "对象可选择",
    "Object Solo": "对象独奏",
    "Object Mute": "对象静音",
    "Object Selection": "对象选择",
    "Object List": "对象列表",
    "Object Browser": "对象浏览器",
    "Object Library": "对象库",
    "Object Category": "对象类别",
    "Object Preset": "对象预设",
    "Object Preview": "对象预览",
    "Object Thumbnail": "对象缩略图",
    "Object Icon": "对象图标",
    "Object Label": "对象标签",
    "Object Order": "对象顺序",
    "Object Arrangement": "对象排列",
    "Object Sort": "对象排序",
    "Object Search": "对象搜索",
    "Add Object": "添加对象",
    "Remove Object": "移除对象",
    "Delete Object": "删除对象",
    "Duplicate Object": "复制对象",
    "Rename Object": "重命名对象",
    "Copy Object": "复制对象",
    "Paste Object": "粘贴对象",
    "Move Object": "移动对象",
    "Re Parent": "重新父级",
    "Set Parent": "设置父级",
    "Clear Parent": "清除父级",
    "Group Objects": "编组对象",
    "Ungroup Objects": "取消编组对象",
    "Transform Object": "变换对象",
    "Reset Object": "重置对象",
    "Clear Object": "清除对象",
    "Create Object": "创建对象",
    "Select Object": "选择对象",
    "Deselect Object": "取消选择对象",
    "Edit Object": "编辑对象",
    "Save Object": "保存对象",
    "Load Object": "加载对象",
    "Export Object": "导出对象",
    "Import Object": "导入对象",
    "Insert Object": "插入对象",
    "Show Object": "显示对象",
    "Hide Object": "隐藏对象",
    "Enable Object": "启用对象",
    "Disable Object": "禁用对象",
    "Lock Object": "锁定对象",
    "Unlock Object": "解锁对象",
    "Merge Objects": "合并对象",
    "Combine Objects": "组合对象",
    "Separate Objects": "分离对象",
    "Split Object": "拆分对象",
    "Lattice": "晶格",
    "Lattice Deform": "晶格变形",
    "Apply Lattice": "应用晶格",
    "Remove Lattice": "移除晶格",
    "Object Deformation": "对象变形",
    "Deform": "变形",
    "Deform Object": "变形对象",
    "Reshape": "重塑",
    "Sculpt Object": "雕刻对象",
    "Flatten Object": "展平对象",
    "Smooth Object": "平滑对象",
    "Shrink Object": "收缩对象",
    "Inflate Object": "膨胀对象",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX67.items():
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
