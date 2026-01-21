# Skills

> **Note:** I'm still new to Skills myself. This page documents my current understanding — I'll refine it into a proper guide once I have a working workflow sorted out.

---

## Shortcuts vs Skills

There are two ways to automate Claude's behavior:

|                        | Shortcuts                          | Skills                                      |
| ---------------------- | ---------------------------------- | ------------------------------------------- |
| **What it is**         | Plain English rule                 | SKILL.md file with structured instructions  |
| **Where it lives**     | CLAUDE.md                          | `.claude/skills/` folder                    |
| **How it's triggered** | Keywords in conversation           | `/name` (explicit) OR auto by context       |
| **When to use**        | Simple "when X, do Y" rules        | Multi-step workflows, checklists, templates |

**Examples:**

- **Shortcut:** In CLAUDE.md you write `"commit" shortcut: When user says "commit", run git add, commit, and push` → Claude follows this when you say "commit"
- **Skill (user-invoked):** You type `/commit` → Claude loads the commit skill
- **Skill (auto-triggered):** You say "review this component" → Claude automatically applies your code-review skill

**Rule of thumb:** If it fits in one sentence, use a shortcut. If it needs a checklist or template, make it a skill.

### Why This Matters: Saving Tokens

Your CLAUDE.md file is loaded into Claude's memory for **every conversation**. If it's full of situational instructions (like "when writing a research report, use this format..."), Claude reads all of that even when you're just asking it to commit code.

**Skills let you move situational instructions out of CLAUDE.md.**

- CLAUDE.md → Things Claude **always** needs to know
- Skills → Things Claude only needs **sometimes**

**Example:** You have detailed instructions for creating UX research reports. Instead of keeping this in CLAUDE.md (loaded every time), move it to a `ux-research-report` skill. Claude only loads those instructions when you're actually working on a report.

This keeps your context lean and saves tokens for what actually matters in each conversation.

### How to Decide: 4 Questions

When choosing between a shortcut and a skill, ask:

1. **Token efficiency** — Is this needed every session? If not, why pay the context cost? Move it to a skill.

2. **Complexity** — Does it have multiple steps? Multi-step workflows (git add → commit → push, fetch → merge → handle conflicts) benefit from detailed, dedicated skill files.

3. **Discoverability** — Should others find this easily? Skills appear via `/help`. Shortcuts are hidden in CLAUDE.md.

4. **Maintainability** — Will this evolve? Easier to update one skill file than hunt through CLAUDE.md.

**If you answer "yes" to 2+ questions → make it a skill.**

---

## What Is a Skill?

A Skill is a folder containing a `SKILL.md` file with instructions. The file has two parts:

1. **Frontmatter** — Name and description (tells Claude when to use it)
2. **Instructions** — What Claude should do

### Example: A Simple Code Review Skill

```
.claude/skills/code-review/
└── SKILL.md
```

Contents of `SKILL.md`:

```markdown
---
name: code-review
description: Reviews code for best practices and potential issues. Use when reviewing code, checking PRs, or analyzing code quality.
---

When reviewing code, check for:

1. Code organization and structure
2. Error handling
3. Security concerns
4. Test coverage
```

When you ask Claude to review code, it reads the description, recognizes this skill is relevant, and follows the instructions automatically.

---

## Types of Skills (By Location)

| Type         | Where It Lives                             | Who Can Use It                 |
| ------------ | ------------------------------------------ | ------------------------------ |
| **Personal** | `~/.claude/skills/`                        | Just you, across all projects  |
| **Project**  | `.claude/skills/` (in your project folder) | Anyone working on this project |
| **Plugin**   | Installed via `/plugin install`            | Anyone who installs the plugin |
| **Managed**  | Set by organization admins                 | Everyone in your organization  |

Start with personal skills while learning. Move to project skills when you have patterns worth sharing with collaborators.

---

## How to Use Skills

### Check If You Have Any Skills Installed

In Claude Code, run:

```
ls ~/.claude/skills/
ls .claude/skills/
```

If these folders don't exist or are empty, you have no skills installed yet.

### Installing Skills from Plugins

Anthropic provides official skills you can install:

```
/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills
```

This gives you skills for creating documents (Word, PDF, PowerPoint, Excel) and other utilities.

### Creating Your Own Skill

1. Create the folder structure:

   ```
   mkdir -p ~/.claude/skills/my-skill-name
   ```

2. Create the SKILL.md file with frontmatter and instructions

3. Claude will automatically detect and use it when relevant

Or just ask Claude:

```
Create a personal skill called "ux-research-report" that helps me
write user research reports. It should include sections for
methodology, key findings, and recommendations.
```

Claude will create the folder and file for you.

---

## Multi-File Skills (Advanced)

For complex skills, you can include supporting files. Claude reads the main SKILL.md first, then loads other files only when needed:

```
.claude/skills/code-review/
├── SKILL.md          # Main instructions
├── SECURITY.md       # Security checklist (loaded when reviewing security)
├── PERFORMANCE.md    # Performance patterns (loaded when relevant)
└── STYLE.md          # Style guide reference
```

This keeps Claude's context focused — it doesn't load everything upfront, just what's needed for the current task.

---

## What Skills Should I Add?

**Only the ones you actually need.**

It's tempting to install a bunch of skills "just in case" — but every skill adds to what Claude has to scan through to decide what's relevant. More isn't better.

### Good Reasons to Add a Skill

- You do this task **repeatedly** (weekly or more)
- The task has a **specific format** you want followed every time
- You're currently keeping detailed instructions in CLAUDE.md that are **only sometimes relevant**

### Bad Reasons to Add a Skill

- "This looks cool"
- "I might need this someday"
- "Everyone recommends it"

### A Practical Approach

1. **Start with zero skills** — See what you actually need
2. **Notice friction** — What do you keep re-explaining to Claude?
3. **Add one skill** — For your most repeated workflow
4. **Evaluate** — Did it actually help? Keep or remove.
5. **Repeat** — Add skills one at a time, based on real need

### Build vs Download

| Situation | Better Choice |
|-----------|---------------|
| Generic capability (create Word docs) | Download official skill |
| Your team's specific format/process | Build your own |
| Trying something new | Download, then customize |

The official Anthropic skills are good for **generic outputs** (documents, spreadsheets). For **your specific workflows** (your research report format, your PRD template), custom skills will serve you better.

---

## Skill Collections

These are good starting points. Don't treat them as final — customize and build upon them for your specific needs.

### Official Anthropic Skills

**Repository:** [github.com/anthropics/skills](https://github.com/anthropics/skills)

| Skill              | What It Does                    |
| ------------------ | ------------------------------- |
| `docx`             | Create/edit Word documents      |
| `pdf`              | Handle PDF documents            |
| `pptx`             | Create PowerPoint presentations |
| `xlsx`             | Create Excel spreadsheets       |
| `frontend-design`  | Frontend design patterns        |
| `brand-guidelines` | Brand identity resources        |
| `doc-coauthoring`  | Collaborative document writing  |

Install with:

```
/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills
```

### Community Collections

| Resource                                                                                                 | What's Included                                       |
| -------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| [BMAD Method Skills](https://aj-geddes.github.io/claude-code-bmad-skills/skills/)                        | Multiple PM and design skills                         |
| [Skills Library (26+ packages)](https://gist.github.com/alirezarezvani/a0f6e0a984d4a4adc4842bbe124c5935) | Tresor (ready-to-use), Skill Factory, domain packages |
| [Skills Directory](https://www.skillsdirectory.com/)                                                     | Searchable directory of community skills              |
| [Claude Plugins Directory](https://claude-plugins.dev/)                                                  | Skills and plugins browser                            |

---

## Skills for Product & UX Work

These are particularly relevant if you're doing product management, UX research, or design work:

### PRD (Product Requirements Document) Skills

| Skill                    | Source                                                                                       | What It Does                                                                                                            |
| ------------------------ | -------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **prd-generator**        | [claude-plugins.dev](https://claude-plugins.dev/skills/@jamesrochabrun/skills/prd-generator) | Generate comprehensive PRDs following best practices                                                                    |
| **Product Requirements** | [MCP Market](https://mcpmarket.com/tools/skills/product-requirements)                        | Interactive PRD creation with quality scoring (aims for 90+ score across business value, UX, and technical constraints) |

---

## When to Use Shortcuts vs Skills

| Use Case                                | Better Option |
| --------------------------------------- | ------------- |
| Simple "when I say X, do Y" rule        | Shortcut      |
| Multi-step workflow                     | Skill         |
| Detailed checklist or template          | Skill         |
| Pattern Claude should auto-apply        | Skill         |
| Shared team standards                   | Skill         |

---

## Next Steps

1. Check what skills you have: `ls ~/.claude/skills/`
2. Try installing official skills: `/plugin install example-skills@anthropic-agent-skills`
3. Identify a workflow that would benefit from a skill
4. Ask Claude to create it for you
5. Customize based on how it works in practice
