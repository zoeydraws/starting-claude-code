# Slash Commands

Slash commands are shortcuts that trigger pre-written prompts. Instead of typing the same instructions repeatedly, you type `/command-name` and Claude follows a defined workflow.

## What Are Slash Commands?

**Think of them as saved shortcuts for complex requests.**

Instead of typing:
```
Stage all my changes, write a descriptive commit message, and push to the remote repository. Don't ask me to confirm — just do it.
```

You type:
```
/commit
```

Same result, much faster.

---

## Built-in vs Custom Commands

| Type | What It Is | Examples |
|------|-----------|----------|
| Built-in | Commands that come with Claude Code | `/help`, `/clear`, `/exit` |
| Custom | Commands you create in CLAUDE.md | `/commit`, `/review-session` |

---

## Built-in Commands

These work out of the box:

| Command | What It Does |
|---------|--------------|
| `/help` | Shows available commands and how to use Claude Code |
| `/clear` | Clears conversation history, starts fresh |
| `/exit` | Closes Claude Code |
| `/compact` | Summarizes conversation to save space |

---

## Custom Commands (The Powerful Part)

You define these in your CLAUDE.md file. When you type the command, Claude reads the full instructions from your file.

### Example: The `/commit` Shortcut

In your global CLAUDE.md, you might have:

```markdown
## Workflow & Communication

- **"commit" shortcut**: When user says "commit" or "/commit",
  stage all changes, commit with a descriptive message, and push
  to remote. No need to ask for confirmation.
```

Now whenever you type `/commit` or just "commit", Claude:
1. Stages your changes
2. Writes a commit message
3. Pushes to your repository
4. All without extra prompts

**Bonus: Auto-deploy to Vercel**
If you've connected your GitHub repo to Vercel (see [1_SETUP_GUIDE.md](1_SETUP_GUIDE.md#optional-set-up-github--vercel-for-auto-deploy)), every `/commit` automatically triggers a deploy. Your site updates without any extra steps.

### Example: The `/review-session` Command

For tracking work across sessions:

```markdown
## Session Review Process

When user says "/review-session":
1. Summarize what we did this session
2. Note any decisions made
3. Update SESSION_LOG.md with an entry
4. List suggested next steps
```

Now at the end of each work session:
```
/review-session
```

Claude handles the documentation automatically.

---

## Creating Your Own Commands

### Step 1: Identify Repetitive Requests

What do you ask Claude to do repeatedly? Examples:
- "Summarize this document for executives"
- "Check this file for formatting issues"
- "Update the research log"

### Step 2: Write the Full Instruction

Be specific. Include:
- What Claude should do
- What format you want
- Whether to ask for confirmation or just do it

### Step 3: Add to CLAUDE.md

Add a section describing the shortcut:

```markdown
## Custom Commands

- **"/summarize-for-execs"**: Read the specified document and create
  a 3-bullet executive summary. Focus on decisions needed and
  recommendations. Keep it under 100 words.

- **"/format-check"**: Review the specified file for:
  - Consistent heading levels
  - Proper markdown formatting
  - Notion compatibility (no horizontal rules)
  Report issues as a checklist.
```

### Step 4: Use It

```
/summarize-for-execs research-findings.md
```

---

## Commands for UX/Design Work

Here are some useful commands to consider:

### For Research Synthesis

```markdown
- **"/extract-quotes"**: Read the specified transcript and pull out
  notable quotes. Format as: "Quote text" — **Participant role**
```

### For Documentation

```markdown
- **"/update-log"**: Add an entry to SESSION_LOG.md with today's date,
  what we accomplished, decisions made, and next steps.
```

### For Review

```markdown
- **"/notion-check"**: Review the file for Notion compatibility:
  - No horizontal rules (---)
  - No ASCII diagrams
  - Tables are okay
  Flag any issues found.
```

### For Handoff

```markdown
- **"/stakeholder-summary"**: Create a non-technical summary of
  [document] suitable for sharing with leadership. Focus on
  implications and recommendations, not methodology.
```

---

## Tips for Good Commands

**Be specific about output format:**
```
Format as a bulleted list with bold headers
```

**Specify when to ask vs just do:**
```
Don't ask for confirmation — just make the changes
```
vs
```
Show me the proposed changes before making them
```

**Include edge cases:**
```
If no issues are found, just say "No issues found"
instead of listing what you checked
```

---

## Where Commands Live

| Command Type | Where to Define |
|--------------|-----------------|
| Personal shortcuts (all projects) | `~/.claude/CLAUDE.md` |
| Project-specific commands | `[project]/CLAUDE.md` |

Project commands override global ones if they have the same name.

---

## Quick Start

1. Open your global CLAUDE.md (or create it at `~/.claude/CLAUDE.md`)
2. Add one simple command (like `/commit`)
3. Test it in Claude Code
4. Add more as you discover repeated workflows

The templates folder has a starter file with common commands already defined.
