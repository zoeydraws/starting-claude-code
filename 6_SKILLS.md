# Skills

> **Note:** I'm still new to Skills myself. This page documents my current understanding — I'll refine it into a proper guide once I have a working workflow sorted out.

---

## Slash Commands vs Skills

In the previous guide, we covered [slash commands](5_SLASH_COMMANDS.md) — shortcuts you type like `/commit` that trigger pre-written prompts.

**Skills are the next level up.**

|                           | Slash Commands                 | Skills                                                  |
| ------------------------- | ------------------------------ | ------------------------------------------------------- |
| **How they're triggered** | You type `/command` explicitly | Claude triggers them **automatically** based on context |
| **Where they live**       | Instructions in CLAUDE.md      | SKILL.md files in a `skills/` folder                    |
| **When to use**           | Repetitive tasks you initiate  | Patterns Claude should always follow                    |

**Example:**

- Slash command: You type `/commit` → Claude commits your code
- Skill: You say "review this component" → Claude automatically applies your code-review skill's checklist without you asking

Think of slash commands as buttons you press. Skills are more like teaching Claude habits — once installed, Claude uses them whenever relevant.

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

## When to Use Skills vs Slash Commands

| Use Case                             | Better Option         |
| ------------------------------------ | --------------------- |
| One-off task you trigger manually    | Slash command         |
| Pattern Claude should always follow  | Skill                 |
| Quick shortcut (commit, push, etc.)  | Slash command         |
| Complex workflow with multiple steps | Skill                 |
| Shared team standards                | Skill (project-level) |
| Personal preference                  | Either works          |

You can use both together. For example:

- **Skill:** Teaches Claude your code review standards
- **Slash command:** `/review` triggers a review using those standards

---

## Next Steps

1. Check what skills you have: `ls ~/.claude/skills/`
2. Try installing official skills: `/plugin install example-skills@anthropic-agent-skills`
3. Identify a workflow that would benefit from a skill
4. Ask Claude to create it for you
5. Customize based on how it works in practice
