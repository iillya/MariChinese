#!/usr/bin/env python3
"""Append the Mari runtime payload to the native installer executable."""

import hashlib
import os
import struct

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "build", "out")
DIST = os.path.join(ROOT, "dist")
MAGIC = 0x314952414D4843  # "CHMARI1"


def main():
    files = [
        ("MariChineseHook.dll", os.path.join(OUT, "MariChineseHook.dll")),
        ("MariDpiVtable.dll", os.path.join(OUT, "MariDpiVtable.dll")),
        ("MariChineseLauncher.exe", os.path.join(OUT, "MariChineseLauncher.exe")),
        ("translations/dictionary_zh.json",
         os.path.join(ROOT, "translations", "dictionary_zh.json")),
    ]
    installer = os.path.join(OUT, "MariChineseInstaller.exe")
    for _, path in files:
        if not os.path.isfile(path):
            raise SystemExit(f"missing payload file: {path}")
    with open(installer, "rb") as stream:
        base = stream.read()

    payload = bytearray()
    entries = []
    offset = len(base)
    for name, path in files:
        with open(path, "rb") as stream:
            data = stream.read()
        encoded = name.encode("utf-8")
        entries.append((encoded, offset, len(data), hashlib.sha256(data).digest()))
        payload += data
        offset += len(data)

    manifest = bytearray()
    for name, file_offset, size, digest in entries:
        manifest += struct.pack("<I", len(name)) + name
        manifest += struct.pack("<QQ", file_offset, size) + digest
    tail = struct.pack("<IIQ", len(manifest), len(entries), MAGIC)

    os.makedirs(DIST, exist_ok=True)
    destination = os.path.join(DIST, "MariChineseInstaller.exe")
    temporary = destination + ".tmp"
    with open(temporary, "wb") as stream:
        stream.write(base + payload + manifest + tail)
    os.replace(temporary, destination)
    print(f"embedded {len(entries)} files -> {destination}")


if __name__ == "__main__":
    main()
