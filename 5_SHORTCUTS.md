# Shortcuts

Speed up your workflow with slash commands and shortcuts.

---

## Built-in Commands

These work out of the box:

| Command    | What It Does                           |
| ---------- | -------------------------------------- |
| `/help`    | Shows available commands               |
| `/clear`   | Clears conversation, starts fresh      |
| `/compact` | Summarizes conversation to save tokens |
| `/exit`    | Closes Claude Code                     |

---

## Slash Commands — Quick Setup

Slash commands are multi-step workflows you trigger by typing `/name`. Here are three essential ones to get you started.

### The Three Starter Commands

| Command           | What It Does                                    |
| ----------------- | ----------------------------------------------- |
| `/commit`         | Stage all changes, write commit message, push   |
| `/pull-main`      | Fetch and merge main branch into current branch |
| `/review-session` | Summarize session and update SESSION_LOG.md     |

### How to Install Them

**Option A: Ask Claude to create them**

1. Open one of the template files in the [`commands/`](commands/) folder (e.g., `commit.md`)
2. Copy the contents
3. Tell Claude:

```
Create a /commit slash command with these instructions:

[paste the contents here]
```

Claude will create the file in `~/.claude/commands/commit.md` for you.

**Option B: Copy the files manually (if you're comfortable with terminal)**

```bash
mkdir -p ~/.claude/commands
cp commands/*.md ~/.claude/commands/
```

### Command File Format

Each command is a `.md` file with a description and instructions:

```markdown
---
description: What this command does (shown in /help)
---

Instructions for Claude to follow when you run this command.
```

See the [`commands/`](commands/) folder for full examples.

---

## Shortcuts — Simple Rules

For simple one-liner rules, add them to your CLAUDE.md instead of creating a file.

**Example** — add this to `~/.claude/CLAUDE.md`:

```markdown
- **"shorter"**: When I say "shorter", rewrite your last response more concisely
```

Now typing `shorter` tells Claude to be more concise. Ask Claude to add more shortcuts as you need them.

---

## Quick Reference

| Type          | Where it lives         | When to use           |
| ------------- | ---------------------- | --------------------- |
| Slash command | `~/.claude/commands/`  | Multi-step workflow   |
| Shortcut      | CLAUDE.md              | Simple one-liner rule |
