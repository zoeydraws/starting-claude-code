# Pipeline Details

## Quote JSON Schema

```json
{
  "participant": "D1",
  "file": "/absolute/path/to/transcript.md",
  "line": 384,
  "speaker": "SPEAKER_02",
  "quote": "Exact verbatim text from transcript",
  "relevance_note": "1 sentence explaining relevance to the extraction topic"
}
```

## Verification Script Template

The verification script must handle two speaker prefix formats found in transcripts:
- Standard: `SPEAKER_00: text here`
- Bracketed: `[SPEAKER_00]: text here`

When subagents extract multi-line quotes, they concatenate text from consecutive lines by the same speaker. The speaker prefix between lines gets included in the raw transcript but should be stripped for verification.

### Common Failure Types

| Failure | Cause | Fix |
|---------|-------|-----|
| File path wrong | Subagent typo in directory name | Correct the path in the JSON |
| Word mismatch | Subagent misread a word (e.g., "self" vs "cell") | Compare with `repr()`, fix the quote |
| Missing prefix word | Subagent dropped "Okay, " or "Yeah, " from start | Add the missing word, fix line number |
| Merged speakers | Subagent combined text from 2 different speakers | Trim to single speaker's text |
| Bracket format | Transcript uses `[SPEAKER_XX]:` not `SPEAKER_XX:` | Update regex in verification script |

### Character-by-character debugging

When a quote fails verification:
```python
# Find where the mismatch starts
for i, (a, b) in enumerate(zip(quote_text, file_text[match_start:])):
    if a != b:
        print(f"Mismatch at position {i}: quote={repr(a)}, file={repr(b)}")
        print(f"Context: ...{repr(quote_text[max(0,i-20):i+20])}...")
        break
```

## Theming Approach

### Assignment Format

Use a compact positive-assignment dict in the build script:

```python
T = {
    "theme_id": [
        ("participant", line_number),
        ("participant", line_number),
    ],
}
```

Everything NOT listed in any theme = dropped. This is much more compact than mapping every single quote.

### Drop Reason Auto-Classification

```python
def classify_drop(quote):
    note = quote.get("relevance_note", "").lower()
    if any(kw in note for kw in ["researcher", "asking"]):
        return "Researcher question/prompt"
    if len(quote["quote"]) < 35:
        return "Fragment or too brief"
    if any(kw in note for kw in ["generic", "observation", "confirm"]):
        return "Generic/vague"
    return "Low analytical value"
```

### Theme Definition Structure

Each theme needs: id, name, description (1-2 sentences), display color (hex).

Sort themes by participant count descending for display.

## HTML Viewer Architecture

- `themes.json` = data source (produced by build script)
- `themes_viewer.html` = standalone HTML that fetches themes.json
- Needs a local server to load (fetch won't work from file://)
- Use existing server if one is running, or `python3 -m http.server 8787`

### Design Tokens (Claude Light Theme)

```css
--bg: #faf9f7;
--card: #fff;
--border: #e8e4df;
--text: #2d2d2d;
--text-secondary: #6b6560;
--accent: #da7756;
```

## Critic Personas

When sending 2 critics in parallel, use complementary personas:

1. **Senior UX Researcher**: Skeptical about theme boundaries, checks if quotes actually support their assigned theme, looks for misplaced quotes, missing themes, and over-broad categories.

2. **Product Manager**: Checks actionability, participant over-representation, discovery vs UT divergence, researcher contamination, and gaps needed for shipping decisions (severity ranking, shipped vs requested, dependency mapping).
