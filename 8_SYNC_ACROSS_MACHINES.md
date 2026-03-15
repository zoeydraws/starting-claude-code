# 8. Sync Your Config Across Machines

Your `~/.claude` folder holds everything that makes Claude Code *yours* – your global instructions, skills, settings, and hooks. By default, this folder only lives on your current machine. If you switch to a laptop, a work computer, or set up a new Mac, you'd have to rebuild everything from scratch.

This guide shows you how to sync your `~/.claude` folder across machines using a private GitHub repo.

---

## What's in ~/.claude?

Here's what builds up over time as you use Claude Code:

| File/Folder    | What it is                                                                    |
| -------------- | ----------------------------------------------------------------------------- |
| `CLAUDE.md`    | Your global instructions – preferences, rules, and conventions for every project |
| `settings.json`| Permissions, hooks, model preferences                                         |
| `skills/`      | Your custom slash commands (e.g. `/review-session`, `/md`)                    |
| `agents/`      | Custom agent definitions                                                      |
| `hooks/`       | Hook scripts that run on specific events                                      |

There are also folders Claude Code generates automatically (cache, history, debug logs, etc.) – we won't sync those since they're machine-specific and get recreated on their own.

---

## Step 1: Create a Private GitHub Repo

Go to [github.com/new](https://github.com/new) and create a new repository:

- **Name:** something like `dot-claude`
- **Visibility:** Private (this contains your personal preferences)
- **Don't** add a README, `.gitignore`, or license – Claude will set those up

Copy the repo URL. It'll look like: `https://github.com/YOUR-USERNAME/dot-claude.git`

---

## Step 2: Set Up the Sync

Give Claude Code this prompt (replace the placeholders with your own info):

````
Set up my ~/.claude folder as a git repo that syncs to GitHub.

My repo URL is: https://github.com/YOUR-USERNAME/dot-claude.git
My GitHub username is: YOUR-USERNAME
My email is: YOUR-EMAIL

Here's what to do:

1. Initialize ~/.claude as a git repo:

```bash
cd ~/.claude
git init
```

2. Create ~/.claude/.gitignore with these contents:

```
# Credentials (sensitive)
.credentials.json

# Machine-specific ephemeral data
.DS_Store
history.jsonl
stats-cache.json
debug/
file-history/
cache/
image-cache/
paste-cache/
shell-snapshots/
session-env/
todos/
tasks/
plans/
ide/
plugins/
backups/
telemetry/
statsig/
projects/
sessions/
```

3. Set git identity for this repo:

```bash
git -C ~/.claude config user.name "YOUR-USERNAME"
git -C ~/.claude config user.email "YOUR-EMAIL"
```

4. Make the initial commit and push:

```bash
cd ~/.claude
git add -A
git commit -m "Initial commit: Claude Code global config"
git remote add origin https://github.com/YOUR-USERNAME/dot-claude.git
git branch -M main
git push -u origin main
```

5. Add these sync aliases to my ~/.zshrc:

```bash
# Claude Code config sync aliases
alias claude-sync='git -C ~/.claude pull'
alias claude-save='git -C ~/.claude add -A && git -C ~/.claude commit -m "sync config" && git -C ~/.claude push'
```

Then run `source ~/.zshrc` to activate them.
````

**Before running this**, make sure you're logged in to GitHub CLI. If you're not sure, tell Claude:

```
Check if I'm logged in to GitHub CLI. If not, log me in.
```

---

## What the .gitignore Does

You might be wondering why we skip certain files. Here's the reasoning:

- **`.credentials.json`** – contains your auth tokens. Never commit secrets to git.
- **`history.jsonl`, `cache/`, `debug/`, etc.** – generated automatically by Claude Code on each machine. They'd cause constant merge conflicts and aren't useful to sync.
- **`projects/`** – auto-memory that Claude Code creates per-project. It references local file paths that won't match on another machine.

**Everything else syncs:** your `CLAUDE.md`, `skills/`, `settings.json`, `hooks/`, `agents/`, and any other config you add.

---

## What the Aliases Do

After setup, you'll have two commands:

| Command        | What it does                                              |
| -------------- | --------------------------------------------------------- |
| `claude-sync`  | Pulls the latest config from GitHub to your machine       |
| `claude-save`  | Stages all changes, commits, and pushes to GitHub         |

You run these in your regular terminal (not inside Claude Code).

---

## Auto-Save When Your Config Changes

Instead of remembering to run `claude-save` manually, you can set up your `/review-session` skill to do it automatically whenever it updates global files. (If you haven't set up `/review-session` yet, see [5_SPEED_UP_WORKFLOW.md](5_SPEED_UP_WORKFLOW.md) for how to install skills.)

Tell Claude:

```
Update my /review-session skill to automatically run claude-save
after it updates global files (~/.claude/CLAUDE.md or ~/.claude/skills/).

Add a new step after the "UPDATE Global CLAUDE.md" step:

### Sync Global Config (After Global Changes)

Only run when the previous step actually updated ~/.claude/CLAUDE.md
or any file in ~/.claude/skills/.

Action: Run claude-save to push global config changes to the remote repo:

source ~/.zshrc && claude-save

Skip this step if no global files were changed in this session.
```

This way, every time you end a session with `/review-session` and it updates your global CLAUDE.md or adds a skill, Claude will automatically push those changes to your repo. No extra step to remember.

**Note:** If you use `/maintain-docs`, it only touches project-level files (project CLAUDE.md and SESSION_LOG.md), so it doesn't need this – your global config won't change during a `/maintain-docs` run.

---

## Setting Up a New Machine

When you get a new computer or want to sync to a second machine, give Claude Code this prompt (replace the placeholders):

````
Set up my Claude Code config from my synced GitHub repo.

My repo URL is: https://github.com/YOUR-USERNAME/dot-claude.git
My GitHub username is: YOUR-USERNAME
My email is: YOUR-EMAIL

Here's what to do:

1. Check if I'm logged in to GitHub CLI. If not, log me in.

2. If ~/.claude already exists, rename it:

```bash
mv ~/.claude ~/.claude-backup
```

3. Clone my config repo:

```bash
git clone https://github.com/YOUR-USERNAME/dot-claude.git ~/.claude
```

4. Set git identity for the repo:

```bash
git -C ~/.claude config user.name "YOUR-USERNAME"
git -C ~/.claude config user.email "YOUR-EMAIL"
```

5. Add these sync aliases to my ~/.zshrc (if they're not already there):

```bash
# Claude Code config sync aliases
alias claude-sync='git -C ~/.claude pull'
alias claude-save='git -C ~/.claude add -A && git -C ~/.claude commit -m "sync config" && git -C ~/.claude push'
```

Then run `source ~/.zshrc` to activate them.
````

After this, launch Claude Code with `claude` and everything will be there – your skills, settings, and global CLAUDE.md. Claude Code will regenerate all the ephemeral folders (cache, history, etc.) automatically.

---

## Daily Workflow

You don't need to sync every day – only when you've made changes you want on your other machines.

| When                                                  | What to run                                     |
| ----------------------------------------------------- | ----------------------------------------------- |
| Starting work on a different machine                  | `claude-sync` (pull latest)                     |
| After changing global CLAUDE.md, skills, or settings  | `claude-save` (push changes)                    |
| Using `/review-session` with auto-save set up         | Nothing – it saves automatically                |

Most sessions you won't change any global config, so you won't need to run anything extra.
