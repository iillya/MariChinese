#!/usr/bin/env python3
"""Re-filter all_ui_candidates_broad.txt into a stricter all_ui_candidates.txt.

Keeps the broad list as all_ui_candidates_broad.txt and writes the stricter,
more clearly UI-oriented list to all_ui_candidates.txt.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BROAD = ROOT / "all_ui_candidates_broad.txt"
STRICT = ROOT / "all_ui_candidates.txt"
MANIFEST = ROOT / "manifest.json"

UI_KEYWORDS = {
    "Add", "Apply", "Remove", "Delete", "Edit", "Save", "Open", "Close",
    "Export", "Import", "Rename", "Duplicate", "Copy", "Paste", "Select",
    "Deselect", "Hide", "Show", "Lock", "Unlock", "Cancel", "OK", "Yes", "No",
    "Layer", "Layers", "Channel", "Channels", "Mask", "Masks", "Paint", "Bake",
    "Projector", "Projection", "Shader", "Shaders", "Node", "Nodes",
    "Geometry", "Geometries", "Object", "Objects", "Image", "Images", "Color",
    "Colors", "View", "Viewport", "Help", "Tools", "Window", "Windows",
    "Project", "Projects", "Stack", "Stacks", "Group", "Groups", "Filter",
    "Filters", "Shelf", "Shelves", "Material", "Materials", "Texture",
    "Textures", "Camera", "Cameras", "Render", "Renders", "Frame", "Timeline",
    "Settings", "Preferences", "Options", "Properties", "Selection",
    "Attribute", "Attributes", "Input", "Output", "Mesh", "Patch", "Patches",
    "Graph", "Graphs", "Panel", "Dialog", "Page", "Section", "List", "State",
    "Mode", "Size", "Width", "Height", "Resolution", "Format", "Quality",
    "Opacity", "Intensity", "Radius", "Angle", "Strength", "Scale", "Offset",
    "Rotation", "Position", "Path", "Folder", "Directory", "Filename", "Name",
    "Type", "Value", "Status", "Enabled", "Disabled", "Visible", "Hidden",
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
    "Mirror", "Instances", "Instance", "Alias", "Swatch", "Backdrop", "Pass",
    "Lens", "Level", "Order", "Advanced", "Basic", "Standard", "Raw",
    "Verified", "License", "Caches", "Cache", "Snap", "Preference",
    "Shortcut", "Recent", "Most", "Used", "Normal", "Unnamed",
}

BAD_SUB = [
    "QString", "QObject", "QAction", "QWidget", "QList", "QColor", "QModel",
    "Internal ", "Invalid ", "NULL", "Null ", "pointer", "not valid",
    "not a valid", "does not contain", "does not have", "could not", "cannot",
    "Unable", "Failed", "Error", "Warning", "Deprecated", "deprecated",
    "removed in a future", "This function", "This calls",
    "Method not supported", "DDI Profile", "No error", "No project",
    "Not available", "startingProcessing", "progressStarted",
    "currentIndexChanged", "currentPathChanged", "is null", "is NULL",
    "std::", "->", "::", "MriCustom", "QIcon", "QPoint", "QItemSelection",
    "QDateTime", "QVariant", "MriFileList", "MriSn", "MriLayer", "MriColor",
    "MriImage", "MriDeserialize", "MriNode", "MriCore", "MriGeo",
    "MriComboBox", "MriCanvas", "MriShader", "libcurl", "curl.se",
    "Copyright", "Linotype", "OpenSSL", "RSA", "AES", "TLS", "SSL",
]

BAD_RE = re.compile(r"%[-+0-9.]*[sdxXfcliupzZ]")
BS = chr(92)


def _bad_char(c):
    return c in "=<>{}[];@$*/" or c == BS


def keep(s):
    if len(s) < 3 or len(s) > 100:
        return False
    if not re.search(r"\s", s):
        return False
    tokens = re.findall(r"[A-Za-z]{2,}", s)
    if len(tokens) < 2:
        return False
    letters = sum(c.isalpha() for c in s)
    if letters / len(s) < 0.65:
        return False

    core = s
    while core.startswith("&"):
        core = core[1:]
    if core[0] in "\"'()!#01,.-+/":
        return False
    if "(" in s or ")" in s:
        return False
    if any(_bad_char(c) for c in s):
        return False
    if BAD_RE.search(s):
        return False
    for bad in BAD_SUB:
        if bad in s:
            return False

    words = set(tokens)
    return bool(words & UI_KEYWORDS)


def main():
    if not BROAD.exists():
        print("Error: %s not found" % BROAD, file=__import__("sys").stderr)
        return 1

    strings = [l for l in BROAD.read_text(encoding="utf-8").splitlines()
               if l and not l.startswith("#")]
    strict = [s for s in strings if keep(s)]

    with STRICT.open("w", encoding="utf-8", newline="\n") as f:
        f.write("# Unique strict UI candidates from Mari 7.1v1 (further filtered)\n")
        for s in sorted(strict):
            f.write(s + "\n")

    if MANIFEST.exists():
        mf = json.loads(MANIFEST.read_text(encoding="utf-8"))
        mf["all_ui_candidate_count"] = len(strict)
        mf["all_ui_candidates_broad_count"] = len(strings)
        with MANIFEST.open("w", encoding="utf-8", newline="\n") as f:
            json.dump(mf, f, ensure_ascii=False, indent=2)

    print("Broad: %d -> Strict: %d" % (len(strings), len(strict)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
