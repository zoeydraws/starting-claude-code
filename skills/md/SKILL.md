---
name: md
description: Create, format, and preview markdown files with Notion + pandoc compatibility
---

# Markdown Skill

Two modes: **create/format** a markdown file, or **preview** one in the browser.

## Mode 1: Create & Format

When creating or editing markdown files, apply all of these formatting rules:

### Formatting Rules

1. **Blank line before lists.** Always add a blank line between a `**Bold label:**` line and the bullet list that follows it. Without the blank line, pandoc renders bullets as inline text.

   Good:
   ```md
   **For agencies:**

   - Bullet one
   - Bullet two
   ```

   Bad:
   ```md
   **For agencies:**
   - Bullet one
   - Bullet two
   ```

2. **En-dashes, not em-dashes.** Use `–` (en-dash) not `—` (em-dash) throughout.

3. **Notion heading promotion.** When the file is intended for Notion paste, promote all headings up one level (`##` → `#`, `###` → `##`, `####` → `###`) but keep the first `#` title as-is. Notion treats `#` as a page-level heading, so document sections need to start at `#` not `##`. Only apply when the user says it's for Notion.

4. **Table formatting.** Use consistent pipe alignment. Always include a header separator row (`|---|---|`).

5. **Section spacing.** One blank line after headings, one blank line before and after horizontal rules (`---`), one blank line between sections.

## Mode 2: Preview

### Open (first time)

When user says **"open [file].md"** or **"pandoc [file]"**, run:

```bash
source ~/.zshrc && mdview "<path-to-file>"
```

- Uses pandoc + Notion-style CSS (`~/.pandoc/notion.css`)
- Outputs self-contained HTML to `/tmp/mdview.html` and opens in default browser

### Refresh (already open)

When user says **"refresh"**, run:

```bash
source ~/.zshrc && mdrefresh
```

- Rebuilds the HTML without opening a new browser tab
- User will Cmd+R manually to see changes
- Don't auto-open URLs – user will refresh manually

## When to Apply

- **Always apply formatting rules** (Mode 1) when creating or editing any `.md` file, even if the user doesn't explicitly invoke `/md`
- **Only run preview commands** (Mode 2) when the user asks to open or refresh
