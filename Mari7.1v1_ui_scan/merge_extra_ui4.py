#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第四批：从全量候选里人工挑出的“确定用户可见”提示/错误/确认句，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX4 = {
    # 名称冲突 / 确认
    "A Preset Called %1 already exists, please pick a unique name": "名为 %1 的预设已存在，请选择唯一的名称",
    "A Toolbar with that name already exists": "已存在同名工具栏",
    "A shelf with that name already exists": "已存在同名架子",
    "A shelf with the name '%1' already exists.": "名为 '%1' 的架子已存在。",
    "A project called '%1' already exists.": "名为 '%1' 的项目已存在。",
    "A group called '%1' is already present at the location '%2'.": "名为 '%1' 的组已存在于位置 '%2'。",
    "A locked group called '%1' is already present at the location '%2'.": "名为 '%1' 的锁定组已存在于位置 '%2'。",
    "A shelf called '%1' is already present at the location '%2'.": "名为 '%1' 的架子已存在于位置 '%2'。",
    "An input with the name %1 already exists in this group.": "此组中已存在名为 %1 的输入。",
    "An output with the name %1 already exists in this group.": "此组中已存在名为 %1 的输出。",
    "An object with that name already exists": "已存在同名对象",
    "Do you really want to delete this collection": "你真的想删除此集合吗",
    "All channels to be created must have non-empty name": "要创建的所有通道都必须有非空名称",
    "New channels must have a name.": "新通道必须有名称。",
    "New palettes must be given a name": "必须为新面板提供名称",
    "Only one object can be selected": "只能选择一个对象",
    "At least one object must be selected": "至少必须选择一个对象",
    "At least one mesh path must be supplied": "至少必须提供一个网格路径",
    "At least one version must be maintained": "至少必须保留一个版本",
    # 分配 / 赋值操作
    "Assign a keyboard shortcut to this item": "为此项目分配键盘快捷键",
    "Assign keyboard shortcuts to selected item(s)": "为所选项目分配键盘快捷键",
    "Assign thumbnails to selected item(s)": "为所选项目分配缩略图",
    "Cache Layer : %1": "缓存图层：%1",
    "Convert Channel : %1 to %2": "转换通道：%1 到 %2",
    "Convert Procedural to Paintable : %1": "将程序化转换为可绘制：%1",
    "Delete Cache : %1": "删除缓存：%1",
    "Delete selected item(s)": "删除所选项目",
    "Export selected item(s) to file": "将所选项目导出到文件",
    "Enter an Activation Key": "输入激活密钥",
    "Enter your Activation Key below": "在下方输入你的激活密钥",
    "Show Error Dialog": "显示错误对话框",
    "Set the number of active directional lights": "设置活动定向灯光的数量",
    "Set the blend mode to clear": "将混合模式设置为清除",
    "Set delay amount for Steady Stroke.": "设置平稳笔画的延迟量。",
    "Set mode for Steady Stroke.": "设置平稳笔画的模式。",
    # 编辑类错误（关于项目/图层/架子/图像/节点）
    "Cannot add new toolbar": "无法添加新工具栏",
    "Cannot add unsaved image to shelf": "无法将未保存的图像添加到架子",
    "Cannot create a project when one is already open": "已有项目打开时无法创建项目",
    "Cannot create new project - input geometry files have invalid extension": "无法创建新项目——输入几何文件的扩展名无效",
    "Cannot delete locked shelves or groups": "无法删除锁定的架子或组",
    "Cannot duplicate a system shader.": "无法复制系统着色器。",
    "Cannot find a shortcut for the given path": "无法为给定路径找到快捷键",
    "Cannot find an action for the given shortcut": "无法为给定快捷键找到操作",
    "Cannot find default brushes directory": "无法找到默认笔刷目录",
    "Cannot find given project": "无法找到给定项目",
    "Cannot find file version": "无法找到文件版本",
    "Cannot remove a locked shelf": "无法移除锁定的架子",
    "Cannot remove all objects from the project (%1)": "无法移除项目中的所有对象（%1）",
    "Cannot remove the only version of the object": "无法移除对象的唯一版本",
    "Cannot rename project '%1'.  Sorry.": "无法重命名项目 '%1'。抱歉。",
    "Cannot pop out multiple shelves. Please select only one.": "无法弹出多个架子。请只选择一个。",
    "Cannot ungroup locked shelves or groups.": "无法取消锁定架子或组的分组。",
    "Cannot load more than one geo entity to be used as a new version.": "无法加载多个几何实体用作新版本。",
    "Cannot load more than one geo version to be used as a new version.": "无法加载多个几何版本用作新版本。",
    "Make Current Layer '%1' from Stack '%2'": "将堆栈 '%2' 中的 '%1' 设为当前图层",
    "Make New Toolbar": "新建工具栏",
    "Move the contents of this group to beside the group": "将此组的内容移动到组旁边",
    "Move the selected groups and shelves into a group": "将选中的组和架子移入一个组",
    "Move this input down in the list of inputs.": "将此输入在输入列表中下移。",
    "Move this input up in the list of inputs.": "将此输入在输入列表中上移。",
    "Remove Input %1 from Node : %2": "从节点 %2 移除输入 %1",
    "Remove Node : %1": "移除节点：%1",
    "Resize node %1": "调整节点 %1 的大小",
    "Resized %1 images to project maximum resolution": "已将 %1 张图像调整为项目最大分辨率",
    "Resized %1 patches in total": "共调整了 %1 个面片的大小",
    # 状态 / 对话框提示
    "Saved to project directory": "已保存到项目目录",
    "Save Painting Failed": "保存绘制失败",
    "Open Image Failed": "打开图像失败",
    "Paste Operation Failed": "粘贴操作失败",
    "Error adding new version": "添加新版本时出错",
    "Error baking mask stack": "烘焙蒙版堆栈时出错",
    "Error loading archive": "加载归档时出错",
    "Error popping out shelf": "弹出架子时出错",
    "Some filters were missing and have been removed from the project.": "部分滤镜缺失并已从项目中移除。",
    "Some layer settings may be lost when converting projects": "转换项目时部分图层设置可能会丢失",
    "The following errors were encountered during image loading:": "加载图像时遇到以下错误：",
    "The file does not exist": "文件不存在",
    "The given image does not exist: '%1'": "给定图像不存在：'%1'",
    "The layer stack up to this layer cannot be cached.": "到此图层的图层堆栈无法缓存。",
    "The layer that contains this stack is locked.": "包含此堆栈的图层已锁定。",
    "The layer has no parent channels": "此图层没有父通道",
    "The layer stack has no parent channels": "此图层堆栈没有父通道",
    "The project directory is not recognized as a valid Mari project location.": "项目目录未被识别为有效的 Mari 项目位置。",
    "The project failed to save.": "项目保存失败。",
    "The project must be saved before clearing history": "清除历史前必须先保存项目",
    "The shortcut '%1' is invalid": "快捷键 '%1' 无效",
    "The shortcut '%1' is reserved and cannot be assigned": "快捷键 '%1' 为保留键，无法分配",
    "The shortcut is empty": "快捷键为空",
    "The smart mask group does not contain any output.": "智能蒙版组没有输出。",
    "The value is beyond the maximum picker value specified in the preferences": "值超出了偏好设置中指定的最大拾取值",
    "The maximum color intensity that can be chosen in the color picker.": "可在颜色选择器中选择的最大颜色强度。",
    # 许可证 / 安装对话框
    "Choose your type of local RLM license": "选择你的本地 RLM 许可证类型",
    "The Activation Key could not be activated.": "激活密钥无法激活。",
    "The Activation Key was successfully activated.": "激活密钥已成功激活。",
    "The license does not support this feature.": "许可证不支持此功能。",
    "The license has expired.": "许可证已过期。",
    "The license is already installed.": "许可证已安装。",
    "You should install the Foundry Licensing Tools (FLT) and try again.": "你应该安装 Foundry 许可工具（FLT）然后再试。",
    "Non-commercial is only available for Release versions of Mari": "非商业版仅适用于 Mari 的发布版本",
    # 其他操作提示
    "Toggle between the different cursor types": "在不同光标类型之间切换",
    "Toggle lighting on main mesh to full with shadows": "将主网格灯光切换为完整并带阴影",
    "Toggle non-Ptex Canvases": "切换非 Ptex 画布",
    "Unable to apply filter": "无法应用滤镜",
    "Unable to convert to Custom Procedural Node": "无法转换为自定义程序化节点",
    "Unable to create Smart Mask node.": "无法创建智能蒙版节点。",
    "Unable to create material layer.": "无法创建材质图层。",
    "Unable to create smart mask layer.": "无法创建智能蒙版图层。",
    "Unable to create/access directory. Please try again as Administrator.": "无法创建/访问目录。请以管理员身份重试。",
    "Unable to load image.": "无法加载图像。",
    "Unable to save filter collection": "无法保存滤镜集合",
    "Unable to swap to 2D Paint mode - no 2D Paint object found.": "无法切换到 2D 绘制模式——未找到 2D 绘制对象。",
    "Unable to swap to 3D Paint mode - no 3D Paint object found.": "无法切换到 3D 绘制模式——未找到 3D 绘制对象。",
    "Warning: No Virtual Memory System detected.": "警告：未检测到虚拟内存系统。",
    "You must be an Administrator to perform this action.": "你必须以管理员身份执行此操作。",
    "Make a copy of the project prior to conversion.": "转换前请复制一份项目。",
    "Make an archive of the project prior to conversion.": "转换前请为项目创建归档。",
    "Please select the patch link group to which you want to link the patch.": "请选择要链接面片的链接组。",
    "Note that they will be permenantly removed from the project if it is saved.": "请注意，若保存项目，它们将被永久移除。",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX4.items():
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
