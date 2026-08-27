#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第六批：节点/烘焙/导入导出类的用户可见错误句，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX6 = {
    "Failed to create Bump input node.": "创建凸凹输入节点失败。",
    "Failed to create Color to Vector node.": "创建颜色转矢量节点失败。",
    "Failed to create Height As Normal input node.": "创建高度作为法线输入节点失败。",
    "Failed to create Normal Modulation node.": "创建法线调制节点失败。",
    "Failed to create Set Unlit node.": "创建设为无光照节点失败。",
    "Failed to create Set Vector node.": "创建设置矢量节点失败。",
    "Failed to create Tangent Space to Eye Space node.": "创建切线空间转到视线空间节点失败。",
    "Failed to create a Color node": "创建颜色节点失败",
    "Failed to create a dummy blend node": "创建虚拟混合节点失败",
    "Failed to create a multi-channel bottom transparency node": "创建多通道底部透明度节点失败",
    "Failed to create a new image set for baked mask.": "为烘焙蒙版创建新图像集失败。",
    "Failed to create a new image set for baked material.": "为烘焙材质创建新图像集失败。",
    "Failed to create a node, but did not specify the error.": "创建节点失败，但未指定错误。",
    "Failed to create a node": "创建节点失败",
    "Failed to create a node of the desired type": "创建所需类型的节点失败",
    "Failed to create a tile for the stroke": "为笔画创建瓦片失败",
    "Failed to create archive file.  QuaZip error: %1": "创建归档文件失败。QuaZip 错误：%1",
    "Failed to create archive.  QuaZip error: %1": "创建归档失败。QuaZip 错误：%1",
    "Failed to create bottom transparency node.": "创建底部透明度节点失败。",
    "Failed to create custom procedural location '%1'": "创建自定义程序化位置 '%1' 失败",
    "Failed to create diffuse node.": "创建漫反射节点失败。",
    "Failed to create material location '%1'": "创建材质位置 '%1' 失败",
    "Failed to create multi-channel group stack.": "创建多通道组堆栈失败。",
    "Failed to create new Geo-Channel.": "创建新几何通道失败。",
    "Failed to create node for baked mask image set.": "为烘焙蒙版图像集创建节点失败。",
    "Failed to create node for baked material image set.": "为烘焙材质图像集创建节点失败。",
    "Failed to create patch link set. The shading context has no patches.": "创建面片链接集失败。着色上下文没有面片。",
    "Failed to create snap shot": "创建快照失败",
    "Failed to create specular node.": "创建高光节点失败。",
    "Failed to decompress archive data.": "解压归档数据失败。",
    "Failed to decompress block data.": "解压块数据失败。",
    "Failed to decompress data block.": "解压数据块失败。",
    "Failed to duplicate an adjustment node": "复制调整节点失败",
    "Failed to duplicate the secondary adjustment node": "复制二级调整节点失败",
    "Failed to find feature:": "找不到功能：",
    "Failed to open file '%1'.": "打开文件 '%1' 失败。",
    "Failed to read file '%1'": "读取文件 '%1' 失败",
    "Failed to save the project": "保存项目失败",
    "Failed to save the selected shelf": "保存选中的架子失败",
    "Failed to write to file '%1'": "写入文件 '%1' 失败",
    "Import failed: %1": "导入失败：%1",
    "Please check your permissions and that the path is correctly formed.": "请检查你的权限以及路径是否正确。",
    "Please confirm the activation code is displayed and click Activate in the browser window.": "请确认激活码已显示，并在浏览器窗口中点击“激活”。",
    "Please pick an existing ptex file": "请选择一个现有的 ptex 文件",
    "Please see log for more details.": "请查看日志了解更多详情。",
    "Please switch to 3D Paint mode?": "是否切换到 3D 绘制模式？",
    "Please switch to 2D Paint mode?": "是否切换到 2D 绘制模式？",
    "Set the 3D LUT size to a higher accuracy": "将 3D LUT 大小设为更高的精度",
    "Sets how the mirror plane should be displayed when painting.": "设置绘制时镜像平面的显示方式。",
    "Sets the color of the mirror plane or line when displayed.": "设置显示时镜像平面或线的颜色。",
    "The Given projector is already added to the list of projectors": "给定投影器已添加到投影器列表中",
    "The Given projector is not added to the list of projectors": "给定投影器未添加到投影器列表中",
    "The OCIO config file and/or corresponding colorspaces are invalid. Please check.": "OCIO 配置文件和/或对应的颜色空间无效。请检查。",
    "The VENDOR/ISV entry in the license string is invalid.": "许可证字符串中的 VENDOR/ISV 条目无效。",
    "The image is not of a uniform color": "图像不是纯色",
    "The license does not support this feature.": "许可证不支持此功能。",
    "The license has expired.": "许可证已过期。",
    "The license is already installed.": "许可证已安装。",
    "The selection contains %1 read-only item(s).": "所选内容包含 %1 个只读项目。",
    "The specified directory path for exporting GeoEntity does not exist : %1": "导出 GeoEntity 的指定目录路径不存在：%1",
    "The specified directory path for exporting GeoEntity is not empty : %1": "导出 GeoEntity 的指定目录路径不为空：%1",
    "The specified directory path for exporting GeoEntity is not writable : %1": "导出 GeoEntity 的指定目录路径不可写：%1",
    "The specified directory path for exporting nodes does not exist : %1": "导出节点的指定目录路径不存在：%1",
    "The specified directory path for exporting nodes is not empty : %1": "导出节点的指定目录路径不为空：%1",
    "The specified directory path for exporting nodes is not writable : %1": "导出节点的指定目录路径不可写：%1",
    "The specified path for exporting GeoEntity is a file : %1": "导出 GeoEntity 的指定路径是文件：%1",
    "The specified path for exporting GeoEntity is not a directory : %1": "导出 GeoEntity 的指定路径不是目录：%1",
    "The specified path for exporting nodes is a file : %1": "导出节点的指定路径是文件：%1",
    "The specified path for exporting nodes is not a directory : %1": "导出节点的指定路径不是目录：%1",
    "The time, in milliseconds, after which a key is considered": "按键在多少毫秒后被判定为",
    "This will have an effect on how much data is uploaded": "这会影响上传的数据量",
    "Toggles the rendering of shadows. This only hides": "切换阴影的渲染。此操作仅隐藏",
    "Unable to access the provided object": "无法访问提供的对象",
    "Unable to create MriFaceSelectionGroup without any faces selected": "未选择任何面时无法创建 MriFaceSelectionGroup",
    "Unable to create MriGeoEntitySelectionGroup without any objects selected": "未选择任何对象时无法创建 MriGeoEntitySelectionGroup",
    "Unable to create MriPatchSelectionGroup without any patches selected": "未选择任何面片时无法创建 MriPatchSelectionGroup",
    "Unable to create adjacency edge channel": "无法创建邻接边通道",
    "Unable to create adjacency face channel": "无法创建邻接面通道",
    "Unable to create edge adjacency channel": "无法创建边邻接通道",
    "Unable to create face adjacency channel": "无法创建面邻接通道",
    "Unable to create/access directory. Please try again as Administrator.": "无法创建/访问目录。请以管理员身份重试。",
    "Unable to determine painting mode.": "无法确定绘制模式。",
    "Unable to get child nodes.": "无法获取子节点。",
    "Unable to get node position.": "无法获取节点位置。",
    "Unable to get port list mode.": "无法获取端口列表模式。",
    "Unable to import images for Geo-Channel %1.": "无法为几何通道 %1 导入图像。",
    "Unable to locate source image": "无法定位源图像",
    "Unable to locate source image for face %1": "无法定位面 %1 的源图像",
    "Unable to locate the 'Patches' MainWindow menu": "无法定位“面片”主窗口菜单",
    "Unable to locate the 'Ptex' MainWindow menu": "无法定位“Ptex”主窗口菜单",
    "Unable to read file '%1'": "无法读取文件 '%1'",
    "Unable to set node position.": "无法设置节点位置。",
    "Unable to set node size.": "无法设置节点大小。",
    "Unable to set port list mode.": "无法设置端口列表模式。",
    "Warning: Could not activate feature with backend": "警告：后端无法激活功能",
    "You should install the Foundry Licensing Tools (FLT) and try again.": "你应该安装 Foundry 许可工具（FLT）然后再试。",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX6.items():
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
        print("已存在跳过:", existed)


if __name__ == "__main__":
    main()
