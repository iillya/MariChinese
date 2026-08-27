#!/usr/bin/env python3
"""Extract likely UI text candidates from Mari 7.1v1 related binaries.

Output is written only inside the directory containing this script.
Raw strings stay in raw/; filtered user-visible text goes to candidates/
and all_ui_candidates.txt.
"""
import json
import re
import sys
from pathlib import Path

TARGET_ROOT = Path(r"C:\Program Files\Mari7.1v1\Bundle\bin")
OUTPUT_ROOT = Path(__file__).resolve().parent
RELATED_NAME_RE = re.compile(r"^(Mari|Mri|Gnz|fn|foundry|Foundry)", re.IGNORECASE)
BINARY_EXTS = {".exe", ".dll", ".pyd", ".so", ".bin"}
ASCII_RE = re.compile(rb"[\x20-\x7e]{3,}")
UTF16_RE = re.compile(rb"(?:[\x20-\x7e]\x00){3,}")

# Common UI single words.  Single-word labels are kept if they appear here or
# appear as a word inside an accepted phrase.
BASE_UI_WORDS = {
    "Add", "Apply", "Cancel", "Close", "Delete", "Edit", "Export", "File",
    "Help", "Import", "New", "OK", "Open", "Remove", "Save", "Tools", "View",
    "Yes", "No", "Layer", "Layers", "Project", "Projects", "Image", "Images",
    "Shader", "Shaders", "Color", "Colors", "Paint", "Node", "Nodes",
    "Geometry", "Geometries", "Object", "Objects", "Camera", "Cameras",
    "Render", "Renders", "Material", "Materials", "Texture", "Textures",
    "Mask", "Masks", "Channel", "Channels", "Shelf", "Selection", "Group",
    "Groups", "Stack", "Stacks", "Filter", "Filters", "Window", "Windows",
    "Action", "Actions", "Attribute", "Attributes", "Input", "Output", "Model",
    "Viewport", "Bake", "Projector", "Mesh", "Patch", "Patches", "Frame",
    "Timeline", "History", "Properties", "Preferences", "Parameters", "Graph",
    "Graphs", "Settings", "Console", "Info", "Rename", "Duplicate", "Undo",
    "Redo", "Copy", "Paste", "Select", "Deselect", "Hide", "Show", "Lock",
    "Unlock", "LayerSet", "ImageSet", "Projection", "PaintBuffer", "BakePoint",
    "MaskGroup", "ShaderInput", "ShaderOutput", "ChannelGroup", "ObjectList",
    "All", "Any", "None", "Custom", "Default", "Normal", "Unnamed", "Name",
    "Type", "Value", "Mode", "Size", "Width", "Height", "Resolution",
    "Format", "Quality", "Opacity", "Intensity", "Radius", "Angle", "Strength",
    "Scale", "Offset", "Rotation", "Position", "Path", "Folder", "Directory",
    "Filename", "State", "Status", "Enabled", "Disabled", "Visible", "Hidden",
    "Active", "Inactive", "Selected", "Locked", "Unlocked", "Root", "Child",
    "Parent", "Original", "Current", "Previous", "Next", "First", "Last",
    "Top", "Bottom", "Left", "Right", "Center", "Up", "Down", "Forward",
    "Back", "True", "False", "On", "Off", "Auto", "Manual", "Max", "Min",
    "Average", "Total", "Start", "End", "Update", "Reload", "Refresh",
    "Reset", "Restore", "Install", "Register", "Confirm", "Warning", "Error",
    "Notice", "Tip", "Hint", "Unknown", "Missing", "Failed", "Success",
    "Done", "Complete", "Progress", "Running", "Pending", "Waiting",
    "Canceled", "Cancelled", "Accept", "Reject", "Allow", "Block", "Skip",
    "Ignore", "Retry", "Abort", "Test", "Debug", "Build", "Load", "Unload",
    "Connect", "Disconnect", "Enable", "Disable", "Expand", "Collapse",
    "Minimize", "Maximize", "Arrange", "Align", "Distribute", "Flip",
    "Mirror", "Instances", "Instance", "Alias", "Swatch", "Backdrop",
    "Pass", "Lens", "Level", "Order", "List", "Panel", "Dialog", "Page",
    "Section", "Option", "Options", "Advanced", "Basic", "Standard",
    "Raw", "Verified", "License", "Caches", "Cache", "Snap",
    "Magnetic", "Preference", "Preferences", "Shortcut", "Shortcuts",
    "Recent", "Recents", "Most", "Used", "Last", "Folders", "Save As",
    "SaveAll", "OpenRecent", "CloseAll", "AddToShelf", "AddToLibrary",
    "RemoveFromShelf", "RemoveFromLibrary",
}


def looks_like_code_symbol(s):
    if not s:
        return True
    if s.startswith("?") or "@@" in s:
        return True
    if re.fullmatch(r"[_a-zA-Z][_a-zA-Z0-9]*@@[_a-zA-Z0-9@?$]+", s):
        return True
    if s.startswith("void __") or s.startswith("public:") or s.startswith("private:"):
        return True
    if re.search(r"__cdecl|__thiscall|__stdcall|__fastcall", s):
        return True
    if re.fullmatch(r"[.&*A-Za-z0-9_]+\(.*\)", s) and " " not in s:
        return True
    return False


def is_path_or_url(s):
    if re.match(r"^[A-Za-z]:[\/]", s):
        return True
    if s.startswith("http://") or s.startswith("https://"):
        return True
    if "\\" in s:
        return True
    return False


def is_phrase_candidate(s):
    """Strings with spaces and multiple usable words, likely UI/error text.

    This intentionally removes source code, shader snippets, C++ diagnostics,
    file paths and printf-style debug logs while keeping Qt-style UI strings.
    """
    if len(s) < 3 or len(s) > 200:
        return False
    if not re.search(r"\s", s):
        return False
    if not re.search(r"[A-Za-z]{2,}", s):
        return False
    if looks_like_code_symbol(s):
        return False
    if is_path_or_url(s):
        return False
    if s.startswith("#") or s.startswith("//") or s.startswith("/*"):
        return False
    # Obvious non-UI remnants.
    if s.startswith("!//") or s.startswith("!!") or s.startswith("%%"):
        return False
    if "Copyright" in s or "stb_image_write" in s or "curl.se" in s:
        return False
    # C++ / shader / code markers.
    if "std::" in s or "::" in s or "->" in s:
        return False
    if re.search(r"[=<>{}\[\]@$*;]", s):
        return False
    if re.search(r"&&|\|\||==|!=|<=|>=", s):
        return False
    # printf style placeholders are usually debug messages; keep Qt %1/%2 style.
    if re.search(r"%[-+0-9.]*[sdxXfcliup]", s):
        return False
    tokens = re.findall(r"[A-Za-z]{2,}", s)
    if len(tokens) < 2:
        return False
    letters = sum(c.isalpha() for c in s)
    if letters < 8 or letters / len(s) < 0.60:
        return False
    if len(tokens) > 20 and len(s) > 120:
        return False
    return True


def is_single_word_candidate(s, word_set):
    # Keep only curated common UI words for standalone labels.  This avoids
    # C++ identifiers, random binary tokens and other non-UI single words.
    _ = word_set
    if len(s) < 2 or len(s) > 30:
        return False
    if not s.isalpha():
        return False
    if looks_like_code_symbol(s):
        return False
    return s in BASE_UI_WORDS


def is_ui_candidate(s, word_set):
    if is_phrase_candidate(s):
        return True
    if is_single_word_candidate(s, word_set):
        return True
    return False


def extract_ascii(data):
    out = []
    for m in ASCII_RE.finditer(data):
        s = m.group().decode("latin-1", errors="replace").strip()
        if len(s) >= 3:
            out.append(("ASCII", s))
    return out


def extract_utf16(data):
    out = []
    for m in UTF16_RE.finditer(data):
        raw = m.group()
        try:
            s = raw.decode("utf-16le", errors="replace").strip()
        except Exception:
            continue
        if len(s) >= 3 and all(ord(c) < 0x7F for c in s):
            out.append(("UTF16", s))
    return out


def sanitize_rel(rel):
    return "__".join(re.sub(r"[^A-Za-z0-9._-]", "_", p) for p in rel.parts)


def unique_strings(ascii_strings, utf16_strings):
    seen = set()
    out = []
    for kind, s in ascii_strings + utf16_strings:
        key = (kind, s)
        if key in seen:
            continue
        seen.add(key)
        out.append((kind, s))
    return out


def main():
    if not TARGET_ROOT.exists():
        print("Error: directory does not exist: %s" % TARGET_ROOT, file=sys.stderr)
        return 1

    raw_dir = OUTPUT_ROOT / "raw"
    cand_dir = OUTPUT_ROOT / "candidates"
    raw_dir.mkdir(parents=True, exist_ok=True)
    cand_dir.mkdir(parents=True, exist_ok=True)

    related = []
    for p in sorted(TARGET_ROOT.rglob("*")):
        if not p.is_file():
            continue
        if p.suffix.lower() not in BINARY_EXTS:
            continue
        if not RELATED_NAME_RE.match(p.name):
            continue
        related.append(p)

    # Pass 1: write raw dumps and build a global set of words that appear in
    # phrase-like UI strings.  This allows single-word labels to be recognized.
    phrase_words = set()
    all_phrase_candidates = set()
    stats = []
    for i, p in enumerate(related, 1):
        rel = p.relative_to(TARGET_ROOT)
        safe = sanitize_rel(rel)
        try:
            data = p.read_bytes()
        except OSError as e:
            print("Skip %s: %s" % (p, e), file=sys.stderr)
            continue

        ascii_strings = extract_ascii(data)
        utf16_strings = extract_utf16(data)
        raw_strings = unique_strings(ascii_strings, utf16_strings)

        raw_path = raw_dir / (safe + ".raw.txt")
        with raw_path.open("w", encoding="utf-8", newline="\n") as f:
            f.write("# source: %s\n" % rel)
            f.write("# bytes: %d\n" % len(data))
            f.write("# strings: %d\n\n" % len(raw_strings))
            for kind, s in raw_strings:
                f.write("[%c] %s\n" % ("A" if kind == "ASCII" else "U", s))

        for kind, s in raw_strings:
            if is_phrase_candidate(s):
                all_phrase_candidates.add(s)
                for w in re.findall(r"[A-Za-z]{2,}", s):
                    phrase_words.add(w)

        stats.append({
            "path": str(rel),
            "size_bytes": len(data),
            "raw_total": len(raw_strings),
        })
        print("[pass1 %d/%d] %s raw=%d" % (i, len(related), rel, len(raw_strings)))

    # Pass 2: write filtered per-file UI candidate files and merged lists.
    all_candidates = set()
    all_ascii = set()
    all_utf16 = set()
    stats2 = []

    for i, p in enumerate(related, 1):
        rel = p.relative_to(TARGET_ROOT)
        safe = sanitize_rel(rel)
        try:
            data = p.read_bytes()
        except OSError as e:
            print("Skip %s: %s" % (p, e), file=sys.stderr)
            continue

        ascii_strings = extract_ascii(data)
        utf16_strings = extract_utf16(data)
        raw_strings = unique_strings(ascii_strings, utf16_strings)

        ui_lines = []
        ui_seen = set()
        for kind, s in raw_strings:
            if s in ui_seen:
                continue
            if is_ui_candidate(s, phrase_words):
                ui_seen.add(s)
                ui_lines.append(s)

        cand_path = cand_dir / (safe + ".ui.txt")
        with cand_path.open("w", encoding="utf-8", newline="\n") as f:
            f.write("# source: %s\n" % rel)
            f.write("# candidates: %d\n\n" % len(ui_lines))
            for s in ui_lines:
                f.write(s + "\n")

        all_candidates.update(ui_lines)
        for _, s in ascii_strings:
            all_ascii.add(s)
        for _, s in utf16_strings:
            all_utf16.add(s)

        stats2.append({
            "path": str(rel),
            "size_bytes": len(data),
            "ui_candidates": len(ui_lines),
        })
        print("[pass2 %d/%d] %s ui=%d" % (i, len(related), rel, len(ui_lines)))

    with (OUTPUT_ROOT / "all_ui_candidates.txt").open("w", encoding="utf-8", newline="\n") as f:
        f.write("# Unique filtered UI candidates from Mari 7.1v1 related binaries\n")
        for s in sorted(all_candidates):
            f.write(s + "\n")

    with (OUTPUT_ROOT / "all_ascii_strings.txt").open("w", encoding="utf-8", newline="\n") as f:
        f.write("# All unique ASCII strings\n")
        for s in sorted(all_ascii):
            f.write(s + "\n")

    with (OUTPUT_ROOT / "all_utf16_strings.txt").open("w", encoding="utf-8", newline="\n") as f:
        f.write("# All unique UTF-16LE strings\n")
        for s in sorted(all_utf16):
            f.write(s + "\n")

    with (OUTPUT_ROOT / "scanned_files.txt").open("w", encoding="utf-8", newline="\n") as f:
        f.write("# Scanned Mari/Foundry binaries: %d\n" % len(related))
        for p in related:
            f.write(str(p.relative_to(TARGET_ROOT)) + "\n")

    manifest = {
        "target_root": str(TARGET_ROOT),
        "output_root": str(OUTPUT_ROOT),
        "scanned_file_count": len(related),
        "all_ui_candidate_count": len(all_candidates),
        "all_phrase_candidate_count": len(all_phrase_candidates),
        "all_ascii_unique_count": len(all_ascii),
        "all_utf16_unique_count": len(all_utf16),
        "files": stats2,
    }
    with (OUTPUT_ROOT / "manifest.json").open("w", encoding="utf-8", newline="\n") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    with (OUTPUT_ROOT / "README.md").open("w", encoding="utf-8", newline="\n") as f:
        f.write("# Mari 7.1v1 UI text static scan\n\n")
        f.write("- Target: `%s`\n" % TARGET_ROOT)
        f.write("- Scanned binaries: %d\n" % len(related))
        f.write("- Unique filtered UI candidates: %d\n" % len(all_candidates))
        f.write("- Unique ASCII strings (raw): %d\n" % len(all_ascii))
        f.write("- Unique UTF-16LE strings (raw): %d\n" % len(all_utf16))
        f.write("\n## Contents\n\n")
        f.write("| Path | Description |\n|---|---|\n")
        f.write("| `raw/` | All ASCII/UTF-16 strings per binary, unfiltered |\n")
        f.write("| `candidates/` | Filtered UI text candidates per binary |\n")
        f.write("| `all_ui_candidates.txt` | Merged unique UI candidates |\n")
        f.write("| `all_ascii_strings.txt` | Merged unique ASCII strings |\n")
        f.write("| `all_utf16_strings.txt` | Merged unique UTF-16LE strings |\n")
        f.write("| `scanned_files.txt` | Exact list of scanned files |\n")
        f.write("| `manifest.json` | Scan metadata and statistics |\n")
        f.write("| `scan_mari_ui_texts.py` | This scanning script |\n")

    print("\nDone. Output directory: %s" % OUTPUT_ROOT)
    print("Scanned files: %d" % len(related))
    print("Unique filtered UI candidates: %d" % len(all_candidates))
    return 0


if __name__ == "__main__":
    sys.exit(main())

