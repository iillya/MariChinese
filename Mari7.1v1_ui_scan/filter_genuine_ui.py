#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 extra_ui_candidates.txt 中的真 UI 词条进一步筛选出来，供翻译合并。"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "extra_ui_candidates.txt"


BAD = re.compile(
    r"("
    # 密钥/证书/加密
    r"PRIVATE KEY|PUBLIC KEY|PARAMETERS|routines|curve over|Compromise|Signing Tool|Time Stamping|Cipher|CRYPTO"
    r"|CRL\b|OCSP|X509|Netscape|CSPs|CSP\b|Trust\b|Key Identifier|Cert Type|Certification|S/MIME|PKINIT|PKCS12|PSS\b"
    r"|CMK\b|CMC\b|CRMF\b|CMS\b|DH \b|DSA\b|EC \b|RSA|WTLS|GOST|DSTU|X9\.|SECG|RPKI|BGPsec|Autonomous|Asynchronous"
    r"|Barings|Extranet|Permanent Identifier|Routing Domain|Brand Indicator|Policy Qualifier|E-mail Protection"
    r"|Class of Signing|KDC Response|KDC\b|Kerberos|TACACS|Encipher|Decipher|Signature Algorithm|Digest Algorithm"
    # 网络/协议/传输
    r"|SOCKS|SSH\b|CONNECT|Client hello|Client key exchange|10Duke|RLM\b|RLMSTAT|RciSDK|Teleport|User-Agent"
    r"|Content-Type|Content-Length|Transfer-Encoding|chunked|Proxy-Connection|Authorization|Bearer|IPv6|IPSec"
    r"|AD Time Stamping|Cessation|Withdrawn|Biometric|SynContext|R4di0|Anonymous|Encoded|ASN\b|X400|E-mail|SMTP"
    r"|FTP\b|TFTP|syslog|EFI\b|SRV\b|NTS\b|mTLS|BPK\b|CT Precertificate|Huffman|BEP\b|THP\b|PEAK\b|q9|Pwd|pwd"
    # USD / Hydra / Hd / Sdf / Tf / Osd / Storm / SVT / OIT
    r"|HdSt|Hdx|Hgi|Hd\b|Hd\b|Sdf|Tf\b|Pcp\b|Ndr|Vt\b|Hio|Glf|Gf\b|Ar\b|OpenSubdiv|Osd\b|Storm\b|Usd|Svt|SVT|OIT\b"
    r"|draw batch|drawBatches|DrawBatch|Dispatch Buffer|Deferred Quad|Primvars|BoundingBox|Bounding box|Indirect draw"
    r"|GpuComputation|ExtComputation|Computations|Gpu Memory|Tile Memory|drawTarget|DrawTarget|scene delegate|render index"
    # 引擎/底层
    r"|DDI\b|DDI_|Ptex|Ptex\b|VDB|Glsl|GLSLFX|Shader Network|ShaderBall|Packing Ptex|Prepare For Ptex|Sdf\b"
    r"|Nuke\b|Mri[A-Za-z]+\b|QtLockedFile|ArchMallocHook|SIC_REGISTRY|SysUpdate|Xfer|xfer|DSO|Dso|AES|ENGINE\n"
    # 纯数值/位深/宏/单大写缩写
    r"|^[A-Z]{2,5}$|BitDepth|Floating-Point|Unsigned 8-bit|Unsigned 16-bit|Unsigned 32-bit|IEEE Floating|DXT[0-9]"
    r"|R8G8B8|R3G3B2|R9G9B9|R16F|R32F|A1R5G5B5|G16R16F|G32R32F|X1R5G5B5|BYTE MACRO|BIT STRING|OCTET STRING|EXTEND ASCII"
    r"|BMP JPEG|SIZE    COUNT|GPU/|CPU Num|CPU Tile|OSD_REAL|%zu|_MRI_|_error|TESTING TEST"
    # 人名 / 署名
    r"|Adrian |Antoni|Akira|Borna|Bradford|Carlos|Charli|Charlie|Chloe|Chris |Daniel |Duncan|Eija|Emeline|Erica"
    r"|Gabriel|Johnny|Stuart|Ollie|Peppe|Phil |Piotr|Rachel|Rajiv|Ravishankar|Robert|Rory|Sibi|Tim |Timothy|Vanessa"
    r"|William|Yann|Nayer|Carl Rand|F6LHJt|Minds|Biometrics|CPE\b|TUI\b|OID\b|WAP\b|The Foundry|Visionmongers"
    r")",
    re.I,
)


rows = [l.strip() for l in open(SRC, encoding="utf-8") if l.strip()]
gen = [s for s in rows if not BAD.search(s)]

# 第二轮：剔除仍有明显“引擎/日志/代码/网络”特征的项目
BAD2 = re.compile(
    r"("
    r"EOF on|Call |Calling |Callbacks?|Callback |Blocking call|Call Sites|argument|prematurel|Exit Code|Expect:|Exp length"
    r"|Auth product|Auth ver|Encrypted Extensions|Enter PEM|END OF RECORD|FILE pointer|FN_ENT|EEEE|Diagnostic|Deferring"
    r"|Data Blocks|Datablock|Dirty list|DirtyList|Consult|Convolve|Convolve Dst|Convolve Src|\bBuffer( Memory| Source)?\b"
    r"|Array Buffer|Element Array|Compile Dispatch|Gather buffer|Pixel Pack|Pixel UnPack|Draw Dirty|Draw geometry|Drawing Array|Drawing Element"
    r"|Fail to compile|Fail to link|Corrupt|crate file|malformed|Escape sequence|hexadecimal|regex|property escape|Backreference"
    r"|JSON|texture object|texture unit|texture format|looks like|does not effect|Extra Read|Extra path|Semaphore|Iteration|Advisory|Advice"
    r"|Advising|Internal |Dynamic engine|Softwar engine|Resource binder|Enumerat|\bDoing linlog\b|PUSHING cached|Supplied list"
    r"|Failed|Failure|Invaild|Invalid|Bad |No argument|Cannot |Couldn|Could not|Unable|Missing |Not enough|Exception|Assert|Stack"
    r"|Insufficient|Account|signature|Abort|Aborted|Cancel|Cancell|Disconnect|Connect |connect |Request|Reject|Refused|Timeout|Timed out"
    r"|Busy|Wait|Waiting|Denied|Forbidden|Fenced|Permission|Unlicensed|timezone|inactive|Not currently|No project|Target memory"
    r"|Memory|Mem Cache|Disk|Cache|Cached|caching|Remember|history|History|Heap|Query|Queries|Statistic|Stats|Status|Revision|Expire date|Days Remaining"
    r"|Very |Too |Out of |no such|no current|no available|no valid|no data|There is no|There are no|There was no|One of|More than|Nothing"
    r"|Imported|Export|Added|Remove|Removed|Renamed|Dropped|Loaded|Saved|Deleted|Created|Updated|Edited|Wrote|Completed|In progress|Finished|Done|Results|Errors were"
    r")",
    re.I,
)

# 只保留很像“菜单/按钮/选项/面板名”的短语：短、非以冒号结尾的纯标签
def is_label(s):
    if len(s.split()) > 5:
        return False
    wc = len(s.split())
    # 4 词以上且长度过大的多半是帮助/提示句
    if wc >= 4 and len(s) > 42:
        return False
    return True

gen2 = []
for s in gen:
    if BAD2.search(s):
        continue
    if not is_label(s):
        continue
    gen2.append(s)

with open(ROOT / "extra_ui_genuine.txt", "w", encoding="utf-8") as fh:
    for s in gen2:
        fh.write(s + "\n")
for f in (ROOT / "extra_ui_genuine.txt",):
    pass

print("final UI candidates:", len(gen2))
print("--- final(前300) ---")
for s in gen2[:300]:
    print(repr(s))
