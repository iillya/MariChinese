#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第八十二批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX82 = {
    "Geometry": "几何体",
    "Mesh": "网格",
    "Mesh Settings": "网格设置",
    "Mesh Options": "网格选项",
    "Mesh Properties": "网格属性",
    "Mesh Name": "网格名称",
    "Mesh Type": "网格类型",
    "Mesh Position": "网格位置",
    "Mesh Rotation": "网格旋转",
    "Mesh Scale": "网格缩放",
    "Mesh Bounds": "网格范围",
    "Mesh Pivot": "网格枢轴",
    "Mesh Origin": "网格原点",
    "Mesh Center": "网格中心",
    "Mesh Visibility": "网格可见性",
    "Mesh Visible": "网格可见",
    "Mesh Invisible": "网格不可见",
    "Mesh Locked": "网格已锁定",
    "Mesh Selectable": "网格可选择",
    "Mesh Selection": "网格选择",
    "Mesh List": "网格列表",
    "Mesh Browser": "网格浏览器",
    "Mesh Library": "网格库",
    "Mesh Category": "网格类别",
    "Mesh Preset": "网格预设",
    "Mesh Preview": "网格预览",
    "Mesh Thumbnail": "网格缩略图",
    "Mesh Icon": "网格图标",
    "Mesh Label": "网格标签",
    "Add Mesh": "添加网格",
    "Remove Mesh": "移除网格",
    "Delete Mesh": "删除网格",
    "Duplicate Mesh": "复制网格",
    "Rename Mesh": "重命名网格",
    "Copy Mesh": "复制网格",
    "Paste Mesh": "粘贴网格",
    "Move Mesh": "移动网格",
    "Import Mesh": "导入网格",
    "Export Mesh": "导出网格",
    "Create Mesh": "创建网格",
    "Select Mesh": "选择网格",
    "Deselect Mesh": "取消选择网格",
    "Edit Mesh": "编辑网格",
    "Save Mesh": "保存网格",
    "Load Mesh": "加载网格",
    "Show Mesh": "显示网格",
    "Hide Mesh": "隐藏网格",
    "Enable Mesh": "启用网格",
    "Disable Mesh": "禁用网格",
    "Lock Mesh": "锁定网格",
    "Unlock Mesh": "解锁网格",
    "Merge Mesh": "合并网格",
    "Combine Mesh": "组合网格",
    "Separate Mesh": "分离网格",
    "Split Mesh": "拆分网格",
    "Mesh Transform": "网格变换",
    "Mesh Deform": "网格变形",
    "Mesh Smooth": "网格平滑",
    "Mesh Normal": "网格法线",
    "Subdivide Mesh": "细分网格",
    "Retopologize Mesh": "重新拓扑网格",
    "Decimate Mesh": "减面网格",
    "Quadrangulate Mesh": "网格四边形化",
    "Triangulate Mesh": "网格三角化",
    "Unwrap Mesh": "展开网格",
    "Mesh UV": "网格 UV",
    "Mesh UV Map": "网格 UV 贴图",
    "Mesh UV Set": "网格 UV 集",
    "Mesh UV Layer": "网格 UV 图层",
    "Mesh UV Channel": "网格 UV 通道",
    "Mesh Material": "网格材质",
    "Mesh Material Assign": "网格材质分配",
    "Mesh Shader": "网格着色器",
    "Mesh Shader Assign": "网格着色器分配",
    "Mesh Render": "网格渲染",
    "Mesh Renderer": "网格渲染器",
    "Mesh Stats": "网格统计",
    "Mesh Stats Info": "网格统计信息",
    "Mesh Details": "网格详情",
    "Mesh Information": "网格信息",
    "Mesh Properties Panel": "网格属性面板",
    "Mesh Editor": "网格编辑器",
    "Mesh Viewer": "网格查看器",
    "Mesh Viewport": "网格视口",
    "Mesh List Panel": "网格列表面板",
    "Mesh Browser Panel": "网格浏览器面板",
    "Mesh Library Panel": "网格库面板",
    "Mesh Category Panel": "网格类别面板",
    "Mesh Filter": "网格滤镜",
    "Mesh Filtering": "网格过滤",
    "Mesh Sort": "网格排序",
    "Mesh Search": "网格搜索",
    "Mesh Rows": "网格行",
    "Mesh Columns": "网格列",
    "Mesh Grid": "网格表",
    "Mesh Grid Settings": "网格表设置",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX82.items():
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
