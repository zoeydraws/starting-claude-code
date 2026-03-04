# Fun Stuff

Optional extras that make Claude Code more enjoyable to use. None of these are required – just nice to have.

---

## Customize Your Status Line

The status line shows helpful info at a glance while you work.

![Status line example](images/status-line.png)

**What it shows:**
- **Branch** — Current git branch (blue)
- **Context %** — How much of Claude's memory is used (green/yellow/red based on usage)
- **Model** — Which Claude model is active (e.g., Opus 4.5)
- **Active subagent** — Which subagent is running, if any (cyan)

---

### How to Set It Up

Ask Claude:

```
Set up a custom status line that shows: git branch (blue), context window
usage % (green under 45%, yellow under 70%, red above), the active model
name, and which subagent is running (if any). Use a shell script at
~/.claude/statusline.sh and hooks to track subagent start/stop.
```

Claude will create the script, hooks, and settings for you.

---

### What It Creates

**`~/.claude/statusline.sh`** — The script that formats the status line:

```bash
#!/bin/bash
input=$(cat)

# ANSI color codes
BLUE='\033[94m'
GREEN='\033[92m'
YELLOW='\033[93m'
RED='\033[91m'
CYAN='\033[96m'
RESET='\033[0m'

# Get git branch name
branch=$(git branch --show-current 2>/dev/null || echo "no-git")

# Get context usage percentage
percent=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | xargs printf "%.0f")

# Get main model name
model=$(echo "$input" | jq -r '.model.display_name // .data.model.display_name // ""')

# Check for active subagent
AGENT_TRACKER="/tmp/claude-subagent-$USER"
subagent=""
if [ -f "$AGENT_TRACKER" ]; then
  subagent=$(cat "$AGENT_TRACKER")
fi

# Color based on context usage
if [ "$percent" -lt 45 ]; then
  PERCENT_COLOR=$GREEN
elif [ "$percent" -lt 70 ]; then
  PERCENT_COLOR=$YELLOW
else
  PERCENT_COLOR=$RED
fi

# Build output
if [ -n "$model" ]; then
  if [ -n "$subagent" ]; then
    echo -e "${BLUE}${branch}${RESET} • ${PERCENT_COLOR}${percent}%${RESET} • ${model} ${CYAN}→ ${subagent}${RESET}"
  else
    echo -e "${BLUE}${branch}${RESET} • ${PERCENT_COLOR}${percent}%${RESET} • ${model}"
  fi
else
  echo -e "${BLUE}${branch}${RESET} • ${PERCENT_COLOR}${percent}%${RESET}"
fi
```

**`~/.claude/hooks/track-subagent.sh`** — Tracks when subagents start and stop:

```bash
#!/bin/bash
input=$(cat)
action="$1"
AGENT_TRACKER="/tmp/claude-subagent-$USER"

if [ "$action" = "start" ]; then
  echo "$input" | jq -r '.agent_type // "agent"' > "$AGENT_TRACKER"
elif [ "$action" = "stop" ]; then
  rm -f "$AGENT_TRACKER"
fi

exit 0
```

**`~/.claude/settings.json`** — Points to the script and hooks:

```json
{
  "hooks": {
    "SubagentStart": [{ "matcher": "", "hooks": [{ "type": "command", "command": "~/.claude/hooks/track-subagent.sh start" }] }],
    "SubagentStop": [{ "matcher": "", "hooks": [{ "type": "command", "command": "~/.claude/hooks/track-subagent.sh stop" }] }]
  },
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh",
    "padding": 0
  }
}
```

---

### Why It's Useful

- **Context %** tells you when to `/compact` (if it's getting high)
- **Model** confirms you're using the right Claude for the task
- **Branch** prevents accidental commits to the wrong branch

---

## Preview Markdown in Your Browser

If you write markdown files (notes, documentation, READMEs), you can preview them as beautifully styled pages in your browser – like how they'd look in Notion.

**What it does:** Converts any `.md` file into a styled HTML page and opens it in your browser. No more squinting at raw markdown.

---

### How to Set It Up

Ask Claude:

```
Set up mdview for me — a shell function that converts markdown files
to styled HTML using pandoc and opens them in my browser. I want
Notion-style CSS styling. Also add an mdrefresh function that rebuilds
the HTML without opening a new tab.
```

Claude will install pandoc (if needed), create the CSS file, and add the shell functions.

---

### How to Use It

**Open a preview:**

```bash
mdview my-file.md
```

This converts the file to HTML and opens it in your browser.

**Update after edits:**

```bash
mdrefresh
```

Then press `Cmd + R` in your browser to see the changes. (mdrefresh rebuilds the HTML but doesn't open a new tab.)
