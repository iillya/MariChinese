#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""对全量宽泛候选做关键词式挖掘：抓 短标签 + 提及界面名词 的潜在 UI。"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BROAD = ROOT / "all_ui_candidates_broad.txt"
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


ENGINE = re.compile(
    r"("
    r"0x|\{|\}|\%z|::|->|\bNULL\b|\bptr\b|\bpointer\b|\bvec[234]\b|\bmat[234]\b"
    r"|OpenSSL|libcurl|CURL|X509|TLS\b|SSL\b|OCSP|CRL\b|Cipher|PRIVATE KEY|PUBLIC KEY|PARAMETERS|routines|curve over|DSTU|GOST|WTLS|X9\.|SECG|KDC|Kerberos|TACACS|PKCS|PRNG|CryptoAPI|DSO\b"
    r"|SOCKS|SSH\b|CONNECT|Client hello|Client key exchange|FTP\b|SMTP|TFTP|EPSV|EHLO|HTTP|https|URL\b|socket|Socket|chunked|Transfer-Encoding|Content-Type|Content-Length|User-Agent|Bearer|Authorization|TFC\b|SRV\b|RCODE|hostid|Hostid|RLM\b|RLMSTAT|RLM_ROAM|Entitlement|entitlement|fulfillment"
    r"|Usd\b|Sdf\b|Tf\b|HdSt|Hdx|Hgi\b|Hio\b|Glf\b|Storm\b|Osd\b|OpenSubdiv|Rprim|drawItem|DrawItem|DrawTarget|ExtComputation|scene index|render index|primvar|Primvar|BoundingBox|bounding box|ArTimestamp|SdfLayer|VtDictionary|Vt\b|OpenVDB|Hd\b"
    r"|Buffer Object|Framebuffer Object|Vertex Array Object|Texture Target|texture object|texel|GL_\b|GLSL|GL_R|GL_[A-Z]+|FBO\b|VAO\b|mipmap|Mip-?Map|Bindless|persistent mapping"
    r"|Data Block Manager|Datablock Manager|Hash Manager|Captured Malloc|DirtyList|Live Blocks|managed blocks|has live|cleanup|LRU\b|rebind|useRange|Malloc|Iterator|iterator|Accessor|accessor|hash table|corpus|Lifeboat|dentry|uuid\b|UtId|Gid\b|Uid\b"
    r"|Floating-Point|IEEE Floating|Unsigned 16-bit|Unsigned 24-bit|Unsigned 32-bit|Unsigned 8-bit|Four CC|R8G8B8|R3G3B2|R16F|R32F|A1R5G5B5|G16R16F|G32R32F|X1R5G5B5|R9G9B9|DXT[0-9]|OSD_REAL|%zu|%zd|AAAA\b|UTF-8|UTF8|hex|Hex|CRC|crc"
    r")",
    re.I,
)


UI_N = re.compile(
    r"("
    r"\bPalette\b|\bPalettes\b|\bShelf\b|\bShelves\b|\bLayer\b|\bLayers\b|\bChannel\b|\bChannels\b|\bBrush\b|\bBrushes\b"
    r"|\bCamera\b|\bCameras\b|\bTool\b|\bTools\b|\bView\b|\bWindow\b|\bProject\b|\bProjects\b|\bImage\b|\bImages\b"
    r"|\bMask\b|\bMasks\b|\bFilter\b|\bFilters\b|\bPreset\b|\bPresets\b|\bShortcut\b|\bShortcuts\b|\bTag\b|\bTags\b|\bTab\b|\bTabs\b"
    r"|\bNode\b|\bNodes\b|\bGeometry\b|\bObject\b|\bObjects\b|\bPatch\b|\bPatches\b|\bPaint\b|\bPainting\b|\bBake\b|\bBaked\b"
    r"|\bMaterial\b|\bTexture\b|\bTextures\b|\bUV\b|\bEnvironment\b|\bLight\b|\bLights\b|\bRender\b|\bFrame\b|\bGroup\b|\bGroups\b"
    r"|\bSelection\b|\bViewport\b|\bCanvas\b|\bProjector\b|\bLocator\b|\bBackdrop\b|\bCurve\b|\bGradient\b|\bGizmo\b"
    r"|\bImport\b|\bExport\b|\bSave\b|\bLoad\b|\bOpen\b|\bClose\b|\bCreate\b|\bDelete\b|\bRemove\b|\bAdd\b|\bApply\b|\bSelect\b"
    r"|\bRename\b|\bDuplicate\b|\bCopy\b|\bPaste\b|\bZoom\b|\bFit\b|\bToggle\b|\bSet\b|\bReset\b|\bEnable\b|\bDisable\b"
    r"|\bShow\b|\bHide\b|\bPlay\b|\bStop\b|\bRecord\b|\bAssign\b|\bFix\b|\bNudge\b|\bNew\b|\bDefault\b|\bCustom\b|\bRecent\b"
    r"|\bClear\b|\bRefresh\b|\bSearch\b|\bDock\b|\bFloat\b|\bPin\b|\bUnpin\b|\bExpand\b|\bCollapse\b|\bVerify\b|\bUpgrade\b|\bConvert\b|\bFlatten\b|\bCache\b|\bUncache\b|\bSync\b|\bRecompose\b|\bOptimize\b"
    r")",
    re.I,
)


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    keys = set(doc["translations"])
    rows = [s.strip() for s in BROAD.open(encoding="utf-8") if s.strip() and not s.strip().startswith("#")]
    cand = [s for s in rows if s not in keys]

    ui = []
    for s in cand:
        if len(s) < 2 or len(s) > 75:
            continue
        if ENGINE.search(s):
            continue
        if not re.match(r"^[A-Za-z][A-Za-z0-9 &%_:.!',\"\-\/\u2019()]*$", s):
            continue
        if not s[0].isupper():
            continue
        # 短标签 或 提及界面名词
        words = s.split()
        if len(words) <= 6 and re.search(r"^[A-Za-z][A-Za-z0-9 &%\-\u2019]*$", s):
            ui.append(s)
        elif UI_N.search(s):
            ui.append(s)

    ui.sort()
    with open(ROOT / "keyword_ui_candidates.txt", "w", encoding="utf-8") as fh:
        for s in ui:
            fh.write(s + "\n")
    print("关键词式挖掘候选:", len(ui))
    print("written to keyword_ui_candidates.txt")
    for s in ui:
        print(repr(s))


if __name__ == "__main__":
    main()
