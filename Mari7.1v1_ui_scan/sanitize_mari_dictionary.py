#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从现有字典里剔除确定不是 UI 的词条（引擎/库/协议/内部校验等），并输出报告。"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DICT = ROOT.parent / "translations" / "dictionary_zh.json"


# 确定不是 UI 的强信号：跨二进制/引擎/协议/加密/OpenGL 状态内部串
# 仅剔除“铁定不会显示到界面”的内部/技术串；可作警告/提示/状态的词一律保留。
NON_UI = re.compile(
    r"("
    r"::|->|0x|\{|\}|\%zu|\%zd|\\n"  # 代码符号/格式符
    # OpenGL / 引擎状态内部（控制台日志）
    r"|\bBuffer Object is\b|\bBuffer Object needs\b|\bFramebuffer Object\b|\bVertex Array Object\b"
    r"|\bTexture Target is\b|\bnot bound on\b|\bhas already been set\b|\bhas not been bound\b"
    r"|\bGL_\b|\bGLSL\b|\bglsl\b|\bFBO\b|\bVAO\b|\bHdSt\b|\bHdx\b|\bHgi\b|\bRprims\b|\bRprim\b|\bdrawItems\b|\bdraw items\b"
    r"|\bExtComputation\b|\bHydra\b|\bOpenSubdiv\b|\bOsd\b|\bStorm\b|\busd imaging\b|\bUsdImaging\b|\bUsdStages\b|\bSdfLayer\b|\bSdf_PathNode\b|\bHio\b|\bGlf\b"
    # 加密 / 证书 / TLS / OpenSSL
    r"|\bX509|\bTLS|\bSSL|\bOCSP|\bCRL\b|\bCipher\b|\bcipher\b|\bPRIVATE KEY\b|\bPUBLIC KEY\b|\bPARAMETERS\b"
    r"|\broutines\b|\bcurve over\b|\bEncipher\b|\bKey Identifier\b|\bCert Type\b|\bDigest Algorithm\b"
    r"|\bCryptoAPI\b|\bDSO\b|\bPRNG\b|\bCESS\b|\bBIT STRING\b|\bOCTET STRING\b|\bBYTE MACRO\b|\bEXTEND ASCII\b"
    # 网络 / 协议 / 传输内部
    r"|\blibcurl\b|\bCURL\b|\bCURLOPT\b|Accept: |Content-Type:|Content-Length:|Transfer-Encoding:|chunked"
    r"|\bClient hello\b|\bClient key exchange\b|\bSOCKS\b|\bProxy-Connection:|User-Agent:"
    r"|\bRCODE\b|\bsocket\b|\bSocket has\b|\bEOF on\b|\bSRV\b|\bRLMSTAT\b|\bRLM_ROAM\b|\brehostable\b"
    r"|\bExp length bad\b|\bAuth product length\b|\bAuth ver length\b|\bAuthorization: Bearer\b|\bBearer\b"
    # 内部管理器 / 哈希 / 数据块 / 清理日志
    r"|\bData Block Manager\b|\bDatablock Manager\b|\bHash Manager\b|\bCaptured Malloc\b|\bDirtyList\b"
    r"|\bLive Blocks\b|\bmanaged blocks\b|\bhas live\b|\bcleanup\b|\bAfter cleanup\b|\bCache bucke\b"
    r"|\bcaptured malloc\b|\bmalloc\b|\bLRU\b|\brebind\b|\buseRange\b"
    # 纯格式/数值/十六进制串
    r"|\bFloating-Point 16-bit|\bFloating-Point 32-bit|\bIEEE Floating-Point|\bUnsigned 16-bit|\bUnsigned 24-bit"
    r"|\bUnsigned 32-bit|\bUnsigned 8-bit|\bFour CC 4-bit|\bFour CC 8-bit|\bR8G8B8|\bA8R8G8B8|\bA8B8G8R8"
    r"|\bX8R8G8B8|\bR6G6B6|\bR3G3B2|\bDXT[1-9]\b|OSD_REAL s,"
    r")",
    re.I,
)


def main():
    with open(DICT, encoding="utf-8") as fh:
        doc = json.load(fh)
    trans = doc["translations"]
    removed = []
    kept = {}
    for k, v in trans.items():
        if NON_UI.search(k):
            removed.append(k)
        else:
            kept[k] = v
    doc["translations"] = kept
    removed.sort()
    with open(DICT, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    with open(ROOT / "removed_non_ui.txt", "w", encoding="utf-8") as fh:
        fh.write("\n".join(removed))
        fh.write("\n")

    print(f"total before: {len(trans)}")
    print(f"removed (非 UI): {len(removed)}")
    print(f"kept (UI 保留): {len(kept)}")
    print(f"removed list -> removed_non_ui.txt")
    print("--- 移除内容样本(前80) ---")
    for r in removed[:80]:
        print(repr(r))


if __name__ == "__main__":
    main()
