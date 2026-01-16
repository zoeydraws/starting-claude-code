# Session Log

Work timeline for the Starting Claude guide project. Newest entries at top.

---

## 2026-01-16 - Added Habit 8 and Language Tweaks

**Changes:**
- Added Habit 8: "Control What Claude Sees" to 3_WORKFLOW_HABITS.md
  - Using VS Code selections to focus Claude on specific lines
  - Closing sensitive files (.env, API keys) before starting Claude
- Updated CLAUDE.md language: "you write instructions" → "ask Claude to add rules"
  - Line 104: Added "You can ask Claude to add rules to this file for you"
  - Line 114: Changed "you write it once" → "you tell Claude once to add it"
- Updated Quick Reference table to include new habit

**Decisions:**
- Frame CLAUDE.md as something Claude updates for you (beginner-friendly)
- Security hygiene (closing secret files) belongs in workflow habits

**Current State:**
- Working: 8 habits in 3_WORKFLOW_HABITS.md, all updated
- Not yet committed to GitHub

**Next Steps:**
- Commit and push all changes
- Test guide with beginners
- Consider screenshots

---

## 2026-01-16 - Major Restructure: Habits vs Output

**Changes:**
- Split 3_WORKING_PRINCIPLES.md into two files:
  - 3_WORKFLOW_HABITS.md (7 habits) — operational hygiene
  - 4_GETTING_GOOD_OUTPUT.md (9 techniques) — prompting quality
- Added 5 new prompting principles:
  - Give Context First
  - Tell Claude Who It's For
  - Make Claude Ask Questions
  - Make Claude Do Everything
  - Iterate, Don't Start Over
- Renamed 4_SLASH_COMMANDS.md → 5_SLASH_COMMANDS.md
- Updated all cross-references in README, CLAUDE.md, 2_FIRST_SESSION.md

**Decisions:**
- Split content by purpose: "habits" = daily hygiene, "output" = quality techniques
- CLAUDE.md setup and Claude Code vs Claude.ai stay in Workflow Habits (operational)
- New prompting principles focus on making Claude work harder for you

**Current State:**
- Working: 9 files total, restructured and all references updated
- Not yet committed to GitHub

**Next Steps:**
- Commit and push restructure
- Test guide with beginners
- Consider screenshots

---

## 2026-01-16 - Added Context Management Principle

**Changes:**
- Added Principle 7: Clear Context After Each Task (review-session → commit → /clear workflow)
- Renumbered principles (now 11 total)
- Updated README messaging: "beginner guide, if you want advanced find Pras"
- Updated "some coding required, but you can learn as you go"

**Decisions:**
- Context management workflow: task complete → /review-session → commit → /clear
- Keeps Claude working with fresh, focused context instead of compacting old conversations

**Current State:**
- Working: 11 principles, all deployed to GitHub
- Guide messaging updated to be more casual/realistic

**Next Steps:**
- Test guide with actual beginners
- Consider screenshots

---

## 2026-01-16 - Initial Guide Creation

**Changes:**
- Created full guide structure with 8 files:
  - README.md, 1_SETUP_GUIDE.md, 2_FIRST_SESSION.md, 3_WORKING_PRINCIPLES.md, 4_SLASH_COMMANDS.md
  - templates/STARTER_GLOBAL_CLAUDE.md, STARTER_PROJECT_CLAUDE.md, SESSION_LOG_TEMPLATE.md
- Setup guide: VS Code-first approach (not standalone Terminal), macOS terminology, Cmd+J shortcut, Homebrew for permissions (no sudo)
- First session: Added /rewind and /resume commands, Escape to stop
- Working principles: Split into 10 principles — key addition is phases → plan → execute workflow (Principles 2-4)
- Added dividers between all H2 sections across all files
- Deployed to GitHub: https://github.com/zoeydraws/starting-claude-code

**Decisions:**
- Target audience: UX folks and Design Managers (non-technical)
- Start from VS Code terminal, not standalone Terminal app
- Cmd+J for terminal (Mac-native), not Ctrl+`
- Homebrew for Node permission issues instead of sudo
- Split "one thing at a time" into three principles: break into phases, plan mode, execute step-by-step
- Removed "Next steps" from project CLAUDE.md template (belongs in SESSION_LOG only)

**Current State:**
- Working: Complete guide deployed to GitHub
- All 8 files have consistent formatting with dividers

**Next Steps:**
- Test guide with actual beginners for feedback
- Consider adding screenshots for key steps
- May need Windows version later

---
