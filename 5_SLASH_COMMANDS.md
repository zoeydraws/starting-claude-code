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

### Step 3: Ask Claude to Add It

Tell Claude what you want the command to do:

```
You: Add a /summarize-for-execs command to my global CLAUDE.md.
     It should read the specified document and create a 3-bullet
     executive summary. Focus on decisions needed and recommendations.
     Keep it under 100 words.

Claude: [Adds the command to your CLAUDE.md file]
```

Claude will write the properly formatted entry for you — you don't need to know the exact syntax.

### Step 4: Use It

```
/summarize-for-execs research-findings.md
```

---

## Commands for UX/Design Work

Here are some useful commands you can ask Claude to create:

### For Research Synthesis

```
Add a /extract-quotes command that reads a transcript and pulls out
notable quotes. Format each as: "Quote text" — Participant role
```

### For Documentation

```
Add a /update-log command that adds an entry to SESSION_LOG.md with
today's date, what we accomplished, decisions made, and next steps.
```

### For Review

```
Add a /notion-check command that reviews a file for Notion compatibility.
Check for: no horizontal rules, no ASCII diagrams, tables are okay.
Flag any issues found.
```

### For Handoff

```
Add a /stakeholder-summary command that creates a non-technical summary
suitable for leadership. Focus on implications and recommendations,
not methodology.
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

1. Think of something you ask Claude to do repeatedly
2. Tell Claude: "Add a /[name] command to my global CLAUDE.md that [does X]"
3. Test it by typing `/[name]` in Claude Code
4. Ask Claude to add more as you discover repeated workflows

The templates folder has examples of common commands to give you ideas.
