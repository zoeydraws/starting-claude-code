# Your First Session

You've installed Claude Code and opened it in your project folder. Now what? This guide walks you through your first 15 minutes.

## The Basics

**How to talk to Claude:**
Just type your question or request and press Enter. It's a conversation, like chatting.

**How to know Claude is thinking:**
You'll see a spinner or "thinking" indicator. Wait for Claude to finish before typing more.

**How to say yes or no:**
When Claude suggests changes, you'll see options like:
- `y` = yes, do it
- `n` = no, don't do it
- `e` = edit (modify the suggestion)

Just type the letter and press Enter.

## Try These First Commands

### 1. Ask Claude what's in your project

```
What files are in this project? Give me a quick overview.
```

**What happens:** Claude will scan your folders and summarize what it finds. This helps Claude (and you) understand what you're working with.

### 2. Ask a question about your content

```
Can you read [filename] and summarize the key points?
```

Replace `[filename]` with an actual file in your project.

**What happens:** Claude reads the file and gives you a summary. This confirms Claude can access your files.

### 3. Ask Claude to help with a small task

```
Can you fix the typo in the heading of [filename]?
```

**What happens:** Claude will:
1. Read the file
2. Show you what it plans to change
3. Wait for your approval before making the change

This is the core workflow — Claude suggests, you approve.

## Understanding Claude's Responses

**Tool usage:**
You might see Claude mention "using Read tool" or "using Edit tool". These are Claude's ways of interacting with your files. You don't need to understand them — just know Claude is working.

**Asking for permission:**
Claude will frequently ask "Should I proceed?" or show you a diff (before/after comparison). Always review before saying yes.

**Long responses:**
If Claude gives a very long response, you can scroll up in Terminal to see everything. On Mac, scroll with your trackpad or use `Cmd + Up Arrow`.

## Common First-Timer Questions

### "How do I stop Claude mid-response?"

Press `Ctrl + C`. This interrupts whatever Claude is doing.

### "How do I exit Claude Code?"

Type `/exit` or press `Ctrl + C` twice.

### "Can I undo a change Claude made?"

Yes! If your project uses git (version control), Claude's changes can be reverted. If you're not using git, Claude usually asks before making changes so you can say no.

For important projects, consider learning basic git — it's like "undo history" for your files.

### "Claude changed something I didn't want"

Tell Claude directly:
```
Please undo that last change
```

Or if you're using git:
```
Please revert the last commit
```

### "How do I start over?"

Type `/clear` to clear the conversation history and start fresh.

## Your First Real Task

Now try something useful for your actual work. Here are ideas for UX/Design folks:

**For research synthesis:**
```
Read through all the .md files in the transcripts folder and list the common themes you notice
```

**For organizing:**
```
What's the structure of this project? How are the folders organized?
```

**For writing:**
```
Help me write a summary of [document] for my stakeholders
```

**For review:**
```
Read [filename] and suggest any improvements for clarity
```

## When You're Done

You can:
- Type `/exit` to close Claude Code
- Just close the Terminal window
- Press `Ctrl + C` twice

Your conversation doesn't automatically save, but your files do. Next session, Claude won't remember this conversation unless you set up a SESSION_LOG (covered in [3_WORKING_PRINCIPLES.md](3_WORKING_PRINCIPLES.md)).

---

## Quick Reference

| Action | How |
|--------|-----|
| Ask Claude something | Just type and press Enter |
| Approve a change | Type `y` and Enter |
| Reject a change | Type `n` and Enter |
| Stop Claude | `Ctrl + C` |
| Exit Claude Code | `/exit` or `Ctrl + C` twice |
| Clear conversation | `/clear` |
| Scroll up | Trackpad or `Cmd + Up Arrow` |
