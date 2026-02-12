# Fun: Customize Your Status Line

The status line shows helpful info at a glance while you work.

![Status line example](images/status-line.png)

**What it shows:**
- **Branch** — Current git branch (green)
- **Context %** — How much of Claude's memory you're using (pink)
- **Model** — Which Claude model is active (e.g., Opus 4.5)
- **Accept edits** — Current edit approval mode (shift+tab to cycle)

---

## How to Enable It

Ask Claude:

```
Enable the terminal status line
```

Or configure it manually in your settings file at `~/.claude/settings.json`:

```json
{
  "terminal": {
    "statusLine": true
  }
}
```

---

## Cycling Through Edit Modes

Press `Shift + Tab` to cycle through:

| Mode | What It Means |
|------|---------------|
| Accept edits **on** | Claude applies edits automatically |
| Accept edits **off** | Claude asks before each edit |

Pick whichever feels comfortable — you can always change it mid-session.

---

## Why It's Useful

- **Context %** tells you when to `/compact` (if it's getting high)
- **Model** confirms you're using the right Claude for the task
- **Branch** prevents accidental commits to the wrong branch
