#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""在宽泛候选（broad）里找出严格列表（strict）遗漏、且像是界面词条的项。"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load(p):
    s = set()
    for line in open(p, encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#"):
            s.add(line)
    return s


strict = load(ROOT / "all_ui_candidates.txt")
broad = load(ROOT / "all_ui_candidates_broad.txt")
rest = sorted(broad - strict)

# 界面上基本不会出现的“技术/代码/库”字眼（宽泛排除，宁可多留一些再做人工判断）
TECH = re.compile(
    r"("
    r"::|->|0x|\(|\)|;|\\|\bstruct\b|\bvoid\b|\bint\b|\bconst\b|\breturn\b|\bbool\b|\btrue\b|\bfalse\b"
    r"|PRIVATE KEY|PUBLIC KEY|PARAMETERS|routines|CERT|X509|TLS|SSL|CRL\b|OCSP|Cipher|cipher|signature|digest algorithm"
    r"|DSA\b|RSA|EC PARAM|WTLS|X9\.|SECG|curve over|Authority|Subject|Issuer|Signing Tool|Encipher|Decipher|Biometric|End Entity|CA \b|TACACS|MAC\b|Time Stamping|Any Extended|Any Purpose"
    r"|libcurl|CURL|HTTP|TLS|FTP|SMTP|TFTP|socket|hostname|Authorization|Content-Type|Content-Length|Transfer-Encoding|alt-svc|RCODE|DNS|Scheme|URL\b|chunked|Content-Encoding"
    r"|Usd|Sdf|Tf|Hd\b|Hgi|Storm|OpenSubdiv|Osd|Pcp|Ndr|prim|VtValue|RefPtr|scene delegate|draw item|DrawItem|render index|Rprim|ExtComputation|Boundingbox|BoundingBox"
    r"|\bGLSL\b|sampler|uniform\b|inlining|\bmipmap\b|\btexel\b|\btexture object\b|\bbindless\b|\bdeferred\b|\bdrawgeometry\b|\bvertex\b|\buv\b"
    r"|\bboost\b|\bopenvdb\b|\bmqtt\b|\bentitlement\b|\broam\b|\btoken\b|\bproxy auth\b|\bhostid\b|\bactivation\b|\blicense\b|\bserver\b"
    r"|\bnot found\b|\bis not\b|\bdoes not\b|\binvalid\b|\bfailed\b|\berror\b|\bwarning\b|\bexception\b|\bassert\b|\bdebug\b|\breport\b|\bdiagnos\b"
    r"|\bunable\b|\bcannot\b|\bcould not\b|\bcouldn\b|\bnull\b|\bzero\b|\bout of range\b|\btoo long\b|\btoo many\b|\btoo large\b|\btoo small\b"
    r"|\bempty\b|\bmismatch\b|\bunknown\b|\bunsupported\b|\bnot allowed\b|\balready\b|\bmust be\b|\bexceeded\b|\bexceeds\b|\bdifferent\b"
    r"|\bexpected\b|\bunexpected\b|\bunhandled\b|\brequested\b|\battempted\b|\bencountered\b|\bdetected\b|\btrying\b|\bforbidden\b|\bdenied\b"
    r"|\bnot set\b|\bnot bound\b|\bnot a\b|\bnot supported\b|\bnot available\b|\bnot the\b|\bno \b|\bhas no\b|\bno such\b|\bdoesn\b"
    r"|\bdeprecated\b|\bremoved in a future\b|\bnot yet\b|\bneeds to\b|\bshould\b|\bshouldn\b|\bmay not\b|\bcan only\b|\bcan't\b|\bcannot be\b"
    r"|\bcompil\b|\bprogram\b|\bthread\b|\bpacket\b|\bstream\b|\bchunk\b|\btransmit\b|\breceive\b|\bhandshake\b|\bphase\b|\bterminal\b"
    r"|\bvalue count\b|\bdata block\b|\bdirtylist\b|\bsesssion\b|\bsession\b|\btimeout\b|\bexpired\b|\bexpires\b|\bconstructing\b|\bemitting\b"
    r"|\bcleaning up\b|\bstarting\b|\bending\b|\bclosing\b|\bopening\b|\bwriting into\b|\bsetting\b|\bskipping\b|\bchecking\b|\blogged\b|\bcancell\b"
    r")",
    re.I,
)

# 明显不像离散界面标签的开头（日志/状态/代码走向）——排除后再看
NOISY_START = re.compile(
    r"^("
    r"Internal |Attempt|Attempting|Found |Did not|couldn|Could |Can not|Can't |Cannot |Unable "
    r"|After |Before |Emitting|Got |Skipping|Detected|Trying|Report|Reading |Writing |Generating "
    r"|Converting |Cleaning |Stopping |Starting |Closing |Returning |Enabling |Disabling |Setting |Setting up "
    r"|Specifying|Controls |Enables |Disables |Determin|Computing |Recomput|Realloc|Resetting |Flushing |Garbage "
    r"|The |This |That |These |Those |You |We |Your |Our |Sorry |Please |When |Step size |Using |Used |Doing "
    r"|Press |Click |Clicking |To work |To override |Valid |Invalid |Wrong |Bad |Illegal |Out of |Exceed |Imbalanced "
    r"|Implement|Undefined |Expected |Unexpected |Unhandled |Unrecognized |Unrecognised |Failed |Failure |Error "
    r"|Value |Count |Skipped |Refreshing |Updated |Updated |Committing |Packing |Excluding |Including |Generated "
    r"|Creating |Created |Done |Complete |Completed |Setup |Preparation |Reading |Deserializ|Serializ |Load |Loaded "
    r"|Resize |Resized |Rescaling |Scale |Scaling |Flipping |Applying |Applies |Applied |Considering |Ignoring "
    r"|Calling |Called |Force |Forced |Froze |Freeze |Follow |Following |Exit |Begin |Finished |Finish "
    r"|Preparing |Prepared |Overriding |Selected |Desel"  # 少部分会误伤，留给人工判断
    r")",
    re.I,
)

# 技术/加密/人员名等应排除的散点
EXTRA = re.compile(
    r"("
    r"^[A-Z]{3,}$|PRIVATE KEY|PUBLIC KEY|PARAMETERS|routines|\blib\b|curve over|Compromise|Signing Tool|Time Stamping"
    r"|AOV Visualiz|API |CONNECT|BYTE MACRO|BIT STRING|OCTET STRING|Autonomous|BGPsec|BIO to Core|Cessation"
    r"|Adrian|Antoni|Akira|Borna|Bradford|Carlos|Charli|Charlie|Chloe|Chris|Daniel|Duncan|Eija|Emeline|Erica"
    r"|Gabriel|Johnny|Stuart|Ollie|Peppe|Phil |Piotr|Rachel|Rajiv|Ravishankar|Robert|Rory|Sibi|Tim |Timothy|Vanessa"
    r"|William|Yann|Nayer|Carl Rand|F6LHJt|\bUi routines\b"
    r")",
    re.I,
)


cands = []
for s in rest:
    if len(s) < 3 or len(s) > 58:
        continue
    if TECH.search(s):
        continue
    if not s[0].isupper():
        continue
    if not re.match(r"^[A-Za-z][A-Za-z0-9 &%_\-.:'\u2019,/\u3001]*$", s):
        continue
    if NOISY_START.match(s):
        continue
    if s.endswith("."):
        continue
    if EXTRA.search(s):
        continue
    if len(s.split()) > 5:
        continue
    cands.append(s)

print("likely UI candidates (broad minus strict):", len(cands))
with open(ROOT / "extra_ui_candidates.txt", "w", encoding="utf-8") as fh:
    for c in cands:
        fh.write(c + "\n")
print("written to extra_ui_candidates.txt")
print("--- sample (first 150) ---")
for c in cands[:150]:
    print(repr(c))
