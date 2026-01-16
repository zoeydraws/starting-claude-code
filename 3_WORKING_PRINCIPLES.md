# Working Principles

Claude Code works best when you treat it as a collaborator, not a magic button. These principles will help you get better results and avoid frustration.

## Principle 1: Claude Suggests, You Decide

**The pattern:**
1. You ask for something
2. Claude proposes what it will do
3. You review and approve (or reject)
4. Claude executes

**Why this matters:**
Claude is powerful but not perfect. The approval step catches mistakes before they happen. Never feel rushed to approve — take time to read what Claude is suggesting.

**In practice:**
```
You: Can you reorganize the headings in my research doc?

Claude: I'll restructure the headings like this:
- [shows proposed changes]
Should I proceed?

You: Actually, keep the "Methods" section where it is

Claude: Got it, I'll reorganize everything except Methods...
```

---

## Principle 2: Break Big Work into Phases

**Claude struggles with big chunks of work.**

Asking Claude to "build me a whole app" or "do this entire project" leads to messy or incomplete results. Claude works best on focused, specific chunks — not entire projects at once.

**Rule of thumb:** If the task would take you hours to do manually, break it into phases first.

| Instead of... | Try... |
|---------------|--------|
| "Build me a portfolio website" | "Let's plan out a portfolio site in phases. What are the key sections I need?" |
| "Analyze all 20 transcripts and write a report" | "Let's start with 3 transcripts. What themes do you notice?" |
| "Create the whole presentation" | "Help me outline the presentation first, then we'll build each section" |

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

## Principle 3: Plan Before You Execute

**Claude Code has two modes:**

| Mode | What It Does | How to Enter |
|------|--------------|--------------|
| Plan mode | Claude researches and proposes an approach, but doesn't make changes | `Shift + Tab` to toggle |
| Execute mode | Claude makes actual changes to your files | Default mode |

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

## Principle 4: Execute One Step at a Time

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

## Principle 5: Teach Claude Your Preferences with CLAUDE.md

**What is CLAUDE.md?**
A file where you write instructions for Claude. Claude reads it at the start of every session and follows those rules.

**Two types:**

| Type | Location | Purpose |
|------|----------|---------|
| Global | `~/.claude/CLAUDE.md` | Your personal preferences for ALL projects |
| Project | `[project]/CLAUDE.md` | Rules specific to one project |

**Why this matters:**
Instead of repeating yourself every session ("don't use emojis", "always explain what you're doing"), you write it once in CLAUDE.md.

**How to set it up:**
See the templates folder for starter files you can customize.

---

## Principle 6: Use SESSION_LOG for Continuity

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

---

## Principle 7: Clear Context After Each Task

**The problem:**
As your conversation grows, Claude has to "compact" (summarize) older context to make room for new work. This can lose details and slow things down.

**The solution:**
Clear context after completing each task. This gives Claude a fresh start with full capacity.

**The workflow:**
```
1. Complete your task
2. /review-session     → Claude updates SESSION_LOG.md
3. commit              → Push changes if using version control (optional)
4. /clear              → Clear conversation, fresh context
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

## Principle 8: Claude Code vs Claude.ai — When to Use Which

| Use Claude Code when... | Use Claude.ai when... |
|------------------------|----------------------|
| Working with files in a project | Quick questions with no files |
| Need to make edits to documents | Brainstorming ideas |
| Want Claude to read multiple files | Don't need file access |
| Running commands (git, etc.) | Just want to chat |
| Repetitive tasks across files | One-off requests |

**Rule of thumb:** If you'd be copy-pasting between Claude.ai and your files, use Claude Code instead.

---

## Principle 9: Be Specific About What You Want

**Vague requests lead to mismatched results.**

**Instead of:**
```
Make this better
```

**Try:**
```
Make this more concise — it's for busy executives who skim
```

**Instead of:**
```
Organize this
```

**Try:**
```
Group these findings by theme, with the most common themes first
```

---

## Principle 10: Don't Hesitate to Say "No" or "Stop"

Claude won't be offended. It's a tool.

- Don't like a suggestion? Say no.
- Want to try a different approach? Tell Claude.
- Realized you asked the wrong thing? Start over.

**Useful phrases:**
- "Actually, let's try a different approach"
- "Stop — I want to think about this first"
- "Undo that and let's go back to what we had"
- "Wait, can you explain what you're about to do?"

---

## Principle 11: Review Changes Before Approving

Claude will show you "diffs" — comparisons between old and new content. Take a moment to actually read them.

**Look for:**
- Unintended changes (Claude sometimes "improves" things you didn't ask about)
- Lost content (make sure nothing important was deleted)
- Formatting changes (Claude might change your preferred style)

**It's okay to say:**
```
I approve the first change but not the second one
```

---

## Common Mistakes to Avoid

| Mistake | Better Approach |
|---------|-----------------|
| Approving without reading | Take 10 seconds to review |
| Asking for multiple things at once | One task at a time |
| Getting frustrated and quitting | Tell Claude to try differently |
| Never setting up CLAUDE.md | Spend 10 min on templates |
| Copy-pasting when Claude Code could edit | Let Claude make the change |

---

## Next Steps

- Set up your CLAUDE.md files using the templates in `templates/`
- Learn about slash commands in [4_SLASH_COMMANDS.md](4_SLASH_COMMANDS.md)
