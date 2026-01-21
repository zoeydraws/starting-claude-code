# Getting Good Output

How to prompt and work with Claude to get quality results. These are techniques for better collaboration.

---

## 1. Claude Suggests, You Decide

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

## 2. Ask Claude What It Understands

**Before Claude starts working, ask it to summarize the task back to you.**

This catches misunderstandings before they become wasted effort.

```
Before you start, tell me what you understand the task to be
```

**Why this matters:**
You'll quickly see if Claude is about to go in the wrong direction — and you can correct it before any work happens.

---

## 3. Make Claude Ask Questions

**Let Claude ask for what it needs instead of guessing.**

When you give Claude a lot of details upfront, you're guessing what it needs to know. Claude fills any gaps with assumptions — which may be wrong.

When Claude asks questions, it's asking for exactly what it needs. This leads to better output with fewer revisions.

**Add this to your CLAUDE.md or say it directly:**
```
If you're unsure about anything, ask me before proceeding
```

**Or prompt it directly:**
```
Before writing this summary, ask me any clarifying questions
```

---

## 4. Make Claude Do Everything

**When Claude tells you how to do something, tell it to do it for you.**

When you ask "How do I do xyz?", Claude often responds with instructions for you to follow. But you don't have to do it yourself — tell Claude to execute it.

```
You: How do I push to GitHub?

Claude: Here's how you can push to GitHub:
1. Stage your changes with git add...
2. Commit with git commit...
3. Push with git push...

You: Do it for me

Claude: I'll commit and push your changes now...
```

**The mindset:** Your job is to direct and review. Claude's job is to execute.

---

## 5. Make Claude Get Better

**When something goes wrong, ask Claude how to avoid it next time.**

Claude can learn from mistakes in the conversation. When it makes an error or gives you something that's not quite right, ask:

```
How can you do this better next time?

How can you avoid this error in the future?

What should I tell you upfront to prevent this?
```

If Claude's answer is useful, add it to your CLAUDE.md so it remembers for future sessions.

---

## 6. Iterate, Don't Start Over

**When Claude's output isn't quite right, refine it — don't re-prompt from scratch.**

**Instead of:**
```
[Claude gives output you don't like]
You: Let me try again... [rewrites entire prompt]
```

**Try:**
```
[Claude gives output you don't like]
You: This is close, but make it shorter
You: Good, now make the tone more casual
You: Perfect, but change "utilize" to "use"
```

**Why this matters:**
- Faster than starting over
- Claude learns your preferences as you go
- You get closer to what you want with each iteration

---

## 7. Don't Hesitate to Say "No" or "Stop"

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

## 8. Review Changes Before Approving

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

## 9. Show an Example

**Sometimes it's easier to show Claude what you want than to describe it.**

Instead of explaining the exact format, tone, or structure — just paste an example.

```
Format it like this:

**Finding:** Users struggled with the navigation
**Impact:** High — affects task completion
**Recommendation:** Simplify the menu structure
```

Claude will match the pattern.

---

## Next Steps

- Learn about shortcuts in [5_SHORTCUTS.md](5_SHORTCUTS.md)
- Set up your CLAUDE.md with prompting preferences
