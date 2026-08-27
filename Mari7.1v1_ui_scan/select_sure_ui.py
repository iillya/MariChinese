#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从全量候选中筛出“八成确定上屏”的用户可见句子（排除引擎词，须像完整提示句）。"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BROAD = ROOT / "all_ui_candidates_broad.txt"
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


ENGINE = re.compile(
    r"("
    r"\bshader\b|\bshaders\b|\bShader\b|\bGLSL\b|\bbuffer\b|\bBuffer\b|\btexture\b|\bTexture\b|\bbindless\b|\bmipmap\b"
    r"|\bprim\b|\bPrim\b|\bprims\b|\bUsd\b|\bSdf\b|\bHd\b|\bHio\b|\bGlf\b|\bStorm\b|\bdrawItem\b|\bDrawTarget\b|\bFBO\b|\bVAO\b"
    r"|\bhandle\b|\bHandle\b|\bAPI\b|\bApi\b|\bapi\b|\bVtDictionary\b|\bVt\b|\bmalloc\b|\baccessor\b|\bAccessor\b"
    r"|\bnetwork\b|\bdatabase\b|\bDatabase\b|\bDB\b|\bGPU\b|\bCPU\b|\bOpenGL\b|\bOpenSubdiv\b|\bNdk\b|\bSDK\b"
    r"|\bplugin URI\b|\bresolver\b|\bArGetResolver\b|\bserver\b|\bServer\b|\bR4di0\b|\bdecode\b|\bdecode\b|\bcipher\b"
    r"|\bsession\b|\bSession\b|\bRoam\b|\broam\b|\btoken\b|\bToken\b|\bX509\b|\bTLS\b|\bOCSP\b|\bCRL\b|\bcert\b|\bCert\b"
    r"|\bcomms\b|\bComm\b|\bprotocol\b|\bProtocol\b|\bsocket\b|\bSocket\b|\bFTP\b|\bSMTP\b|\bMQTT\b|\bproxy\b|\bProxy\b"
    r"|\bexecutor\b|\bExecutor\b|\binstance\b|\bInstance\b|\bregistr\b|\bRegister\b|\bdirty\b|\bDirty\b|\bcompositor\b"
    r"|\bcomputed\b|\bComputed\b|\braymarch\b|\bSVT\b|\bOIT\b|\bDLSS\b|\bHgi\b|\bOsd\b|\bTfPyLock\b|\bClause\b"
    r")",
    re.I,
)


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    keys = set(doc["translations"])
    rows = [s.strip() for s in BROAD.open(encoding="utf-8") if s.strip() and not s.strip().startswith("#")]
    cand = [s for s in rows if s not in keys]

    pick = []
    for s in cand:
        if ENGINE.search(s):
            continue
        w = s.split()
        if len(w) < 3 or len(w) > 14:
            continue
        if len(s) > 110:
            continue
        if not s[0].isupper():
            continue
        if not re.match(r"^[A-Za-z][A-Za-z0-9 &%_:.!',\"\-\/\u2019()]*$", s):
            continue
        # 以动作/询问/提示类动词或"某某"类名词引导又像完整句子的优先
        if re.match(r"^(Please|Are you sure|Would you like|Do you|You (must|will|can|cannot|are|need|should)|Cannot |Can't |Could not|Failed to|An error|The |This will|Only |At least|A |An |Apply|Select|Open|Save|Load|Create|Delete|Remove|Add|Rename|Duplicate|Import|Export|Set|Reset|Enable|Disable|Hide|Show|Choose|Enter|Cancel|OK|Yes|No|Paste|Copy|Close|Warning|Error|Success|Progress|Done|All |No |One |Some |New |Existing|Missing|Invalid|Unable to|Try |Retry |Ignore |Skip |Go |Back |Next |Upgrade|Convert|Flatten|Cache|Uncache|Sync|Spawn|Dock|Toggle|Show/Hide|Make|Assign|Extract|Fit |Fix |Find |Activate|Install|Check|Search|Play|Record|Stop|Zoom|Pick|Pump|Purge|Resize|Move|Repackage|Regenerate)", s):
            pick.append(s)

    pick.sort()
    with open(ROOT / "sure_ui_candidates.txt", "w", encoding="utf-8") as fh:
        for s in pick:
            fh.write(s + "\n")
    print("八成确定上屏候选:", len(pick))
    print("written to sure_ui_candidates.txt")
    for s in pick:
        print(repr(s))


if __name__ == "__main__":
    main()
