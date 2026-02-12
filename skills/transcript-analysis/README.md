# Shared Claude Code Skills

Skills for Claude Code (Anthropic's CLI tool) that automate common research workflows.

## What are skills?

Skills are reusable prompts that teach Claude Code how to perform multi-step tasks. When installed, they appear as slash commands (e.g., `/transcript-analysis`) that you can invoke during any conversation.

## Available skills

| Skill | What it does |
|-------|-------------|
| `transcript-analysis` | Extract verbatim quotes from interview transcripts on a topic, verify them programmatically, cluster into themes, and generate an HTML viewer |

## How to install

### Option A: Install for all your projects (personal/global)

Copy the skill folder into your global skills directory:

```bash
cp -r transcript-analysis ~/.claude/skills/
```

After copying, the folder structure should look like:

```
~/.claude/skills/
└── transcript-analysis/
    ├── SKILL.md                 # Main instructions Claude follows
    ├── references/
    │   └── pipeline-details.md  # Detailed technical reference
    └── scripts/
        ├── verify_quotes.py     # Template: verify extracted quotes
        └── build_themes.py      # Template: assign quotes to themes
```

### Option B: Install for one project only (shared with team via git)

Copy the skill folder into your project's `.claude/skills/` directory:

```bash
mkdir -p .claude/skills
cp -r transcript-analysis .claude/skills/
```

This option lets you commit the skill to git so your whole team has access.

## How to verify it's installed

Open Claude Code in your terminal and type `/transcript`. You should see `transcript-analysis` appear in the autocomplete suggestions.

You can also check by running `/context` in Claude Code — it will list all loaded skills and their token usage.

## How to use

In any Claude Code conversation, type:

```
/transcript-analysis chart editing features
```

Replace "chart editing features" with whatever topic you want to extract quotes about. Claude will then walk through a 4-phase pipeline:

1. **Inventory** — counts your transcripts and estimates size
2. **Extract** — sends parallel agents to pull verbatim quotes from each transcript
3. **Verify** — runs a Python script to check every quote exists in the source
4. **Theme + Visualize** — clusters quotes into themes and generates an HTML viewer

## Prerequisites

- **Claude Code** installed (`npm install -g @anthropic-ai/claude-code`)
- **Python 3** available on your machine (for verification and theming scripts)
- Interview transcripts as `.md` or `.txt` files in a directory

## Recommended CLAUDE.md rule

Add this to your `~/.claude/CLAUDE.md` (global) or project `CLAUDE.md` to improve performance on bulk data tasks:

```markdown
## Bulk Data Processing Rule

Always prefer Python scripts over LLM reasoning for bulk data operations.
When processing 50+ items (quotes, entries, records, assignments):
- Write a compact Python script with the data/mapping as a dict or list
- Run the script to produce the output
- Never spend LLM turns reasoning through items one by one
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Skill doesn't appear in autocomplete | Restart Claude Code. Check the folder is at `~/.claude/skills/transcript-analysis/SKILL.md` (exact path matters) |
| "Permission denied" when running scripts | Run `chmod +x ~/.claude/skills/transcript-analysis/scripts/*.py` |
| HTML viewer shows "Could not load themes.json" | Serve the output directory with `python3 -m http.server 8787` and open `http://localhost:8787/themes_viewer.html` |
| Verification script fails on bracket speaker format | The script handles both `SPEAKER_00:` and `[SPEAKER_00]:` formats. If your transcripts use a different format, edit the regex in `verify_quotes.py` |
