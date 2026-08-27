#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第十批：无效值/状态/视图编辑类界面词，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX10 = {
    "All server licenses in use": "所有服务器许可证都在使用中",
    "Archive path is empty": "归档路径为空",
    "Array textures not supported yet, sorry!": "暂不支持数组纹理，抱歉！",
    "Device verification request failed": "设备验证请求失败",
    "Differing Numbers of proxy levels": "代理级别数量不同",
    "Find": "查找",
    "Generate": "生成",
    "Import Failed": "导入失败",
    "Invalid bit depth": "无效的位深度",
    "Invalid bit depth provided": "提供的位深度无效",
    "Invalid channel count": "无效的通道数量",
    "Invalid channel name.": "无效的通道名称。",
    "Invalid color count": "无效的颜色数量",
    "Invalid color picker mode supplied": "提供的颜色选择器模式无效",
    "Invalid crop parameters": "无效的裁剪参数",
    "Invalid empty output image path": "无效的空输出图像路径",
    "Invalid empty path": "无效的空路径",
    "Invalid file extension for %1 Bake Point Node.": "'%1' 烘焙点节点的文件扩展名无效。",
    "Invalid frame count": "无效的帧数",
    "Invalid geo channel": "无效的几何通道",
    "Invalid image passed": "传入的图像无效",
    "Invalid image set parameter": "无效的图像集参数",
    "Invalid input colorspace": "无效的输入颜色空间",
    "Invalid input colorspace supplied": "提供的输入颜色空间无效",
    "Invalid output colorspace": "无效的输出颜色空间",
    "Invalid projector provided": "提供的投影器无效",
    "Invalid property key": "无效的属性键",
    "Invalid property value": "无效的属性值",
    "Invalid shelf or group given for ungrouping.": "为取消编组提供的架子或组无效。",
    "Invalid size encountered": "遇到无效的大小",
    "Invalid string list type.": "无效的字符串列表类型。",
    "Not enough data available": "可用数据不足",
    "Only Some Reasons": "仅部分原因",
    "Select all": "全选",
    "Select none": "全不选",
    "Show all": "显示全部",
    "Show none": "不显示",
    "Zoom in": "放大",
    "Zoom out": "缩小",
    "Fit to screen": "适应屏幕",
    "Next page": "下一页",
    "Previous page": "上一页",
    "Apply to all": "应用到全部",
    "Go to": "转到",
    "No items": "没有项目",
    "No results": "没有结果",
    "No changes": "无更改",
    "No selection": "未选择",
    "No open files": "没有打开的文件",
    "Nothing selected": "未选择任何内容",
    "Ok": "确定",
    "Are you sure?": "你确定吗？",
    "Yes to All": "全部选是",
    "No to All": "全部选否",
    "Cancel All": "全部取消",
    "Close All": "全部关闭",
    "Save All": "全部保存",
    "Select None": "全不选",
    "Remove All": "全部移除",
    "Delete All": "全部删除",
    "Apply All": "全部应用",
    "View All": "查看全部",
    "Hide All": "全部隐藏",
    "Show All": "全部显示",
    "Clear All": "全部清除",
    "Enable All": "全部启用",
    "Disable All": "全部禁用",
    "Keep Current": "保留当前",
    "Use Current": "使用当前",
    "Use Default": "使用默认",
    "Reset To Defaults": "重置为默认值",
    "Load Defaults": "加载默认值",
    "Restore Defaults": "还原默认值",
    "Open Recent": "打开最近使用",
    "Open Project": "打开项目",
    "New Project": "新建项目",
    "Save Project": "保存项目",
    "Save Project As": "项目另存为",
    "Close Project": "关闭项目",
    "Project Settings": "项目设置",
    "Preferences": "首选项",
    "Import Image": "导入图像",
    "Export Image": "导出图像",
    "New Layer": "新建图层",
    "Duplicate Layer": "复制图层",
    "Delete Layer": "删除图层",
    "Layer Properties": "图层属性",
    "New Channel": "新建通道",
    "Channel Properties": "通道属性",
    "New Folder": "新建文件夹",
    "New Group": "新建组",
    "Delete Group": "删除组",
    "Move to Group": "移动到组",
    "Add to Shelf": "添加到架子",
    "Remove from Shelf": "从架子移除",
    "New Tag": "新建标签",
    "Edit Tags": "编辑标签",
    "Filter by Tag": "按标签筛选",
    "Filter by Name": "按名称筛选",
    "Sort by Name": "按名称排序",
    "Sort by Modified": "按修改时间排序",
    "History": "历史记录",
    "Clear History": "清除历史记录",
    "Recent Files": "最近文件",
    "Recent Projects": "最近项目",
    "Untitled": "未命名",
    "Rename Layer": "重命名图层",
    "Make Visible": "设为可见",
    "Make Hidden": "设为隐藏",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX10.items():
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
    if existed:
        print("已存在跳过(部分):", existed[:20])


if __name__ == "__main__":
    main()
