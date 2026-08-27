#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第六十六批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX66 = {
    "Layer": "图层",
    "Layers": "图层",
    "Layer Settings": "图层设置",
    "Layer Options": "图层选项",
    "Layer Properties": "图层属性",
    "Layer Name": "图层名称",
    "Layer Type": "图层类型",
    "Layer Mode": "图层模式",
    "Layer Blend Mode": "图层混合模式",
    "Layer Opacity": "图层不透明度",
    "Layer Color": "图层颜色",
    "Layer Alpha": "图层 Alpha",
    "Layer Mask": "图层蒙版",
    "Layer Mask Enabled": "图层蒙版已启用",
    "Layer Mask Disabled": "图层蒙版已禁用",
    "Layer Mask Locked": "图层蒙版已锁定",
    "Layer Mask Linked": "图层蒙版已链接",
    "Layer Mask Unlinked": "图层蒙版已取消链接",
    "Layer Visibility": "图层可见性",
    "Layer Visible": "图层可见",
    "Layer Invisible": "图层不可见",
    "Layer Locked": "图层已锁定",
    "Layer Unlocked": "图层已解锁",
    "Layer Solo": "图层独奏",
    "Layer Mute": "图层静音",
    "Layer Enabled": "图层已启用",
    "Layer Disabled": "图层已禁用",
    "Layer Selection": "图层选择",
    "Layer List": "图层列表",
    "Layer Stack": "图层堆栈",
    "Layer Group": "图层组",
    "Layer Folder": "图层文件夹",
    "Layer Browser": "图层浏览器",
    "Layer Library": "图层库",
    "Layer Category": "图层类别",
    "Layer Preset": "图层预设",
    "Layer Preview": "图层预览",
    "Layer Thumbnail": "图层缩略图",
    "Layer Thumbnails": "图层缩略图",
    "Layer Icon": "图层图标",
    "Layer Label": "图层标签",
    "Layer Order": "图层顺序",
    "Layer Arrange": "图层排列",
    "Layer Sort": "图层排序",
    "Layer Search": "图层搜索",
    "Add Layer": "添加图层",
    "Remove Layer": "移除图层",
    "Delete Layer": "删除图层",
    "Duplicate Layer": "复制图层",
    "Rename Layer": "重命名图层",
    "Copy Layer": "复制图层",
    "Paste Layer": "粘贴图层",
    "Move Layer": "移动图层",
    "Reorder Layer": "重新排序图层",
    "Set Layer": "设置图层",
    "Reset Layer": "重置图层",
    "Clear Layer": "清除图层",
    "Flatten Layer": "展平图层",
    "Bake Layer": "烘焙图层",
    "Cache Layer": "缓存图层",
    "Uncache Layer": "取消缓存图层",
    "Convert Layer": "转换图层",
    "Create Layer": "创建图层",
    "Select Layer": "选择图层",
    "Deselect Layer": "取消选择图层",
    "Edit Layer": "编辑图层",
    "Save Layer": "保存图层",
    "Load Layer": "加载图层",
    "Export Layer": "导出图层",
    "Import Layer": "导入图层",
    "Insert Layer": "插入图层",
    "Show Layer": "显示图层",
    "Hide Layer": "隐藏图层",
    "Enable Layer": "启用图层",
    "Disable Layer": "禁用图层",
    "Lock Layer": "锁定图层",
    "Unlock Layer": "解锁图层",
    "Merge Layer": "合并图层",
    "Merge Down": "向下合并",
    "Merge Up": "向上合并",
    "Merge Visible": "合并可见",
    "Merge Layer Down": "向下合并图层",
    "New Layer Group": "新建图层组",
    "Add to Layer Group": "添加到图层组",
    "Remove from Layer Group": "从图层组移除",
    "Move to Layer Group": "移动到图层组",
    "New Adjustment Layer": "新建调整图层",
    "New Layer Mask": "新建图层蒙版",
    "Apply Layer Mask": "应用图层蒙版",
    "Remove Layer Mask": "移除图层蒙版",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX66.items():
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
