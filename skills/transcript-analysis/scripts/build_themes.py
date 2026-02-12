#!/usr/bin/env python3
"""
Template theming script. Reads quotes_*.json files, assigns to themes
via a compact mapping dict, outputs themes.json.

Customize THEMES and T (assignments) for each project.

Usage: python3 build_themes.py [directory_with_quotes_json_files]
"""
import json, os, sys
from collections import defaultdict

BASE = sys.argv[1] if len(sys.argv) > 1 else "."

# === CUSTOMIZE: Theme definitions (order = display order) ===
THEMES = [
    # (id, name, description, hex_color)
    ("example_theme", "Example Theme",
     "Description of what this theme captures.",
     "#da7756"),
]

# === CUSTOMIZE: Positive assignment mapping ===
# theme_id -> [(participant, line), ...]
# Everything NOT listed = dropped
T = {
    "example_theme": [
        # ("D1", 384),
    ],
}

def main():
    # Load all quotes
    all_quotes = []
    for f in sorted(os.listdir(BASE)):
        if f.startswith("quotes_") and f.endswith(".json"):
            with open(os.path.join(BASE, f)) as fh:
                all_quotes.extend(json.load(fh))
    print(f"Loaded {len(all_quotes)} quotes")

    # Build reverse map
    assigned = {}
    for theme_id, keys in T.items():
        for key in keys:
            assigned[key] = theme_id

    # Classify
    themes_out = {}
    for tid, name, desc, color in THEMES:
        themes_out[tid] = {
            "id": tid, "name": name, "description": desc, "color": color,
            "participants": [], "quotes": [], "quote_count": 0, "participant_count": 0
        }

    dropped = []
    kept = 0
    for q in all_quotes:
        key = (q["participant"], q["line"])
        tid = assigned.get(key)
        if tid:
            themes_out[tid]["quotes"].append({
                "participant": q["participant"], "line": q["line"],
                "speaker": q["speaker"], "quote": q["quote"],
                "note": q.get("relevance_note", ""),
            })
            kept += 1
        else:
            note = q.get("relevance_note", "").lower()
            if any(kw in note for kw in ["researcher", "asking"]):
                reason = "Researcher question/prompt"
            elif len(q["quote"]) < 35:
                reason = "Fragment or too brief"
            elif any(kw in note for kw in ["generic", "observation", "confirm"]):
                reason = "Generic/vague"
            else:
                reason = "Low analytical value"
            dropped.append({
                "participant": q["participant"], "line": q["line"],
                "quote": q["quote"][:120], "reason": reason,
            })

    # Compute stats
    for tid in themes_out:
        pts = sorted(set(q["participant"] for q in themes_out[tid]["quotes"]),
                     key=lambda p: (0 if p.startswith("D") else 1, p))
        themes_out[tid]["participants"] = pts
        themes_out[tid]["quote_count"] = len(themes_out[tid]["quotes"])
        themes_out[tid]["participant_count"] = len(pts)
        themes_out[tid]["quotes"].sort(
            key=lambda q: (0 if q["participant"].startswith("D") else 1,
                           q["participant"], q["line"]))

    output = {
        "metadata": {
            "total_quotes": len(all_quotes), "kept": kept,
            "dropped": len(dropped), "themes": len(THEMES),
            "unique_participants": len(set(
                q["participant"] for q in all_quotes
                if assigned.get((q["participant"], q["line"])))),
        },
        "theme_order": [t[0] for t in THEMES],
        "themes": {tid: themes_out[tid] for tid in [t[0] for t in THEMES]},
        "dropped": dropped,
    }

    out_path = os.path.join(BASE, "themes.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nWrote {out_path}")
    print(f"  Kept: {kept}, Dropped: {len(dropped)}")
    for tid, name, _, _ in THEMES:
        t = themes_out[tid]
        print(f"  {name}: {t['quote_count']}q, {t['participant_count']}p")

if __name__ == "__main__":
    main()
