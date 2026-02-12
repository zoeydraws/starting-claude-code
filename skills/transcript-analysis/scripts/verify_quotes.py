#!/usr/bin/env python3
"""
Template verification script for transcript quote extraction.
Checks that every extracted quote exists verbatim in its source transcript.

Usage: python3 verify_quotes.py [directory_with_quotes_json_files]
"""
import json, os, re, sys

def strip_speaker_prefixes(text):
    """Remove speaker labels that appear between merged multi-line quotes."""
    text = re.sub(r"\n+SPEAKER_\d+: ", " ", text)
    text = re.sub(r"\n+\[SPEAKER_\d+\]: ", " ", text)
    return text

def verify_quote(quote, file_cache):
    """Check if a quote exists verbatim in its source file."""
    filepath = quote["file"]
    if filepath not in file_cache:
        try:
            with open(filepath, "r") as f:
                raw = f.read()
            file_cache[filepath] = strip_speaker_prefixes(raw)
        except FileNotFoundError:
            return False, f"File not found: {filepath}"

    cleaned = file_cache[filepath]
    if quote["quote"] in cleaned:
        return True, None
    return False, "Quote text not found in source file"

def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "."
    file_cache = {}
    total = 0
    passed = 0
    failed = 0
    failures = []

    for fname in sorted(os.listdir(base)):
        if not (fname.startswith("quotes_") and fname.endswith(".json")):
            continue
        filepath = os.path.join(base, fname)
        with open(filepath) as f:
            quotes = json.load(f)
        for i, q in enumerate(quotes):
            total += 1
            ok, err = verify_quote(q, file_cache)
            if ok:
                passed += 1
            else:
                failed += 1
                failures.append((fname, i, q["participant"], q["line"], err))

    print(f"\nResults: {passed}/{total} pass ({100*passed/total:.1f}%)")
    if failures:
        print(f"\n{failed} failures:")
        for fname, idx, pid, line, err in failures:
            print(f"  {fname}[{idx}] {pid} L{line}: {err}")
    else:
        print("All quotes verified!")

if __name__ == "__main__":
    main()
