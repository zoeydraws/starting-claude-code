---
description: >
  This skill should be used when the user asks to "extract quotes from transcripts",
  "mine interviews for a topic", "theme interview quotes", "analyze transcripts for X",
  or has a set of interview/UT transcripts they want to analyze for a specific feature
  or topic. Runs a 4-phase pipeline: inventory, extract, verify, theme + visualize.
argument-hint: "[topic-description]"
---

# Transcript Analysis

Extract verbatim quotes from interview transcripts on a given topic, programmatically verify them, cluster into themes, and generate an HTML viewer.

**When to use:** You have interview transcripts (discovery, UT, or mixed) and want to extract all quotes about a specific topic for bottom-up thematic analysis.

## Critical Rules

| Rule | Why |
|------|-----|
| **Scripts do the work, not LLM thinking** | Never spend turns reasoning through 200+ quotes. Write a Python script with a compact mapping dict and let it classify/generate. |
| **Test 2, then fire all** | Extract from 2 transcripts first. Verify format. Fix issues. Then fire all remaining in parallel. |
| **Verify 100% programmatically** | Every quote must be checked against its source file via full-text search. Never trust LLM extraction without verification. |
| **Work on the next step while subagents run** | Build verification scripts while extraction runs. Build theming scripts while verification runs. Zero idle time. |
| **Break large outputs into script + run** | Never generate large HTML/JSON in a single LLM turn. Write a Python script, run it. |

## Workflow

### Phase 1: Inventory

Send a **haiku** subagent to list all transcript files, count them, and estimate total tokens.

```
Output: "Found N transcripts in M directories (~X tokens total)"
```

Report to user before proceeding. Ask for the extraction topic if not already provided.

### Phase 2: Extract

**Test run (2 transcripts):**

Fire 2 **sonnet** subagents (1 per transcript) with this prompt template:

```
Read the transcript at [FILE_PATH].

Extract every quote where someone directly talks about [TOPIC].
Include both participant statements AND researcher questions about [TOPIC].

Output a JSON array. Each object must have:
- "participant": "[ID]"
- "file": "[full file path]"
- "line": [line number where quote starts]
- "speaker": "[SPEAKER_XX from transcript]"
- "quote": "[exact verbatim text - do not paraphrase]"
- "relevance_note": "[1 sentence: why this quote is relevant to TOPIC]"

Rules:
- Quotes must be VERBATIM - exact words from transcript
- Multi-line quotes: include full text, the speaker prefix between lines will be stripped during verification
- Include the line number of the FIRST line of the quote
- If no relevant quotes exist, return an empty array []
```

Verify the 2 test outputs with the verification script (Phase 3). Fix any format issues.

**Full run:**

Fire all remaining subagents in parallel (sonnet, 1 per transcript). Save each output as `quotes_[id].json`.

### Phase 3: Verify

Write/use `verify_quotes.py` that:

1. Loads each `quotes_*.json`
2. For each quote, reads the source transcript file
3. Strips speaker prefixes from transcript text: both `SPEAKER_XX: ` and `[SPEAKER_XX]: ` formats
4. Checks that the quote text exists verbatim in the cleaned transcript
5. Reports pass/fail for each quote

```python
# Key verification logic:
def strip_speaker_prefixes(text):
    text = re.sub(r"\n+SPEAKER_\d+: ", " ", text)
    text = re.sub(r"\n+\[SPEAKER_\d+\]: ", " ", text)
    return text

# Check: quote_text in strip_speaker_prefixes(full_file_text)
```

**Target: 100% pass.** Fix failures individually:
- File path typos: correct the path
- Misread words: compare character-by-character with source using `repr()`
- Wrong line numbers: find correct line
- Merged quotes from different speakers: trim to single speaker's text

### Phase 4: Theme + Visualize

1. **Write a Python build script** (`build_themes.py`) with:
   - Theme definitions (id, name, description, color)
   - A compact assignment mapping: `theme_id -> [(participant, line), ...]`
   - Everything NOT assigned = dropped
   - Auto-classify drop reasons from relevance_note keywords

2. **Run the script** to produce `themes.json`

3. **Write an HTML viewer** (`themes_viewer.html`) that:
   - Loads `themes.json` (via fetch from same directory)
   - Floating sidebar nav with theme names + participant counts
   - Scrollable main content with theme sections
   - Quotes grouped by participant within each theme
   - Collapsible dropped section at bottom

**Gate check after each phase:**
- Phase 2: "N quotes extracted from M transcripts. K had 0 relevant quotes."
- Phase 3: "N/N pass (100%). K failures fixed."
- Phase 4: "N quotes kept in K themes, M dropped. HTML at [path]."

## Anti-Patterns

| Don't | Do instead |
|-------|------------|
| Generate large HTML in one LLM turn | Write Python build script, run it |
| Reason through 200+ quote assignments in your head | Write compact mapping dict in Python |
| Use coder/architect subagents for simple file I/O | Use explorer or do it yourself |
| Verify quotes at exact line numbers | Verify via full-text search (lines shift) |
| Fire all subagents without testing first | Test 2 first, verify, then fire all |
| Wait idle while subagents run | Build next phase's scripts in parallel |
| Use AskUserQuestion for rapid-fire scoping | Ask inline in regular messages |

## Model Selection

| Task | Model |
|------|-------|
| Inventory (file listing) | haiku |
| Quote extraction | sonnet |
| Verification script | Write it yourself |
| Thematic analysis + assignment | Write it yourself (Python script) |
| Critics / peer review | sonnet (2 in parallel, different personas) |
