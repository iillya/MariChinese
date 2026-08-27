#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第二批：把剩余候选里的真 UI 词条翻译后合并进正式词典。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX2 = {
    # ---- 面板 / 窗口 ----
    "Background Importer": "后台导入器",
    "Background Jobs": "后台任务",
    "HUD Manager": "HUD 管理器",
    "Message Log": "消息日志",
    "Mari Palettes": "Mari 面板",
    "Mari Configuration": "Mari 配置",
    "Mari Command Port": "Mari 命令端口",
    "Mari Graphics Card Check": "Mari 显卡检查",
    "Mari OpenGL Check": "Mari OpenGL 检查",
    "Mari Non-Commercial": "Mari 非商业版",
    "Mari Non-commercial": "Mari 非商业版",
    "Mari Indie": "Mari 独立版",
    "Mari Message": "Mari 消息",
    "Mari build information": "Mari 构建信息",
    "Curve Atlas": "曲线图集",
    "Curve Editor": "曲线编辑器",
    "Custom Palette": "自定义面板",
    "Custom Procedural": "自定义程序化",
    "Custom Toolbars": "自定义工具栏",
    "Tool Manager": "工具管理器",
    "Named Files": "已命名文件",
    # ---- 版本 / 版本名 ----
    "Business Edition": "商业版",
    "Commercial Mari": "商业版 Mari",
    "Compute Cluster Edition": "计算集群版",
    "Datacenter Edition": "数据中心版",
    "Datacenter x64 Edition": "数据中心 x64 版",
    "Enterprise Edition": "企业版",
    "Enterprise x64 Edition": "企业 x64 版",
    "Home Edition": "家庭版",
    "Home Premium Edition": "家庭高级版",
    "Starter Edition": "入门版",
    "Ultimate Edition": "终极版",
    "Web Edition": "网络版",
    # ---- 编辑 / 操作 ----
    "Bake Image: %1": "烘焙图像：%1",
    "Calculate Normals": "计算法线",
    "Capture state": "捕获状态",
    "Cloud Logout": "云端登出",
    "Delete Knob : %1": "删除控件：%1",
    "Delete Mask : %1": "删除蒙版：%1",
    "Edit Script of '%1'": "编辑 '%1' 的脚本",
    "Initialize Rendering System": "初始化渲染系统",
    "Keep existing image set": "保留现有图像集",
    "Loading Version": "加载版本",
    "Manage Login Licenses": "管理登录许可证",
    "Manage Login Roaming": "管理登录漫游",
    "Mark Final": "标记为最终版",
    "Move Layer '%1'": "移动图层 '%1'",
    "Move node %1": "移动节点 %1",
    "Pick Again": "重新拾取",
    "Pick Environment": "拾取环境",
    "Pick an image file": "拾取图像文件",
    "Pick raw pixels": "拾取原始像素",
    "Pick screen pixels": "拾取屏幕像素",
    "Pin the palette": "固定面板",
    "Pin/float palette mode": "固定/浮动面板模式",
    "Play temporary macro": "播放临时宏",
    "Record temporary macro": "录制临时宏",
    "Replace mask": "替换蒙版",
    "Remap Colorspaces": "重映射颜色空间",
    "Rescue All Floating Palettes": "复原所有浮动面板",
    "Search Actions": "搜索操作",
    "Search Hits %1": "搜索结果命中 %1",
    "Search Paths": "搜索路径",
    "Search the available actions": "搜索可用的操作",
    "Split Point": "分割点",
    "Team Login": "团队登录",
    "Team Login Roaming": "团队登录漫游",
    "Welcome To Mari": "欢迎使用 Mari",
    "Welcome to Mari Non-commercial": "欢迎使用 Mari 非商业版",
    # ---- 选项 / 参数 / 设置 ----
    "Changed %1 Automatic Colorspace": "已更改 %1 自动颜色空间",
    "Changed %1 Colorspace": "已更改 %1 颜色空间",
    "Changed OCIO Config": "已更改 OCIO 配置",
    "ColorCorrection Pipeline": "色彩校正管线",
    "Colorspace LUT": "颜色空间 LUT",
    "Colorspace Transform": "颜色空间变换",
    "Colorspace CPU Usage": "颜色空间 CPU 使用量",
    "Custom OCIO Config": "自定义 OCIO 配置",
    "Container for %1 properties": "%1 属性的容器",
    "Create Singleton": "创建单例",
    "Deformation flags:": "变形标志：",
    "Dense equivalent:": "稠密等效值：",
    "Extended Info:": "扩展信息：",
    "Fast Importer": "快速导入器",
    "File version unrecognized": "文件版本无法识别",
    "Files used for checkout:": "用于检出的文件：",
    "General painting layer": "常规绘制图层",
    "Image Info : %1": "图像信息：%1",
    "Input count : %1": "输入数量：%1",
    "Inverse Difference": "反向差异",
    "Label loop": "标签循环",
    "Link Knobs:": "链接控件：",
    "Maximum number of lights": "最大灯光数量",
    "Minimum Flick Speed": "最小轻拂速度",
    "Mip-Map Generation": "Mip 贴图生成",
    "Modifed By": "修改者",
    "More details": "更多详情",
    "More information": "更多信息",
    "Multi-channel group": "多通道组",
    "Multiple OCIO Configs": "多个 OCIO 配置",
    "Native DPI scaling enabled": "已启用原生 DPI 缩放",
    "Not Paintable": "不可绘制",
    "Not required": "非必需",
    "Number of Keyframes": "关键帧数量",
    "Number of Snapshots": "快照数量",
    "OCIO Colorspace": "OCIO 颜色空间",
    "OCIO Config": "OCIO 配置",
    "OCIO Config Differs from Environment": "OCIO 配置与环境不同",
    "Occlusion Distance - 10.0m": "遮挡距离 - 10.0m",
    "Occlusion Distance - 3.0m": "遮挡距离 - 3.0m",
    "Occlusion Rays - 256": "遮挡光线 - 256",
    "Offscreen AA": "离屏抗锯齿",
    "Offscreen Buffers": "离屏缓冲区",
    "Only this layer": "仅此图层",
    "Output Level/BlackOut": "输出级别/黑出",
    "Output Level/OutBlack": "输出级别/输出黑",
    "Output Level/OutWhite": "输出级别/输出白",
    "Output Level/WhiteOut": "输出级别/白出",
    "Painting Style": "绘制风格",
    "Painting hidden": "绘制已隐藏",
    "Per face texture size": "每面纹理大小",
    "Post Process": "后期处理",
    "Procedural Property": "程序化属性",
    "Processing Animation": "正在处理动画",
    "Projecting on front of objects": "投影到对象前面",
    "Projecting through objects": "穿透对象投影",
    "Quad Remapping": "四边形重映射",
    "Reloads shaders without upgrading nodes": "重新加载着色器但不升级节点",
    "Roaming page description": "漫游页描述",
    "Shared shader": "共享着色器",
    "Smart Mask/Color Procedural/%1": "智能蒙版/颜色程序化/%1",
    "Smart Mask/Procedural Mask/%1": "智能蒙版/程序化蒙版/%1",
    "Sponge Desaturate": "海绵去饱和",
    "Spread Angle - 180": "扩散角度 - 180",
    "Spread Angle - 45": "扩散角度 - 45",
    "Steady Stroke": "平稳笔画",
    "Texels per Unit": "每单位纹理元素",
    "Thumbnail Generated": "缩略图已生成",
    "Thumbnail generation": "缩略图生成",
    "Tile Layout": "瓦片布局",
    "Upgrades nodes and reload shaders": "升级节点并重新加载着色器",
    "User attributes": "用户属性",
    "View only the current paint/mask": "仅查看当前绘制/蒙版",
    "Write to datafile changed": "数据文件写入已更改",
    "Write to rawfile changed": "原文件写入已更改",
    # ---- 着色器 / 灯光 / 插件分类标签 ----
    "Lighting/Standalone/Standard Lighting": "灯光/独立/标准灯光",
    "Lighting/Utils/Color To Vector": "灯光/工具/颜色转矢量",
    "Lighting/Utils/Lighting Result Modulation": "灯光/工具/灯光结果调制",
    "Lighting/Utils/Normal Modulation": "灯光/工具/法线调制",
    "Lighting/Utils/Tangent Space To Eye Space": "灯光/工具/切线空间转视线空间",
    "Misc./Slider Precision": "杂项/滑块精度",
    "Misc/Slider Precision/sliderPrecision": "杂项/滑块精度/sliderPrecision",
    "Misc/Bake Point": "杂项/烘焙点",
    "Misc/Channel Input": "杂项/通道输入",
    "Misc/Current Layer": "杂项/当前图层",
    "Misc/Set Unlit": "杂项/设为无光照",
    "Misc/Set Vector": "杂项/设置矢量",
    "Misc/Smart Mask": "杂项/智能蒙版",
    "Misc/Vector Split": "杂项/矢量拆分",
    "Mari/Onscreen Controls/": "Mari/屏幕控制/",
    "Mari/Onscreen Controls/Adjust": "Mari/屏幕控制/调整",
    # ---- 对话框/提示 ----
    "Affiliation Changed": "隶属关系已更改",
    "All licenses in use": "所有许可证都在使用中",
    "All licenses were installed successfully": "所有许可证均已成功安装",
    "Application Exit": "应用程序退出",
    "Incompatible source and destination paths": "源路径与目标路径不兼容",
    "Keeping existing image set": "保留现有图像集",
    "Sorry. Not quite working": "抱歉，尚未正常工作",
    "System information:": "系统信息：",
    "Technical description :": "技术说明：",
    "Unwritable Files": "不可写文件",
    "Unwritable files:": "不可写文件：",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX2.items():
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
