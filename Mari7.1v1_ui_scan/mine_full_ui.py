#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""针对全量宽泛候选(all_ui_candidates_broad.txt)做更彻底的真UI筛选。"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BROAD = ROOT / "all_ui_candidates_broad.txt"
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


TECH = re.compile(
    r"("
    r"::|->|0x|\{|\}|\%z|nul byte|Nul byte"
    # OpenGL / 图形 / Slang内部
    r"|\bBuffer Object\b|\bFramebuffer Object\b|\bVertex Array Object\b|\bTexture Target\b|\bTexture ID\b"
    r"|\btexture object\b|\btexture unit\b|\btexture format\b|\btexel\b|\bmipmem\b|\bmipmap\b|\bGL_\b|\bGLSL\b|\bFBO\b|\bVAO\b"
    r"|\bHdSt\b|\bHdx\b|\bHgi\b|\bHd\b|\bStorm\b|\bOsd\b|\bOpenSubdiv\b|\bRprim\b|\bdrawItem\b|\bDrawItem\b|\bExtComputation\b"
    r"|\bUsd\b|\busd\b|\bSdf\b|\bTf\b|\bHio\b|\bGlf\b|\brender index\b|\bscene index\b|scene delegate|\bBoundingBox\b"
    # 加密 / 证书 / TLS / OpenSSL
    r"|\bX509|\bTLS|\bSSL|\bOCSP|\bCRL\b|\bCipher\b|\bcipher\b|\bPRIVATE KEY\b|\bPUBLIC KEY\b|\bPARAMETERS\b|\broutines\b"
    r"|\bcurve over\b|\bCertificate\b|\bcertificate\b|\bSubject\b|\bIssuer\b|\bAuthority\b|\bSigning\b|\bSignature\b|\bhase\b"
    r"|\bCSP\b|\bKey Identifier\b|\bCert Type\b|\bEncipher\b|\bDecipher\b|\bCryptoAPI\b|\bPRNG\b|\bDSO\b|\bDsa\b|\bDSTU\b|\bGOST\b"
    r"|\bPKCS\b|\bKDC\b|\bKerberos\b|\bTACACS\b|\bNIST CURVE\b|\bSECG\b|\bWTLS\b|\bX9\." # 刻意保留证书名
    # 网络 / 协议流程
    r"|\bSOCKS\b|\bSSH\b|\bCONNECT\b|\bClient hello\b|\bClient key exchange\b|\bFTP\b|\bSMTP\b|\bTFTP\b|\bEPSV\b|\bEHLO\b"
    r"|\bHTTP\b|\bhttps\b|\bURL\b|\bproxy\b|\bProxy\b|\bsocket\b|\bSocket\b|\bchunked\b|\bTransfer-Encoding\b|\bContent-Type\b"
    r"|\bContent-Length\b|\bUser-Agent\b|\bBearer\b|\bAuthorization\b|\bAes\b|\bAES\b|\bSession\b|\bsession\b|\bMailbox\b|\bUIDVALIDITY\b"
    r"|\bRLM\b|\bRLMSTAT\b|\bRLM_ROAM\b|\bRoam\b|\broam\b|\bhostid\b|\bHostid\b|\bfulfillment\b|\bEntitlement\b|\bentitlement\b|\bproduct length\b"
    # 引擎 / 底层管理器 / 哈希 / 清理日志
    r"|\bData Block Manager\b|\bDatablock Manager\b|\bHash Manager\b|\bCaptured Malloc\b|\bDirtyList\b|\bLive Blocks\b"
    r"|\bmanaged blocks\b|\bhas live\b|\bcleanup\b|\bAfter cleanup\b|\bMalloc\b|\bLRU\b|\brebind\b|\buseRange\b|\bDbuffer\b"
    r"|\bIterateur\b|\bIterator\b|\bIterat\b|\bAdress\b|accessor|\bAccessor\b|\bcorpus\b|\bBaking\b|\bCompute\b|\bCached\b"
    # 纯格式 / 数值 / 十六进制 / 枚举串
    r"|\bFloating-Point\b|\bIEEE Floating|\bUnsigned 16-bit|\bUnsigned 24-bit|\bUnsigned 32-bit|\bUnsigned 8-bit|\bFour CC\b"
    r"|\bR8G8B8|\bR3G3B2|\bR16F|\bR32F|\bA1R5G5B5|\bG16R16F|\bG32R32F|\bX1R5G5B5|\bR9G9B9|\bDXT[0-9]\b|\bOSD_REAL\b|\b%zu\b"
    r"|\bAAAA|\bMachine\b|\bACRES\b|\bOID\b|\bTUID\b|\bEFI\b|\bIX\b|\bMRPE\b|\bSig\b|\bMax\b"
    # 人名（抽样）
    r"|\bJack \b|\bJames \b|\bJohn \b|\bJon \b|\bJordan \b|\bJorel \b|\bKate \b|\bKevin \b|\bKiyoyuki|\bLaurent\b|\bLeigh\b|\bLuma\b"
    r"|\bMarcus \b|\bMariano|\bMark \b|\bMatt \b|\bMichal\b|\bMike \b|\bMorgan\b|\bNapoleon\b|\bNathalie\b|\bPhilip\b|\bYann\b|\bSibi\b"
    r")",
    re.I,
)


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    keys = set(doc["translations"])

    rows = [s.strip() for s in BROAD.open(encoding="utf-8") if s.strip() and not s.strip().startswith("#")]
    cand = set(rows) - keys

    ui = []
    for s in cand:
        if len(s) < 2 or len(s) > 90:
            continue
        if TECH.search(s):
            continue
        # 界面文本一般以字母开头、由单词/空格/常用标点组成
        if not re.match(r"^[A-Za-z][A-Za-z0-9 &%_:.!'\",\-/\u2019()\u00b0]*$", s):
            continue
        ui.append(s)

    ui.sort()
    with open(ROOT / "full_ui_candidates.txt", "w", encoding="utf-8") as fh:
        for s in ui:
            fh.write(s + "\n")
    print("broad total:", len(rows))
    print("已在词典:", len(rows) - len(cand))
    print("全量宽泛 - 词典 未收录:", len(cand))
    print("过滤后真 UI 候选:", len(ui))


if __name__ == "__main__":
    main()
