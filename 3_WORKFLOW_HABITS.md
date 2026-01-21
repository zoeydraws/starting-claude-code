# Workflow Habits

Day-to-day habits that keep your Claude Code sessions running smoothly. Think of these as hygiene — do them regularly and things stay clean.

---

## 1. Break Big Work into Phases

**Claude struggles with big chunks of work.**

Asking Claude to "build me a whole app" or "do this entire project" leads to messy or incomplete results. Claude works best on focused, specific chunks — not entire projects at once.

**Rule of thumb:** If the task would take you hours to do manually, break it into phases first.

| Instead of...                                   | Try...                                                                         |
| ----------------------------------------------- | ------------------------------------------------------------------------------ |
| "Build me a portfolio website"                  | "Let's plan out a portfolio site in phases. What are the key sections I need?" |
| "Analyze all 20 transcripts and write a report" | "Let's start with 3 transcripts. What themes do you notice?"                   |
| "Create the whole presentation"                 | "Help me outline the presentation first, then we'll build each section"        |

**Example:**

```
You: I need to reorganize all my research findings into a final report

Claude: That's a big task. Let's break it into phases:
- Phase 1: Review and tag all findings
- Phase 2: Group by theme
- Phase 3: Write section summaries
- Phase 4: Compile into final report

Which phase should we start with?
```

---

## 2. Plan Before You Execute

**Claude Code has two modes:**

| Mode         | What It Does                                                         | How to Enter            |
| ------------ | -------------------------------------------------------------------- | ----------------------- |
| Plan mode    | Claude researches and proposes an approach, but doesn't make changes | `Shift + Tab` to toggle |
| Execute mode | Claude makes actual changes to your files                            | Default mode            |

**When to use plan mode:**

- Starting a new phase of work
- Unfamiliar task where you want to see the approach first
- Anything that touches multiple files

**Example:**

```
You: [Shift + Tab to enter plan mode]
You: How should we reorganize the transcripts folder?

Claude: Here's my suggested approach:
1. Create subfolders by participant type
2. Rename files with consistent naming
3. Move files to appropriate folders
4. Update any references

[Claude doesn't make changes yet — just plans]

You: [Shift + Tab to exit plan mode]
You: Ok let's do step 1
```

**Why this matters:**

- You see Claude's thinking before it acts
- You catch bad ideas early, before any changes are made

---

## 3. Execute One Step at a Time

**After planning, don't ask Claude to do everything at once.**

Execute one step, review the result, then move to the next. This gives you control and lets you course-correct.

**The pattern:**

```
You: Let's do step 1 — create the subfolders

Claude: [Creates subfolders, shows what it did]

You: Good. Now step 2 — rename the files

Claude: [Renames files, shows what it did]

You: Actually, I don't like that naming format. Let's try...
```

**Why this matters:**

- You can catch mistakes early
- You can change direction without undoing a lot of work
- You learn how Claude works by seeing each step

**For beginners:** Do things manually step-by-step at first. This helps you understand Claude's behavior. You can let Claude do more autonomously once you're comfortable.

---

## 4. Be Careful with Powerful Commands

**Claude sometimes suggests commands that can make big changes to your system.**

Most commands are safe, but a few can delete files permanently, change system settings, or do things that are hard to undo. You don't need to memorize these — just know what to watch for.

**When you see these patterns, ask Claude to explain before running:**

| Pattern            | What it does              | Why to be careful                                  |
| ------------------ | ------------------------- | -------------------------------------------------- |
| `sudo ...`         | Runs as administrator     | Can modify system files, install software globally |
| `rm -rf ...`       | Deletes files/folders     | Permanent deletion, no trash, no undo              |
| `git push --force` | Overwrites remote history | Can delete other people's work                     |
| `chmod` / `chown`  | Changes file permissions  | Can lock you out of files or expose them           |
| `npm install -g`   | Installs globally         | Affects your whole system, not just this project   |

**Good news:** Claude Code asks for permission before running commands, so you always have a chance to say no. But knowing these patterns helps you ask the right questions.

**Rule of thumb:** If a command looks unfamiliar or has flags you don't recognize, ask Claude to explain it in plain English first.

---

## 5. Set Up CLAUDE.md for Your Preferences

**What is CLAUDE.md?**
A file containing instructions for Claude. Claude reads it at the start of every session and follows those rules. You can ask Claude to add rules to this file for you.

**Two types:**

| Type | Location | Purpose |
|------|----------|---------|
| Global | `~/.claude/CLAUDE.md` | Your personal preferences for ALL projects |
| Project | `[project]/CLAUDE.md` | Rules specific to one project |

**Why this matters:**
Instead of repeating yourself every session ("don't use emojis", "always explain what you're doing"), you tell Claude once to add it to CLAUDE.md.

**How to set it up:**
See the templates folder for starter files you can customize.

---

## 6. Use SESSION_LOG for Continuity

**The problem:**
Claude Code doesn't automatically remember previous sessions. You might have to re-explain context each time.

**The solution:**
Keep a SESSION_LOG.md file in your project. At the end of each session, ask Claude to update it with what you did.

**The pattern:**
```

End of session:
You: Update SESSION_LOG.md with what we did today

Claude: [Adds entry with date, changes, decisions, next steps]

```

```

Start of next session:
You: Read SESSION_LOG.md to catch up on where we left off

Claude: [Reads the log and has context]

```

**Tip:** You can set up a `/review-session` skill to automate this. See [5_SPEED_UP_WORKFLOW.md](5_SPEED_UP_WORKFLOW.md) for how to install it.

---

## 7. Clear Context After Each Task

**The problem:**
As your conversation grows, Claude has to "compact" (summarize) older context to make room for new work. This can lose details and slow things down.

**The solution:**
Clear context after completing each task. This gives Claude a fresh start with full capacity.

**The workflow:**
```

1. Complete your task
2. /review-session → Claude updates SESSION_LOG.md
3. commit → Push changes if using version control (optional)
4. /clear → Clear conversation, fresh context

```

**Why this matters:**
- Claude works better with focused, fresh context
- Your work is saved in files and SESSION_LOG before clearing
- Next time you start, Claude reads SESSION_LOG to catch up

**Example:**
```

You: [Finish reorganizing the research docs]

You: /review-session

Claude: [Updates SESSION_LOG.md with what you did]

You: commit

Claude: [Commits and pushes changes]

You: /clear

[Fresh context — ready for next task]

```

---

## 8. Claude Code vs Claude.ai — When to Use Which

| Use Claude Code when... | Use Claude.ai when... |
|------------------------|----------------------|
| Working with files in a project | Quick questions with no files |
| Need to make edits to documents | Brainstorming ideas |
| Want Claude to read multiple files | Don't need file access |
| Running commands (git, etc.) | Just want to chat |
| Repetitive tasks across files | One-off requests |

**Rule of thumb:** If you'd be copy-pasting between Claude.ai and your files, use Claude Code instead.

---

## 9. Control What Claude Sees

**Claude reads your open files and selections in VS Code.** This is powerful but requires awareness.

**Use selections to focus Claude's attention:**
When you select lines in VS Code before prompting, Claude sees that selection as context. Use this to:
- Point Claude to the exact section you want to edit
- Show Claude a specific piece of code to explain or fix
- Focus Claude on one part of a large file

**Example:**
```

1. Select lines 45-60 in your file
2. Type: "Simplify this section"
3. Claude knows exactly which lines you mean

```

**Close sensitive files before starting Claude:**
Claude can see the contents of open files. Before starting a Claude session:
- Close any files with API keys, passwords, or secrets
- Close `.env`, `.env.local`, or credential files
- Select something else (like your main code file) so secrets aren't in context

**Why this matters:**
- Your selections give Claude precise context
- Closing secret files prevents accidentally sharing sensitive data
- You control what Claude sees, not just what you type

---

## 10. Paste Images for Visual Context

**Claude can see images you paste into the terminal.**

This is useful for quick UI or prototype fixes. Instead of describing what's wrong, just show Claude.

**How to do it:**
1. Take a screenshot or copy an image to your clipboard
2. Paste directly into the Claude Code terminal in VS Code (`Cmd + V`)
3. Ask Claude what you want

**Example:**
```

[Paste screenshot of a button that looks off]
You: The spacing on this button looks wrong. Can you fix it?

Claude: I can see the button has uneven padding. I'll adjust the CSS...

```

**Good for:**
- UI bugs ("this doesn't look right")
- Comparing design vs implementation
- Showing error messages or console output
- Quick feedback on prototypes

---

## Quick Reference

| Habit | When |
|-------|------|
| Break into phases | Before starting big work |
| Plan mode | Before executing unfamiliar tasks |
| One step at a time | During execution |
| Watch for powerful commands | When Claude suggests unfamiliar commands |
| CLAUDE.md | Set up once, update as needed |
| SESSION_LOG | End of each session |
| Clear context | After completing a task |
| Control what Claude sees | Before starting Claude, during prompting |
| Paste images | When visuals explain faster than words |

---

## Next Steps

- Set up your CLAUDE.md files using the templates in `templates/`
- Learn how to get better output in [4_GETTING_GOOD_OUTPUT.md](4_GETTING_GOOD_OUTPUT.md)
