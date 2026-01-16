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

## Principle 2: One Thing at a Time

**The pattern:**
Ask for one task, see it through, then ask for the next.

**Why this matters:**
Bundling multiple requests often leads to confusion or missed items. Single requests give you more control.

**Instead of:**
```
Reorganize my doc, fix the typos, and add a summary at the end
```

**Try:**
```
Let's reorganize the doc first. Can you show me a new outline?
```

Then after that's done:
```
Now let's fix any typos
```

## Principle 3: Teach Claude Your Preferences with CLAUDE.md

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

## Principle 4: Use SESSION_LOG for Continuity

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

## Principle 5: Claude Code vs Claude.ai — When to Use Which

| Use Claude Code when... | Use Claude.ai when... |
|------------------------|----------------------|
| Working with files in a project | Quick questions with no files |
| Need to make edits to documents | Brainstorming ideas |
| Want Claude to read multiple files | Don't need file access |
| Running commands (git, etc.) | Just want to chat |
| Repetitive tasks across files | One-off requests |

**Rule of thumb:** If you'd be copy-pasting between Claude.ai and your files, use Claude Code instead.

## Principle 6: Be Specific About What You Want

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

## Principle 7: Don't Hesitate to Say "No" or "Stop"

Claude won't be offended. It's a tool.

- Don't like a suggestion? Say no.
- Want to try a different approach? Tell Claude.
- Realized you asked the wrong thing? Start over.

**Useful phrases:**
- "Actually, let's try a different approach"
- "Stop — I want to think about this first"
- "Undo that and let's go back to what we had"
- "Wait, can you explain what you're about to do?"

## Principle 8: Review Changes Before Approving

Claude will show you "diffs" — comparisons between old and new content. Take a moment to actually read them.

**Look for:**
- Unintended changes (Claude sometimes "improves" things you didn't ask about)
- Lost content (make sure nothing important was deleted)
- Formatting changes (Claude might change your preferred style)

**It's okay to say:**
```
I approve the first change but not the second one
```

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
