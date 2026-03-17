---
name: acceptance-criteria
description: Generate testable acceptance criteria embedded in PRDs. Use this skill whenever someone mentions acceptance criteria, AC, definition of done, test requirements, or wants to define what "done" looks like for a feature. Also trigger when someone asks to review a PRD and produce testable conditions, or wants to prepare criteria before writing Playwright or other automated tests. This skill bridges the gap between product requirements and verifiable implementation.
---

# Acceptance Criteria Generator

Generate precise, testable acceptance criteria by reading both the PRD (for intent) and the codebase (for reality). AC is embedded directly in the PRD – under each sub-feature heading, using `- [ ]` checkboxes. This keeps requirements and their testable conditions together, making the PRD the single source of truth.

To generate automated tests from the output of this skill, use the **playwright-ac-tests** skill.

## Step 1: Gather context

Before generating any criteria, read both sources.

**From the PRD**, extract:
- The user problem being solved
- Intended user flows and interactions
- Stated requirements (functional and non-functional)
- Edge cases or constraints already mentioned
- Target users and their context
- Priority labels (e.g. `[P0]`, `[P1]`, `[P2]`) – higher priority features warrant more thorough edge case coverage

**From the codebase**, focus on files directly related to the feature. Spend no more than a few minutes exploring – the goal is to ground your AC in real constraints, not to audit the entire repo. Prioritize in this order:

1. **Route definitions** – what pages/URLs exist for this feature
2. **API service files** – what endpoints are called, what response shapes look like (success and error)
3. **Component props and types** – what data shapes flow through the UI
4. **Error boundaries and catch blocks** – how failures are currently handled
5. **Constants and config** – max values, feature flags, default states, enums
6. **Existing test files** – what's already tested (avoid duplicating, fill gaps)

The codebase reveals what the PRD won't tell you: real constraints, existing patterns to stay consistent with, and edge cases the product spec didn't anticipate. Use what you find to make AC specific rather than generic. Instead of "handles long titles gracefully," write "titles exceeding 120 characters are truncated with an ellipsis in the card view" – because you found the truncation logic or the max-length in the code.

## Step 2: Write the acceptance criteria

Each criterion must pass this test: **can someone read it and unambiguously say "yes it works" or "no it doesn't" without asking a follow-up question?**

### Principles

1. **One behavior per criterion.** Split criteria that bundle unrelated behaviors. Use judgment – "The page displays the dataset title, description, and last updated date" is fine because those elements form a single coherent expectation. "The page displays the title and clicking download exports a CSV" is two criteria because those are unrelated behaviors.

2. **State the condition and the observable outcome.** What does the user do or what state exists, and what should they see?
   - Good: "Clicking 'Download CSV' on a dataset with 10k+ rows returns a file within 5 seconds."
   - Bad: "CSV download works."

3. **Quantify where possible.** Replace vague adjectives with measurable values.
   - "Page loads quickly" → "Page reaches interactive state within 2 seconds on a 4G connection"
   - "Accessible" → "Passes axe-core audit with zero critical or serious violations"

4. **Cover the unhappy paths.** For every happy path criterion, ask: what happens when this fails? These are not second-class criteria – they belong alongside the happy paths, not separated into a different section.
   - API returns 500
   - Network timeout
   - Empty data / no results
   - Invalid input
   - Unauthorized access

5. **Specify boundary conditions.** Derived from the codebase – use actual data types and limits you found.
   - Zero items, one item, maximum items
   - Empty strings, max-length strings
   - Special characters in user input
   - First-time user vs returning user state

6. **Include "should NOT" criteria.** Prevent regressions and unintended side effects.
   - "Changing the date filter does not reset the search query"
   - "Navigating away and returning preserves the selected filters"

7. **Note visual/layout expectations where relevant.** Call out when the criterion is about how something looks or responds to viewport changes, since these are verified differently than text/state checks. But keep them with the rest of the criteria – don't separate them.
   - "The chart renders within the content area without horizontal overflow on viewports >= 1280px"
   - "The empty state illustration and message are vertically centered in the content area"

8. **Make each criterion independently verifiable.** If testing criterion 4 requires completing criteria 1–3 first, restructure so each can stand alone or explicitly state the prerequisite as the condition.

9. **Use tables for matrix-style criteria.** When a criterion has multiple conditions across dimensions (e.g. "toggle X is visible when chart type is Y, defaults to Z"), use a table instead of repeating N separate bullets. This is clearer and easier to scan.

   Example – instead of 7 bullets describing each toggle:

   | Toggle | Visible when | Default | Behavior |
   |--------|-------------|---------|----------|
   | Show legend | Always | On | Shows/hides chart legend |
   | Show dots | Line or Area | On | Shows/hides point markers |
   | Gradient fill | Area only | Off | Adds gradient from series color to transparent |

10. **Add decision rationale where it helps.** After a group of AC, use a `> **Decision:**` or `> **Why:**` blockquote to explain non-obvious choices. This helps future readers understand *why* the AC is shaped that way – not just *what* it says.

    ```markdown
    - [ ] Decimal places apply to tooltips and data labels only
    - [ ] Decimal places do not affect Y-axis tick labels

    > **Decision:** Axis labels stay clean and auto-rounded; tooltips and data labels provide precision on demand.
    ```

### Priority-aware depth

When the PRD uses priority labels, scale your AC depth accordingly:

| Priority | Edge case depth | Unhappy paths | Boundary conditions |
|----------|----------------|---------------|---------------------|
| **P0** (must-have) | Thorough – cover all foreseeable edge cases | Required for every API call and user input | Derived from codebase with actual values |
| **P1** (should-have) | Moderate – cover likely edge cases | Required for primary flows | Key boundaries only |
| **P2** (nice-to-have) | Light – happy path + most obvious failure | At least one unhappy path per flow | Optional |

## Step 3: Embed in the PRD

AC is written directly inside the PRD, under each sub-feature heading. Use `- [ ]` checkboxes so criteria are trackable.

### Structure

```markdown
## Sub-feature name

[Context paragraph: what the user wants and why]

**Acceptance Criteria**

[Optional grouping label, e.g. "Layout" or "States"]
- [ ] Criterion one
- [ ] Criterion two
  - [ ] Sub-criterion (indented for closely related conditions)

[Another grouping label]
- [ ] Criterion three

| Column A | Column B | Column C |
|----------|----------|----------|
| Value    | Value    | Value    |

- [ ] Table-level criterion that applies to all rows above

> **Decision:** Rationale for non-obvious choices in this group.
```

### Format notes

- Group criteria by sub-feature area, not by happy/unhappy path. Error handling criteria sit next to the behavior they relate to.
- Use grouping labels (plain text, not headings) when a sub-feature has distinct aspects (e.g. "Layout", "States", "Responsive behavior").
- Use indented `- [ ]` for sub-criteria that are tightly coupled to a parent criterion (e.g. a list of specific rules under a general behavior).
- Each criterion should make sense to a developer who hasn't read the rest of the PRD.

## Step 4: Self-review checklist

Before presenting AC to the user, verify against these checklists.

### Always check

- [ ] Every requirement from the PRD has at least one corresponding criterion
- [ ] No criterion bundles unrelated behaviors
- [ ] Each criterion can be read by a developer who hasn't seen the PRD and still be understood
- [ ] "Should NOT" criteria exist for likely regression points (state preservation, side effects)
- [ ] Matrix-style criteria use tables instead of repetitive bullet lists
- [ ] Decision rationale is provided for non-obvious AC choices

### Production readiness

- [ ] Unhappy paths exist for every API call or user input
- [ ] Boundary conditions reference actual values from the code (field lengths, data types, enums) rather than generic placeholders
- [ ] Visual/layout criteria exist for any UI that could break across viewports
- [ ] Accessibility criteria exist for interactive elements (labels, keyboard nav, focus management)
