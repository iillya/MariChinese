# Mari 7.1v1 UI text static scan

- Target: `C:\Program Files\Mari7.1v1\Bundle\bin`
- Scanned binaries: 73
- Unique strict UI candidates: 2115
- Unique broad UI candidates: 12736
- Unique ASCII strings (raw): 293766
- Unique UTF-16LE strings (raw): 1103

## Contents

| Path | Description |
|---|---|
| `raw/` | All ASCII/UTF-16 strings per binary, unfiltered |
| `candidates/` | Filtered UI text candidates per binary |
| `all_ui_candidates.txt` | Strict merged UI candidates (recommended for translation) |
| `all_ui_candidates_broad.txt` | Broad merged candidates (kept as backup for manual review) |
| `all_ascii_strings.txt` | Merged unique ASCII strings |
| `all_utf16_strings.txt` | Merged unique UTF-16LE strings |
| `scanned_files.txt` | Exact list of scanned files |
| `manifest.json` | Scan metadata and statistics |
| `scan_mari_ui_texts.py` | Raw extraction + broad filtering script |
| `filter_ui_candidates.py` | Re-filters broad candidates into strict `all_ui_candidates.txt` |
