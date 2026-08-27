#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第八十九批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX89 = {
    "Texture": "纹理",
    "Texture Settings": "纹理设置",
    "Texture Options": "纹理选项",
    "Texture Properties": "纹理属性",
    "Texture Name": "纹理名称",
    "Texture Type": "纹理类型",
    "Texture Format": "纹理格式",
    "Texture Size": "纹理大小",
    "Texture Width": "纹理宽度",
    "Texture Height": "纹理高度",
    "Texture Depth": "纹理深度",
    "Texture Resolution": "纹理分辨率",
    "Texture Scale": "纹理缩放",
    "Texture Offset": "纹理偏移",
    "Texture Repeat": "纹理重复",
    "Texture Wrap": "纹理循环",
    "Texture Mode": "纹理模式",
    "Texture Color Space": "纹理颜色空间",
    "Texture Bit Depth": "纹理位深度",
    "Texture Pixel Format": "纹理像素格式",
    "Texture Compression": "纹理压缩",
    "Texture Quality": "纹理质量",
    "Texture Filtering": "纹理过滤",
    "Texture Filter": "纹理滤镜",
    "Texture Mipmap": "纹理 Mipmap",
    "Texture Mipmaps": "纹理 Mipmap",
    "Texture Preview": "纹理预览",
    "Texture Preview Size": "纹理预览大小",
    "Texture Preview Quality": "纹理预览质量",
    "Texture Thumbnail": "纹理缩略图",
    "Texture Thumbnail Size": "纹理缩略图大小",
    "Texture Icon": "纹理图标",
    "Texture Label": "纹理标签",
    "Texture Path": "纹理路径",
    "Texture File": "纹理文件",
    "Texture Folder": "纹理文件夹",
    "Texture Directory": "纹理目录",
    "Texture Library": "纹理库",
    "Texture Browser": "纹理浏览器",
    "Texture List": "纹理列表",
    "Texture Stack": "纹理堆叠",
    "Texture Group": "纹理组",
    "Texture Category": "纹理类别",
    "Texture Preset": "纹理预设",
    "Texture Default": "默认纹理",
    "Texture Custom": "自定义纹理",
    "Texture Atlas": "纹理图集",
    "Texture Atlas Size": "纹理图集大小",
    "Texture Atlas Resolution": "纹理图集分辨率",
    "Texture Atlas Layout": "纹理图集布局",
    "Texture Generate": "生成纹理",
    "Texture Update": "更新纹理",
    "Texture Refresh": "刷新纹理",
    "Texture Rebuild": "重建纹理",
    "Texture Add": "添加纹理",
    "Texture Remove": "移除纹理",
    "Texture Delete": "删除纹理",
    "Texture Duplicate": "复制纹理",
    "Texture Rename": "重命名纹理",
    "Texture Copy": "复制纹理",
    "Texture Paste": "粘贴纹理",
    "Texture Edit": "编辑纹理",
    "Texture Create": "创建纹理",
    "Texture Import": "导入纹理",
    "Texture Export": "导出纹理",
    "Texture Save": "保存纹理",
    "Texture Load": "加载纹理",
    "Texture Set": "设置纹理",
    "Texture Reset": "重置纹理",
    "Texture Clear": "清除纹理",
    "Texture Show": "显示纹理",
    "Texture Hide": "隐藏纹理",
    "Texture Enable": "启用纹理",
    "Texture Disable": "禁用纹理",
    "Texture Lock": "锁定纹理",
    "Texture Unlock": "解锁纹理",
    "Texture Visible": "纹理可见",
    "Texture Invisible": "纹理不可见",
    "Texture Selected": "纹理已选择",
    "Texture Filtering": "纹理过滤",
    "Texture Sort": "纹理排序",
    "Texture Search": "纹理搜索",
    "Texture Notes": "纹理备注",
    "Texture Tags": "纹理标签",
    "Texture Info": "纹理信息",
    "Textures": "纹理",
    "Texture Map": "纹理贴图",
    "Texture Maps": "纹理贴图",
    "Texture Set": "纹理集",
    "Texture Sets": "纹理集",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX89.items():
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
