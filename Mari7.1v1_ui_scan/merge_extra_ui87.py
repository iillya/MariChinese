#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第八十七批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX87 = {
    "Image": "图像",
    "Image Settings": "图像设置",
    "Image Options": "图像选项",
    "Image Properties": "图像属性",
    "Image Name": "图像名称",
    "Image Type": "图像类型",
    "Image Format": "图像格式",
    "Image Size": "图像大小",
    "Image Width": "图像宽度",
    "Image Height": "图像高度",
    "Image Depth": "图像深度",
    "Image Resolution": "图像分辨率",
    "Image Scale": "图像缩放",
    "Image Offset": "图像偏移",
    "Image Color Space": "图像颜色空间",
    "Image Color Depth": "图像颜色深度",
    "Image Bit Depth": "图像位深度",
    "Image Width": "图像宽度",
    "Image Height": "图像高度",
    "Image Pixels": "图像像素",
    "Image Pixel Size": "图像像素大小",
    "Image Pixel Format": "图像像素格式",
    "Image Pixel Depth": "图像像素深度",
    "Image Pixel Ratio": "图像像素比例",
    "Image DPI": "图像 DPI",
    "Image PPI": "图像 PPI",
    "Image Dots Per Inch": "图像每英寸点数",
    "Image Compression": "图像压缩",
    "Image Quality": "图像质量",
    "Image Preview": "图像预览",
    "Image Preview Size": "图像预览大小",
    "Image Preview Quality": "图像预览质量",
    "Image Preview Mode": "图像预览模式",
    "Image Thumbnail": "图像缩略图",
    "Image Thumbnail Size": "图像缩略图大小",
    "Image Thumbnail Quality": "图像缩略图质量",
    "Image Icon": "图像图标",
    "Image Label": "图像标签",
    "Image Path": "图像路径",
    "Image File": "图像文件",
    "Image File Path": "图像文件路径",
    "Image File Name": "图像文件名",
    "Image File Type": "图像文件类型",
    "Image File Size": "图像文件大小",
    "Image File Format": "图像文件格式",
    "Image Folder": "图像文件夹",
    "Image Directory": "图像目录",
    "Image Status": "图像状态",
    "Image State": "图像状态",
    "Image Visible": "图像可见",
    "Image Hidden": "图像隐藏",
    "Image Locked": "图像已锁定",
    "Image Enabled": "图像已启用",
    "Image Disabled": "图像已禁用",
    "Image Selected": "图像已选择",
    "Image Unselected": "图像未选择",
    "Image Output": "图像输出",
    "Image Result": "图像结果",
    "Image Layer": "图像图层",
    "Image Channel": "图像通道",
    "Image Mask": "图像蒙版",
    "Image Alpha": "图像 Alpha",
    "Image Opacity": "图像不透明度",
    "Image Blend": "图像混合",
    "Image Blend Mode": "图像混合模式",
    "Image Composite": "图像合成",
    "Image Composite Mode": "图像合成模式",
    "Image Transform": "图像变换",
    "Image Position": "图像位置",
    "Image Rotation": "图像旋转",
    "Image Scale": "图像缩放",
    "Image flip": "图像翻转",
    "Image Mirror": "图像镜像",
    "Image Crop": "图像裁剪",
    "Image Resize": "图像调整大小",
    "Image Upscale": "图像放大",
    "Image Downscale": "图像缩小",
    "Image Rotate": "图像旋转",
    "Image Flip Horizontal": "图像水平翻转",
    "Image Flip Vertical": "图像垂直翻转",
    "Image Rotate 90": "图像旋转 90 度",
    "Image Rotate 180": "图像旋转 180 度",
    "Image Rotate 270": "图像旋转 270 度",
    "Image Trim": "图像裁剪",
    "Image Canvas": "图像画布",
    "Image Canvas Size": "图像画布大小",
    "Image Canvas Position": "图像画布位置",
    "Image Canvas Background": "图像画布背景",
    "Image Canvas Color": "图像画布颜色",
    "Image Import": "导入图像",
    "Image Export": "导出图像",
    "Image Save": "保存图像",
    "Image Load": "加载图像",
    "Image Close": "关闭图像",
    "Image Open": "打开图像",
    "Image Rename": "重命名图像",
    "Image Duplicate": "复制图像",
    "Image Delete": "删除图像",
    "Image Remove": "移除图像",
    "Image Copy": "复制图像",
    "Image Paste": "粘贴图像",
    "Image Move": "移动图像",
    "Image Reorder": "重新排序图像",
    "Image Refresh": "刷新图像",
    "Image Reload": "重新加载图像",
    "Image New": "新建图像",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX87.items():
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
