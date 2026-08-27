#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第七十八批：常用界面词补充，翻译并入。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


T_EX78 = {
    "Note": "备注",
    "Notes": "备注",
    "Note Editor": "备注编辑器",
    "Note Text": "备注文本",
    "Note Name": "备注名称",
    "Note Label": "备注标签",
    "Note Color": "备注颜色",
    "Note Content": "备注内容",
    "Note Added": "已添加备注",
    "Note Updated": "备注已更新",
    "Note Deleted": "备注已删除",
    "Add Note": "添加备注",
    "Edit Note": "编辑备注",
    "Remove Note": "移除备注",
    "Delete Note": "删除备注",
    "Update Note": "更新备注",
    "Save Note": "保存备注",
    "Clear Note": "清除备注",
    "New Note": "新建备注",
    "Comments": "注释",
    "Comment": "注释",
    "Comment Text": "注释文本",
    "Comment Name": "注释名称",
    "Comment Label": "注释标签",
    "Add Comment": "添加注释",
    "Edit Comment": "编辑注释",
    "Remove Comment": "移除注释",
    "Delete Comment": "删除注释",
    "Update Comment": "更新注释",
    "New Comment": "新建注释",
    "Comment added": "已添加注释",
    "Comment updated": "注释已更新",
    "Comment deleted": "注释已删除",
    "Comments count": "注释数量",
    "Commented": "已注释",
    "Uncommented": "未注释",
    "Annotation": "标注",
    "Annotations": "标注",
    "Annotation Tool": "标注工具",
    "Annotation Text": "标注文本",
    "Add Annotation": "添加标注",
    "Remove Annotation": "移除标注",
    "Edit Annotation": "编辑标注",
    "Delete Annotation": "删除标注",
    "New Annotation": "新建标注",
    "Annotated": "已标注",
    "Unannotated": "未标注",
    "Tag": "标签",
    "Tagged": "已标记",
    "Untagged": "未标记",
    "Bookmark": "书签",
    "Bookmarks": "书签",
    "Add Bookmark": "添加书签",
    "Remove Bookmark": "移除书签",
    "Go to Bookmark": "转到书签",
    "Next Bookmark": "下一个书签",
    "Previous Bookmark": "上一个书签",
    "Bookmark This": "设为此为书签",
    "Bookmarked": "已加书签",
    "Unbookmarked": "未加书签",
    "Favorite": "收藏",
    "Favorites": "收藏",
    "Add to Favorites": "添加到收藏",
    "Remove from Favorites": "从收藏移除",
    "Favorite This": "收藏此项",
    "Mark Favorite": "标记收藏",
    "Favorite Items": "收藏的项目",
    "Favorited": "已收藏",
    "Unfavorited": "未收藏",
    "Star": "加星",
    "Starred": "已加星",
    "Unstarred": "未加星",
    "Star This": "为此加星",
    "Pin": "固定",
    "Pinned": "已固定",
    "Unpinned": "未固定",
    "Pin This": "固定此",
    "Unpin This": "取消固定此",
    "Pin to Top": "固定到顶部",
    "Pin to Panel": "固定到面板",
    "Unpin from Panel": "从面板取消固定",
    "Flag": "标记",
    "Flagged": "已标记",
    "Unflagged": "未标记",
    "Flag This": "标记此",
    "Mark Flagged": "标记为已标记",
}


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    added = []
    existed = []
    for k, v in T_EX78.items():
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
