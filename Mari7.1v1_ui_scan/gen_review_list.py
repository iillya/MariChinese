#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成“待确认的界面候选”清单：可能上屏的提示/错误/状态/确认句，排除明确内部日志。"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BROAD = ROOT / "all_ui_candidates_broad.txt"
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


# 明确内部/技术/非上屏的强排除
INTERNAL = re.compile(
    r"("
    # 内部对象校验 / 引擎日志
    r"Internal Mri|After emitting|After shutdown|After adding|Called |Calling |callback\b|callback\(|Aggregation strategy"
    r"|at the empty path|Accessor\b|accessor\b|Iterator\b|iterator\b|Subtree\b|subtree\b|dirty list|Dirty list|DirtyList|Repr "
    r"|dbuffer|DBuffer|uuid\b|UID\b|mriapp|logMetric|SdfLayer|sdfLayer|Usd\b|usd\b|Hydra|HdSt|Hdx|Hgi|Storm\b|Osd\b|OpenSubdiv"
    r"|prim\b|\bPrim\b|prims\b|Rprim|drawItem|DrawItem|ExtComputation|scene index|render index|BoundingBox|Bounding box"
    # 网络/协议/加密
    r"|SOCKS|SSH\b|CONNECT|Client hello|Client key exchange|FTP\b|SMTP|TFTP|EPSV|EHLO|HTTP|https|URL\b|proxy|Proxy|socket|Socket"
    r"|chunked|Transfer-Encoding|Content-Type|Content-Length|User-Agent|Bearer|Authorization|AES\b|Session\b|session\b|Mailbox|UIDVALIDITY"
    r"|RLM\b|RLMSTAT|RLM_ROAM|hostid|Hostid|fulfillment|Entitlement|entitlement|product length|server line|RLMCloud"
    r"|X509|TLS\b|SSL\b|OCSP|CRL\b|Cipher|cipher|PRIVATE KEY|PUBLIC KEY|PARAMETERS|routines|curve over|Certificate|certificate"
    r"|Subject\b|Issuer|Authority\b|Signing\b|Signature\b|Key Identifier|Cert Type|Encipher|Decipher|CryptoAPI|PRNG\b|PKCS|KDC|Kerberos|TACACS"
    # 底层管理器/哈希/数据块
    r"|Data Block Manager|Datablock Manager|Hash Manager|Captured Malloc|Malloc\b|LRU\b|rebind|useRange|has live|managed blocks|cleanup|After cleanup"
    # 纯格式/数值/十进制
    r"|Floating-Point|IEEE Floating|Unsigned 16-bit|Unsigned 24-bit|Unsigned 32-bit|Unsigned 8-bit|Four CC|R8G8B8|R3G3B2|R16F|R32F"
    r"|A1R5G5B5|G16R16F|G32R32F|X1R5G5B5|R9G9B9|DXT[0-9]|OSD_REAL|%zu|%zd|\bAAAA\b|NIST CURVE|DSTU|GOST|WTLS|X9\.|SECG"
    # 人名
    r"|Jack |James |John |Jon |Jordan |Jorel |Kate |Kevin |Kiyoyuki|Laurent|Leigh|Luma|Marcus |Mariano|Mark |Matt |Michal|Mike |Morgan"
    r"|Napoleon|Nathalie|Philip|Yann|Sibi|Adrian|Antoni|Akira|Borna|Bradford|Carlos|Charli|Charlie|Chloe|Chris |Daniel|Duncan|Eija"
    r"|Emeline|Erica|Gabriel|Johnny|Stuart|Ollie|Peppe|Phil |Piotr|Rachel|Rajiv|Ravishankar|Robert|Rory|Tim |Timothy|Vanessa|William"
    r")",
    re.I,
)


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    keys = set(doc["translations"])

    rows = [s.strip() for s in BROAD.open(encoding="utf-8") if s.strip() and not s.strip().startswith("#")]
    cand = [s for s in rows if s not in keys]

    # 高精度白名单：以“对话框/确认/错误”常见开头词开头，且不含内部技术词
    DIALOG_OPEN = re.compile(
        r"^("
        r"Please |Are you sure|Do you|Would you like|Do you want|You must|You will|You can|You are|You need|You have|You should|You chose|You cancelled|You selected"
        r"|Cannot |Can't |Could not|Couldn't|Unable to|Failed to|Failure |An error|The following|There was|There were|There is|There are|There was no|There are no"
        r"|Warning|Error:|Sorry|Select |Choose |Enter |Save |Load |Open |Close |Create |Delete |Remove |Add |Apply |Cancel |OK |Yes |No |Set |Reset |Rename |Duplicate |Import |Export |Hide |Show "
        r"|Only one|At least one|The |This |These |Those |That |These |Your |My |All |No |Some |One |More |New |Existing |Selected |Unselected |Visible |Hidden |Locked |Unlocked |Enabled |Disabled |Cached |Uncached"
        r")",
        re.I,
    )
    ui = []
    for s in cand:
        if INTERNAL.search(s):
            continue
        tokens = s.split()
        if len(tokens) < 3 or len(tokens) > 14:
            continue
        if len(s) > 110:
            continue
        if not DIALOG_OPEN.match(s):
            continue
        if not re.match(r"^[A-Za-z][A-Za-z0-9 &%_:.!',\"\-\/\u2019()]*$", s):
            continue
        ui.append(s)

    ui.sort()
    with open(ROOT / "review_ui_candidates.txt", "w", encoding="utf-8") as fh:
        for s in ui:
            fh.write(s + "\n")

    print("高精度待确认候选:", len(ui))
    print("written to review_ui_candidates.txt")
    print("--- 样例(全量, 前150) ---")
    for s in ui[:150]:
        print(repr(s))


if __name__ == "__main__":
    main()
