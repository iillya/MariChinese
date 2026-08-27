#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第五十四批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX54 = {
    "Export": "导出",
    "Export File": "导出文件",
    "Export Folder": "导出文件夹",
    "Export Images": "导出图像",
    "Export Image Set": "导出图像集",
    "Export Channel": "导出通道",
    "Export Layer": "导出图层",
    "Export Material": "导出材质",
    "Export Texture": "导出纹理",
    "Export Model": "导出模型",
    "Export Mesh": "导出网格",
    "Export Geometry": "导出几何体",
    "Export Object": "导出对象",
    "Export Project": "导出项目",
    "Export Scene": "导出场景",
    "Export Preset": "导出预设",
    "Export Brush": "导出笔刷",
    "Export Archive": "导出归档",
    "Export Shelf": "导出架子",
    "Export Selection": "导出选择",
    "Export Sequence": "导出序列",
    "Export Options": "导出选项",
    "Export Settings": "导出设置",
    "Export Path": "导出路径",
    "Export Folder Path": "导出文件夹路径",
    "Export File Path": "导出文件路径",
    "Export Format": "导出格式",
    "Export Type": "导出类型",
    "Export Mode": "导出模式",
    "Export Scale": "导出缩放",
    "Export Offset": "导出偏移",
    "Export Rotation": "导出旋转",
    "Export Units": "导出单位",
    "Export Resolution": "导出分辨率",
    "Export Size": "导出大小",
    "Export Color Space": "导出颜色空间",
    "Export Mipmaps": "导出 Mipmap",
    "Export Proxy": "导出代理",
    "Export Padding": "导出内边距",
    "Export Transforms": "导出变换",
    "Export UVs": "导出 UV",
    "Export Normals": "导出法线",
    "Export Tangents": "导出切线",
    "Export in Background": "后台导出",
    "Export on Bake": "烘焙时导出",
    "Export on Save": "保存时导出",
    "Export Range": "导出范围",
    "Export All": "全部导出",
    "Export Selected": "导出所选",
    "Export Visible": "导出可见",
    "Export Frame Range": "导出帧范围",
    "Export Time Range": "导出时间范围",
    "Export Complete": "导出完成",
    "Export Failed": "导出失败",
    "Export in Progress": "导出进行中",
    "Export Cancelled": "导出已取消",
    "Export Success": "导出成功",
    "Export Error": "导出错误",
    "Export Warning": "导出警告",
    "Export Summary": "导出摘要",
    "Export Details": "导出详情",
    "Export Result": "导出结果",
    "Export Items": "导出项目",
    "Files to Export": "要导出的文件",
    "Exporting Files": "正在导出文件",
    "Exporting Data": "正在导出数据",
    "Export Ready": "导出准备就绪",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX54.items():
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
