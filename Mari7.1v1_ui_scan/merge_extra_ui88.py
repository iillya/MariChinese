#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第八十八批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX88 = {
    "Material": "材质",
    "Material Settings": "材质设置",
    "Material Options": "材质选项",
    "Material Properties": "材质属性",
    "Material Name": "材质名称",
    "Material Type": "材质类型",
    "Material Mode": "材质模式",
    "Material Color": "材质颜色",
    "Material Base Color": "材质基础颜色",
    "Material Opacity": "材质不透明度",
    "Material Transparency": "材质透明",
    "Material Roughness": "材质粗糙度",
    "Material Metallic": "材质金属度",
    "Material Specular": "材质高光",
    "Material Normal": "材质法线",
    "Material Bump": "材质凹凸",
    "Material Displacement": "材质置换",
    "Material Emission": "材质自发光",
    "Material Emissive": "材质自发光",
    "Material Ambient Occlusion": "材质环境光遮蔽",
    "Material Reflection": "材质反射",
    "Material Refraction": "材质折射",
    "Material Transmission": "材质透射",
    "Material Subsurface": "材质次表面",
    "Material Preview": "材质预览",
    "Material Preview Mode": "材质预览模式",
    "Material Preview Size": "材质预览大小",
    "Material Thumbnail": "材质缩略图",
    "Material Thumbnail Size": "材质缩略图大小",
    "Material Icon": "材质图标",
    "Material Label": "材质标签",
    "Material Library": "材质库",
    "Material Browser": "材质浏览器",
    "Material List": "材质列表",
    "Material Stack": "材质堆叠",
    "Material Group": "材质组",
    "Material Category": "材质类别",
    "Material Preset": "材质预设",
    "Material Default": "默认材质",
    "Material Custom": "自定义材质",
    "Material Shader": "材质着色器",
    "Material Shader Model": "材质着色器模型",
    "Material Shader Network": "材质着色器网络",
    "Material Layer": "材质图层",
    "Material Layers": "材质图层",
    "Material Layer Stack": "材质图层堆栈",
    "Material Node": "材质节点",
    "Material Node Graph": "材质节点图",
    "Material Graph": "材质图",
    "Material Assign": "材质分配",
    "Material Assign To": "分配材质到",
    "Material Assign To Object": "分配材质到对象",
    "Material Assign To Selection": "分配材质到所选",
    "Material Assign To Layer": "分配材质到图层",
    "Material Assign To Channel": "分配材质到通道",
    "Material Assign To Mesh": "分配材质到网格",
    "Material Add": "添加材质",
    "Material Remove": "移除材质",
    "Material Delete": "删除材质",
    "Material Duplicate": "复制材质",
    "Material Rename": "重命名材质",
    "Material Copy": "复制材质",
    "Material Paste": "粘贴材质",
    "Material Edit": "编辑材质",
    "Material Create": "创建材质",
    "Material Select": "选择材质",
    "Material Save": "保存材质",
    "Material Load": "加载材质",
    "Material Import": "导入材质",
    "Material Export": "导出材质",
    "Material Update": "更新材质",
    "Material Refresh": "刷新材质",
    "Material Reset": "重置材质",
    "Material Restore": "还原材质",
    "Material Clear": "清除材质",
    "Material Bake": "烘焙材质",
    "Material Convert": "转换材质",
    "Material Flatten": "展平材质",
    "Material Cache": "缓存材质",
    "Material Uncache": "取消缓存材质",
    "Material Show": "显示材质",
    "Material Hide": "隐藏材质",
    "Material Enable": "启用材质",
    "Material Disable": "禁用材质",
    "Material Lock": "锁定材质",
    "Material Unlock": "解锁材质",
    "Material Visible": "材质可见",
    "Material Invisible": "材质不可见",
    "Material Selected": "材质已选择",
    "Material Filter": "材质筛选",
    "Material Sort": "材质排序",
    "Material Search": "材质搜索",
    "Material Notes": "材质备注",
    "Material Tags": "材质标签",
    "Material Info": "材质信息",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX88.items():
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
