#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""列出 extra_ui_genuine.txt 中尚未进入词典的词条，供继续挑选合并。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"

with open(DICT, encoding="utf-8") as fh:
    doc = json.load(fh)
keys = set(doc["translations"])

rows = [s.strip() for s in (ROOT / "sure_ui_candidates.txt").open(encoding="utf-8") if s.strip()]
remaining = [s for s in rows if s not in keys]

print("已收录/候选总数:", len(rows), "  未收录:", len(remaining))
for s in remaining:
    print(repr(s))
