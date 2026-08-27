#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第七十九批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX79 = {
    "Group": "组",
    "Groups": "组",
    "Group Name": "组名称",
    "Group Label": "组标签",
    "Group Color": "组颜色",
    "Group Icon": "组图标",
    "Group Type": "组类型",
    "Group Size": "组大小",
    "Group Count": "组数量",
    "Group Items": "组项目",
    "Group Content": "组内容",
    "Group Members": "组成员",
    "Group Selection": "组选择",
    "Group List": "组列表",
    "Group Stack": "组堆叠",
    "Group Editor": "组编辑器",
    "Group Folder": "组文件夹",
    "Group Browser": "组浏览器",
    "Group Library": "组库",
    "Group Preset": "组预设",
    "Group Settings": "组设置",
    "Group Options": "组选项",
    "Group Properties": "组属性",
    "Group Visibility": "组可见性",
    "Group Visible": "组可见",
    "Group Invisible": "组不可见",
    "Group Locked": "组已锁定",
    "Group Unlocked": "组已解锁",
    "Group Expanded": "组已展开",
    "Group Collapsed": "组已折叠",
    "Group Enabled": "组已启用",
    "Group Disabled": "组已禁用",
    "Group Solo": "组独奏",
    "Group Mute": "组静音",
    "Add Group": "添加组",
    "Remove Group": "移除组",
    "Delete Group": "删除组",
    "Rename Group": "重命名组",
    "Duplicate Group": "复制组",
    "Copy Group": "复制组",
    "Paste Group": "粘贴组",
    "Move Group": "移动组",
    "Select Group": "选择组",
    "Deselect Group": "取消选择组",
    "Edit Group": "编辑组",
    "Show Group": "显示组",
    "Hide Group": "隐藏组",
    "Collapse Group": "折叠组",
    "Expand Group": "展开组",
    "Lock Group": "锁定组",
    "Unlock Group": "解锁组",
    "Enable Group": "启用组",
    "Disable Group": "禁用组",
    "Solo Group": "独奏组",
    "Mute Group": "静音组",
    "Unmute Group": "取消静音组",
    "Sort Group": "排序组",
    "Search Group": "搜索组",
    "Group Sort": "组排序",
    "Group Search": "组搜索",
    "Group Create": "创建组",
    "Group Add": "添加组",
    "Group Remove": "移除组",
    "Group Delete": "删除组",
    "Group Rename": "重命名组",
    "Group Duplicate": "复制组",
    "Group Copy": "复制组",
    "Group Move": "移动组",
    "Group Align": "对齐组",
    "Group Arrange": "排列组",
    "Group Distribute": "分布组",
    "Group Reorder": "重新排序组",
    "Group Order": "组顺序",
    "Group Level": "组级别",
    "Group Depth": "组深度",
    "Group Parent": "父组",
    "Group Child": "子组",
    "Group Root": "根组",
    "Group Leaf": "叶组",
    "Group Node": "组节点",
    "Group Tree": "组树",
    "Group Hierarchy": "组层级",
    "Group Path": "组路径",
    "Group Location": "组位置",
    "Group Origin": "组原点",
    "Group Bounds": "组范围",
    "Group Extent": "组范围",
    "Group Area": "组区域",
    "Group Size": "组大小",
    "Group Width": "组宽度",
    "Group Height": "组高度",
    "Group Depth": "组深度",
    "Group Opacity": "组不透明度",
    "Group Alpha": "组 Alpha",
    "Group Color Space": "组颜色空间",
    "Group Grading": "组调色",
    "Group Look": "组外观",
    "Group Filter": "组滤镜",
    "Group Layer": "组图层",
    "Group Mask": "组蒙版",
    "Group Clipping": "组裁剪",
    "Group Clip": "组裁剪",
    "Group Blend": "组混合",
    "Group Composite": "组合成",
    "Group Composite Mode": "组合成模式",
    "Group Metadata": "组元数据",
    "Group Tag": "组标签",
    "Group Tags": "组标签",
    "Group Notes": "组备注",
    "Group Status": "组状态",
    "Group State": "组状态",
    "Group Active": "组活动",
    "Group Inactive": "组非活动",
    "Group Current": "当前组",
    "Group Default": "默认组",
    "Group Custom": "自定义组",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX79.items():
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
