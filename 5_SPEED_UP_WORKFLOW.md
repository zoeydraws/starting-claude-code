# Speed Up Your Workflow

Skills and shortcuts to save time.

---

## Built-in Commands

These work out of the box:

| Command    | What It Does                           |
| ---------- | -------------------------------------- |
| `/help`    | Shows available commands and skills    |
| `/clear`   | Clears conversation, starts fresh      |
| `/compact` | Summarizes conversation to save tokens |
| `/exit`    | Closes Claude Code                     |

---

## Skills — Quick Setup

Skills are multi-step workflows you trigger by typing `/name`. Here are three essential ones to get you started.

### Starter Skills

| Skill             | What It Does                                         |
| ----------------- | ---------------------------------------------------- |
| `/create-pr`      | Rebase onto main, handle conflicts, create pull request |
| `/review-session` | Summarize session and update SESSION_LOG.md          |
| `/maintain-docs`  | Review and condense docs to manage context size      |

### How to Install Them

**Option A: Ask Claude to create them**

1. Open one of the template files in the [`skills/`](skills/) folder (e.g., `create-pr/SKILL.md`)
2. Copy the contents
3. Tell Claude:

```
Create a /create-pr skill with these instructions:

[paste the contents here]
```

Claude will create the skill folder at `~/.claude/skills/create-pr/SKILL.md` for you.

**Option B: Copy the files manually (if you're comfortable with terminal)**

```bash
mkdir -p ~/.claude/skills
cp -r skills/* ~/.claude/skills/
```

### Skill File Format

Each skill is a folder containing a `SKILL.md` file:

```
~/.claude/skills/
└── commit/
    └── SKILL.md
```

The `SKILL.md` file has a description and instructions:

```markdown
---
description: What this skill does (shown in /help)
---

Instructions for Claude to follow when you run this skill.
```

See the [`skills/`](skills/) folder for full examples.

---

## Shortcuts — Simple Rules

For simple one-liner rules, add them to your CLAUDE.md instead of creating a file.

### Git Shortcuts

These are common git workflows that work well as shortcuts:

| Shortcut | What It Does |
|----------|--------------|
| `commit` | Stage all changes, write commit message, push |
| `pull-main` | Fetch and merge main into current branch |
| `new-branch <name>` | Check out main, pull latest, create new branch |

Add these to your `~/.claude/CLAUDE.md` (see [templates/STARTER_GLOBAL_CLAUDE.md](templates/STARTER_GLOBAL_CLAUDE.md) for examples).

### Custom Shortcuts

You can create any shortcut for things you say often:

```markdown
- **"shorter"**: When I say "shorter", rewrite your last response more concisely
```

Now typing `shorter` tells Claude to be more concise. Ask Claude to add more shortcuts as you need them.

---

## Quick Reference

| Type     | Where it lives       | When to use           |
| -------- | -------------------- | --------------------- |
| Skill    | `~/.claude/skills/`  | Multi-step workflow   |
| Shortcut | CLAUDE.md            | Simple one-liner rule |
