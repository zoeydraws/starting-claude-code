---
name: playwright-ac-tests
description: Generate and run Playwright tests from acceptance criteria. Use this skill when someone wants to write automated tests for a feature, run Playwright tests against localhost, generate screenshot baseline tests, create text/state assertion tests, or turn acceptance criteria into executable test files. Also trigger when someone mentions e2e tests, visual regression tests, browser tests, or wants to verify a feature works before shipping. If no acceptance criteria exist yet, generate them first using the acceptance-criteria skill.
---

# Playwright AC Test Generator

Generate and run Playwright tests from acceptance criteria against a local dev server. Produces two types of tests: **state/interaction tests** (text, visibility, behavior assertions) and **screenshot tests** (visual comparison against baselines).

If no acceptance criteria exist in the PRD for the feature, generate them first using the **acceptance-criteria** skill, or fall back to reading the page directly: navigate to the relevant URL, inventory what's on screen, and generate tests from what you observe combined with the codebase.

## Step 0: Assess the project

Before writing any tests, check the project setup.

### Detect framework

Look for clues in the codebase:
- `next.config.*` → Next.js
- `vite.config.*` → Vite
- `package.json` → check `dependencies` for `next`, `react-scripts`, `vite`, `nuxt`, etc.
- Check the `scripts` section for the dev server command (`next dev`, `vite`, `npm start`, etc.)

Note the dev server command and the port it runs on. You'll need this for the Playwright config `webServer` block.

### Check for existing Playwright setup

Look for:
- `playwright.config.ts` or `playwright.config.js` in the project root
- A `tests/` or `e2e/` directory with `.spec.ts` files
- `@playwright/test` in `package.json` devDependencies

**If Playwright exists:** Read the existing config. Note the base URL, existing projects/viewports, screenshot paths, and any custom fixtures. Adapt to the existing setup — don't override it.

**If Playwright does not exist:** Set it up:

```bash
npm init playwright@latest -- --yes --install-deps
```

Then create or update `playwright.config.ts` with the configuration from the section below.

### Determine test data

Before writing tests, figure out what URLs and data to use:

1. Read route definitions to find valid page paths
2. Check for seed data, fixtures, or known staging dataset IDs
3. Look at existing test files for patterns — they often reference known-good IDs
4. If the app depends on API data, decide: use real dev/staging API (simpler, less stable) or mock with `page.route()` (stable, more setup). For a first pass, real API is fine. Mock later if tests become flaky.

Document the test data decisions at the top of each test file:

```typescript
// Test data: uses staging dataset "population-by-age-2024" (ID: abc-123)
// API: hits real dev server at localhost:3000
```

## Step 1: Configure Playwright

Whether you're creating a new config or updating an existing one, ensure these elements are present.

### Viewports

Test across three breakpoints:

```typescript
projects: [
  {
    name: 'desktop',
    use: { viewport: { width: 1280, height: 720 } },
  },
  {
    name: 'tablet',
    use: { viewport: { width: 768, height: 1024 } },
  },
  {
    name: 'mobile',
    use: { viewport: { width: 390, height: 844 } },
  },
],
```

### Screenshot config

```typescript
expect: {
  toHaveScreenshot: {
    maxDiffPixelRatio: 0.01,
    animations: 'disabled',
  },
},
```

### Retry config

Flaky tests are inevitable with e2e. Set retries to reduce noise:

```typescript
retries: process.env.CI ? 2 : 0,
```

Zero retries locally (so you see real failures immediately), two in CI (so transient issues don't block the pipeline).

### Web server

Point to the local dev server. Adapt the command and port to what you found in Step 0:

```typescript
webServer: {
  command: 'npm run dev',  // adjust based on framework
  port: 3000,              // adjust based on project
  reuseExistingServer: true,
  timeout: 30000,
},
```

`reuseExistingServer: true` is important — if the dev server is already running, Playwright won't try to start a second one.

### Screenshot directory

```typescript
snapshotPathTemplate: 'tests/__screenshots__/{projectName}/{testFilePath}/{arg}{ext}',
```

This organizes screenshots by viewport:
```
tests/__screenshots__/
  desktop/
    dataset-search.visual.spec.ts/
      search-results-layout.png
  tablet/
    ...
  mobile/
    ...
```

## Step 2: Classify acceptance criteria

Read the AC section of the PRD for the feature being tested. Classify each criterion into a test type. For table-format AC (matrix criteria like display toggles), generate one test per row or one parameterized test covering all rows.

**State/interaction tests** (`.spec.ts`):
- Criteria about text content, element visibility, element state
- Criteria about behavior after user actions (click, type, navigate)
- Error handling criteria (use `page.route()` for mocking)

**Screenshot tests** (`.visual.spec.ts`):
- Criteria about layout, spacing, visual appearance
- Criteria that mention viewports or responsive behavior
- Criteria where "does it look right" is the core question

**Accessibility tests** (`.a11y.spec.ts`):
- Criteria about screen reader labels, keyboard navigation, focus management
- General "no a11y violations" sweep

If a criterion is ambiguous, default to a state/interaction test — they're faster and more stable.

## Step 3: Write state/interaction tests

These assert on text content, element presence, behavior after user actions, and error handling.

### File structure

One test file per feature area:
```
tests/
  dataset-search.spec.ts        ← state, interaction, error tests
  dataset-search.visual.spec.ts ← screenshot tests
  dataset-search.a11y.spec.ts   ← accessibility tests (if enough to warrant a file)
```

### Locator strategy (in priority order)

Prefer accessible locators that reflect what the user sees:

1. `page.getByRole()` — buttons, headings, links, inputs by their accessible role
2. `page.getByText()` — visible text content
3. `page.getByLabel()` — form fields by their label
4. `page.getByPlaceholder()` — inputs by placeholder
5. `page.getByTestId()` — use `data-testid` attributes as a last resort

Avoid CSS selectors and XPath unless no semantic alternative exists. Accessible locators make tests resilient to refactors and also validate that the a11y markup is correct.

### Patterns

**Basic state assertion:**
```typescript
test('dataset page shows title and last updated date', async ({ page }) => {
  await page.goto('/datasets/abc-123');
  await expect(page.getByRole('heading', { level: 1 })).toContainText('Population by Age');
  await expect(page.getByText(/last updated/i)).toBeVisible();
});
```

**Interaction assertion:**
```typescript
test('typing a query and pressing Enter shows results', async ({ page }) => {
  await page.goto('/search');
  await page.getByRole('searchbox').fill('population');
  await page.keyboard.press('Enter');
  await expect(page.getByRole('list')).toBeVisible();
  const count = await page.getByRole('listitem').count();
  expect(count).toBeGreaterThan(0);
});
```

**Error state with mocked API:**
```typescript
test('shows error banner when API returns 500', async ({ page }) => {
  await page.route('**/api/datasets/**', route =>
    route.fulfill({ status: 500, body: 'Internal Server Error' })
  );
  await page.goto('/datasets/abc-123');
  await expect(page.getByRole('alert')).toBeVisible();
  await expect(page.getByText(/something went wrong/i)).toBeVisible();
});
```

**"Should NOT" regression test:**
```typescript
test('changing date filter does not reset search query', async ({ page }) => {
  await page.goto('/search');
  await page.getByRole('searchbox').fill('population');
  await page.keyboard.press('Enter');
  await page.getByLabel('Date range').selectOption('2024');
  await expect(page.getByRole('searchbox')).toHaveValue('population');
});
```

## Step 4: Write screenshot tests

These capture the visual appearance and compare against baselines.

### Waiting for stability

Do not use `page.waitForLoadState('networkidle')` — it's unreliable with analytics, long-polling, or websockets. Instead, wait for a specific element that signals the page is ready:

```typescript
test('search results page layout', async ({ page }) => {
  await page.goto('/search?q=population');
  // wait for the actual content, not a generic network condition
  await page.getByRole('list').waitFor({ state: 'visible' });
  await expect(page).toHaveScreenshot('search-results.png');
});
```

Pick a meaningful readiness signal: the main content container, a heading, the last-loaded section, or a data element that only appears after the API responds.

### Mask dynamic content

Anything that changes between runs will cause false failures:

```typescript
await expect(page).toHaveScreenshot('search-results.png', {
  mask: [
    page.locator('[data-testid="timestamp"]'),
    page.locator('[data-testid="live-count"]'),
  ],
});
```

Common things to mask: timestamps, relative dates ("3 hours ago"), live counters, user-specific data, randomized content.

### Name screenshots descriptively

```typescript
// good — describes what you're verifying
await expect(page).toHaveScreenshot('dataset-card-grid-layout.png');

// bad — meaningless
await expect(page).toHaveScreenshot('screenshot-1.png');
```

### Full page vs element screenshots

Use full page for layout tests, element-level for component-specific visuals:

```typescript
// full page layout
await expect(page).toHaveScreenshot('search-page-full.png', { fullPage: true });

// specific component
const chart = page.getByTestId('chart-container');
await expect(chart).toHaveScreenshot('chart-rendered.png');
```

### Responsive behavior

Each screenshot test automatically runs at all three viewport projects (desktop, tablet, mobile), producing three separate baselines. You don't need to resize within a test — the project config handles it.

## Step 5: Accessibility tests

Install axe if not present:

```bash
npm install -D @axe-core/playwright
```

Pattern:
```typescript
import AxeBuilder from '@axe-core/playwright';

test('dataset page has no critical a11y violations', async ({ page }) => {
  await page.goto('/datasets/abc-123');
  await page.getByRole('heading', { level: 1 }).waitFor({ state: 'visible' });
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa'])
    .analyze();
  expect(results.violations.filter(v =>
    v.impact === 'critical' || v.impact === 'serious'
  )).toHaveLength(0);
});
```

## Step 6: Running the tests

### First run — generate baselines

The first time screenshot tests run, there are no baselines to compare against, so they will fail. Generate baselines with:

```bash
npx playwright test --update-snapshots
```

Review the generated screenshots in `tests/__screenshots__/` manually. If they look correct, commit them — they are now your baselines.

### Subsequent runs

```bash
# run all tests
npx playwright test

# run only state/interaction tests (skip screenshots for speed)
npx playwright test --ignore 'tests/**/*.visual.spec.ts'

# run only screenshot tests
npx playwright test tests/**/*.visual.spec.ts

# run tests for a specific feature
npx playwright test dataset-search

# run with UI mode for debugging
npx playwright test --ui
```

### When screenshot tests fail

Playwright generates three files for each failure:
- `*-expected.png` — the baseline
- `*-actual.png` — what was captured this run
- `*-diff.png` — highlights the differences

Review the diff. If the change is intentional (you updated the UI), update the baseline:
```bash
npx playwright test --update-snapshots
```

If it's unintentional, you've caught a visual regression — fix the code.

### Diagnosing flaky tests

If a test passes sometimes and fails sometimes:

1. **Screenshot flakes:** Usually caused by animations, font loading, or dynamic content that wasn't masked. Check the diff — if the difference is subtle (anti-aliasing, subpixel rendering), increase `maxDiffPixelRatio` slightly. If the difference is content, add a mask.
2. **Timing flakes:** A locator resolves before the content is ready. Replace generic waits with explicit waits for the element that signals readiness.
3. **Data flakes:** The test depends on API data that changes. Move to mocked responses with `page.route()`.

## Test organization summary

```
tests/
  __screenshots__/            ← screenshot baselines (committed to git)
    desktop/
    tablet/
    mobile/
  [feature].spec.ts           ← state, interaction, error tests
  [feature].visual.spec.ts    ← screenshot comparison tests
  [feature].a11y.spec.ts      ← accessibility tests (if enough to warrant)
playwright.config.ts
```

## Mapping AC to test code — quick reference

| Criterion is about...           | Test file            | Key Playwright APIs                                     |
|---------------------------------|----------------------|---------------------------------------------------------|
| Text, visibility, element state | `.spec.ts`           | `expect(locator).toBeVisible()`, `.toContainText()`     |
| Behavior after user action      | `.spec.ts`           | `locator.click()`, `.fill()`, `.press()`, then assert   |
| Error handling                  | `.spec.ts`           | `page.route()` to mock, then assert error UI            |
| Layout, visual appearance       | `.visual.spec.ts`    | `expect(page).toHaveScreenshot()`                       |
| Accessibility                   | `.a11y.spec.ts`      | `AxeBuilder` audit, assert zero critical violations     |

## Notes for Claude Code usage

When generating tests from AC using this skill:

1. Read the AC section in the PRD first. If none exists, either generate one with the **acceptance-criteria** skill or fall back to inspecting the running page and codebase directly.
2. Classify each criterion into a test type using the table above.
3. Determine test data: read routes, check for seed data or fixtures, look at existing test files for known-good IDs.
4. Check if relevant test files already exist — extend them rather than overwriting.
5. Verify the dev server is accessible before writing tests (try fetching the base URL).
6. Generate test files following the patterns above.
7. Run the tests once and report results.
8. For screenshot tests on first run, generate baselines and ask the user to review them before committing.
9. If tests fail, diagnose clearly: is it a test issue (wrong locator, timing, missing mock) or a real bug in the feature? Report which it is.
