# Starting Claude Guide

## Project Overview

Beginner-friendly guide for getting started with Claude Code, targeted at UX folks and Design Managers with no coding/terminal experience.

**Repo:** https://github.com/zoeydraws/starting-claude-code

## Project Structure

```
/
├── README.md                    # Overview and navigation
├── 1_SETUP_GUIDE.md             # VS Code + installation steps
├── 2_FIRST_SESSION.md           # First 15 minutes walkthrough
├── 3_WORKING_PRINCIPLES.md      # 10 principles for working with Claude
├── 4_SLASH_COMMANDS.md          # Custom shortcuts explained
├── templates/
│   ├── STARTER_GLOBAL_CLAUDE.md
│   ├── STARTER_PROJECT_CLAUDE.md
│   └── SESSION_LOG_TEMPLATE.md
├── CLAUDE.md                    # This file
└── SESSION_LOG.md               # Work timeline
```

## Conventions

- **Audience assumption:** Zero technical knowledge — explain everything
- **VS Code first:** All instructions assume VS Code terminal, not standalone Terminal
- **macOS only:** Guide is Mac-specific (may add Windows later)
- **Dividers:** Use `---` between all H2 sections for visual separation

## Git Identity

```bash
git config user.name "zoeydraws"
git config user.email "zoeydraws@gmail.com"
```

## Key Decisions

- 2026-01-16: VS Code terminal approach (not standalone Terminal) — easier for non-technical users who already use VS Code for markdown
- 2026-01-16: Homebrew for Node permissions instead of sudo — safer for beginners
- 2026-01-16: Split "one thing at a time" into 3 principles (phases → plan → execute) — clearer mental model
