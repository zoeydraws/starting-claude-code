---
description: Create and review product requirement documents (PRDs) through a 4-phase pipeline
---

# PRD

**When to use:** When creating a new PRD from research, fleshing out features, formatting for Notion, or auditing an existing PRD.

**Invocation:**

| Command | Phase | What it does |
|---------|-------|-------------|
| `/prd scaffold` | 1 | Generate feature sections from research docs |
| `/prd build` | 2 | Flesh out features with acceptance criteria |
| `/prd format` | 3 | Reorganize into final Notion-ready format |
| `/prd review` | 4 | Audit completeness + research traceability |
| `/prd` | — | Show which phase to start with |

---

## Phase 1: Scaffold

**Input:** Research synthesis docs (interview findings, UT findings, competitive research)

**What to do:**

1. Read all research docs in the project
2. Group related findings into features (don't 1:1 map quotes to features)
3. Output feature sections as scaffolding – enough structure to start adding detail into:

```markdown
# Feature: [Name]

**Research signal:** [1-2 sentences, agency attribution, participant count]

**Design decision:** [Brief rationale for the chosen approach – what and why]

## What it does
- [Bullet point, concise]
- [Bullet point, concise]

## Acceptance criteria
_(empty – filled in Phase 2)_

**Future:**
_(empty – filled in Phase 2)_
```

4. Flag out-of-scope items in a separate section at the bottom
5. Each feature gets its own section with research signal + design decision filled in
6. "What it does" should have 2-4 bullets max – just enough to define scope
7. Ask user to confirm/edit the feature list before proceeding

---

## Phase 2: Build

**Input:** Scaffolded feature sections from Phase 1 + user's design decisions during prototyping

**What to do:** Flesh out each feature section – expand bullets, write acceptance criteria, add future items.

**Rules:**

- Each bullet should be understandable without reading the rest of the PRD
- Acceptance criteria must be testable (not vague like "works well")
- Design decisions documented inline with rationale, not in a separate table
- Simple language, no jargon – reader is a PM or designer, not an engineer
- No implementation details (no schema, no code paths, no class names)

---

## Phase 3: Format

**Input:** Built PRD (may be messy from iterative editing)

**What to do:** Clean up into final Notion-ready format.

**Rules:**

- **Heading promotion:** `##` -> `#`, `###` -> `##`, `####` -> `###` (keep first `#` title as-is). Notion treats `#` as page-level heading.
- **Architecture section** at top for cross-cutting concerns (shared logic, data cleaning, type detection, display name mapping)
- **Section order:** Architecture -> Features (by importance) -> Research Theme Coverage -> Out of Scope
- **Tables** over paragraphs when comparing things
- **Bullet points** over paragraphs when listing things
- **No redundancy** – if a decision is explained in a feature section, don't repeat elsewhere
- **Remove metadata line** (Product/Date/Status) – Notion page has its own properties
- **Bold** for field/control names in bullet points
- **`·` separator** for listing sub-features within table cells

---

## Phase 4: Review

**Input:** Completed PRD + research docs (if available)

**What to do:** Audit and fix.

**Checks:**

1. **Acceptance criteria coverage** – every feature has testable criteria
2. **Research traceability** – if research docs exist, generate Research Theme Coverage table:

```markdown
| Theme | Agencies | Priority | PRD Feature |
|-------|:---------|:---------|:------------|
| [Theme] | [X/N] | [P0/Out of scope] | **[Feature]:** sub-feature · sub-feature |
```

3. **Completeness** – no features mentioned in research but missing from PRD
4. **Consistency** – no contradictions between feature sections
5. **Future items** – all deferred items nested under parent features (not floating)
6. **Out of scope** – items listed with brief rationale

---

## No-arg invocation (`/prd`)

When invoked without arguments, check the project state and recommend a phase:

- **No PRD exists** -> suggest Phase 1 (scaffold)
- **Feature list exists but no full sections** -> suggest Phase 2 (build)
- **Full PRD exists but messy/not formatted** -> suggest Phase 3 (format)
- **Clean PRD exists** -> suggest Phase 4 (review)
