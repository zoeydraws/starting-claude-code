---
name: maintain-docs
description: Review and condense documentation files to manage context length
---

# Maintain Documentation

Review and maintain project documentation files to keep them useful as they grow.

## Your Tasks

### 1. Check SESSION_LOG.md (If Exists)

**Action:** Read SESSION_LOG.md and identify entries older than 2 weeks.

**For each old entry:**
1. **Extract architectural decisions** - Any "Why X over Y", patterns established, or design choices
2. **Condense entry** to 1-2 lines:
   ```
   ## YYYY-MM-DD - Brief Title
   One-line summary of what was done
   ```
3. **Migrate decisions** to project CLAUDE.md (with date)

**Keep:**
- Recent 2 weeks: full detailed entries
- Older: condensed to 1-2 lines

---

### 2. Check Project CLAUDE.md (If Exists)

**Line count check:**
- Read file and count lines
- If over 800 lines: suggest consolidation (use tables, merge related sections)

**Staleness check:**
- Look for decisions without dates - suggest adding them
- Flag any obviously outdated information

**Format check:**
- Ensure decisions have dates, e.g., "Prism.js for tokenization (Dec 2025)"

---

### 3. Report

After making changes, report:

```markdown
# Documentation Maintenance Complete

## SESSION_LOG.md
- Entries reviewed: [X]
- Entries condensed: [Y]
- Decisions migrated to CLAUDE.md: [list or "none"]

## Project CLAUDE.md
- Line count: [N] lines [OK / REVIEW NEEDED if >800]
- Decisions without dates: [list or "none found"]
- Outdated items flagged: [list or "none found"]

## Actions Taken
- [List of actual changes made]
```

---

## Important Notes

- **Always read before editing** - Use Read tool first
- **Preserve architectural decisions** - Never delete design rationale without migrating it
- **Use Edit tool** - Actually make the changes, don't just suggest them
- **Date your decisions** - Format: (Mon YYYY) e.g., (Dec 2025)
