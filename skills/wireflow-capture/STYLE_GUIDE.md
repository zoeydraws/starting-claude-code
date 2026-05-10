# Wireflow Visual Style

A starter house style for HTML wireflows so a set reads consistently in Figma. The canonical CSS lives in this doc – paste the **Foundation**, **Tokens**, **Type utilities**, and **Base classes** blocks into a new wireflow's `<style>` and you have the full system. Treat tokens as a starting point – swap colours, type, and radii for your own brand.

## How tokens flow into Figma

The html-to-design converter reads computed styles, so `var(--token)` resolves to its hex before capture – tokens never reach Figma as variables, only as their resolved values. Renaming a token, changing its value, or swapping a class definition all produce identical capture output to writing the hex inline.

## Foundation

```css
* { box-sizing: border-box; }
body { margin: 0; padding: 0; }
#page {
  min-width: 2300px;          /* baseline width – widen per feature */
  width: max-content;         /* grows to widest row, never clips */
  padding: var(--s-page);
  background: var(--c-surface-page);
  color: var(--c-text-primary);
  font-family: var(--font-sans);
  font-size: 14px;
  display: flex;
  flex-direction: column;
}
```

**Page wrapper rule.** Never put flex on `<body>` – the converter mishandles its bounding box and top children render above the captured frame. Wrap content in `<div id="page">` (see `SKILL.md` → Authoring rules).

## Tokens

Paste this `:root` block verbatim into every wireflow.

```css
:root {
  /* Type */
  --font-sans: -apple-system, "Segoe UI", Roboto, sans-serif;
  --font-mono: ui-monospace, SFMono-Regular, Menlo, monospace;

  /* Text */
  --c-text-primary:     #1e1e1e;   /* primary text, dark pills, top bars, logos */
  --c-text-strong:      #2e2e2e;   /* slightly softer body */
  --c-text-body:        #474747;   /* muted body */
  --c-text-muted:       #686868;   /* captions, eyebrows, meta, placeholder labels */
  --c-text-placeholder: #a0a0a0;   /* placeholder text */
  --c-text-disabled:    #b0b0b0;   /* disabled / unchecked checkbox border */
  --c-text-arrow:       #9c9c9c;   /* arrow glyphs */
  --c-text-inverse:     #ffffff;   /* white text on dark backgrounds (pills, topbars) */

  /* Borders */
  --c-border-input:        #d0d0d0;
  --c-border-frame:        #e3e3e7;   /* workhorse: frames, cards, sections, form-section underline */
  --c-border-subdivider:   #ececec;   /* sub-divider inside cards */
  --c-border-table-cell:   #f0f0f3;
  --c-border-table-head:   #e8e8ea;

  /* Surfaces */
  --c-surface-page:  #ffffff;
  --c-surface-grey:  #f5f5f7;        /* scenario-block bg, table headers, code chip bg, sidebar */
  --c-surface-focus: #fafafa;        /* focus row in dashboard table */

  /* Status */
  --c-success:        #1e7d3a;        /* success, healthy, "chosen" outline */
  --c-danger:         #b42318;        /* warning, overdue, required asterisk, inline code */
  --c-warning:        #b8860b;        /* yellow status pill text */
  --c-toast-title:    #06502a;
  --c-toast-border:   #abefc6;
  --c-toast-bg:       #ecfdf3;

  /* Highlights */
  --c-sticky-bg:        #fef7c0;
  --c-sticky-text:      #2e2400;
  --c-formula-bg:       #fff7d6;
  --c-formula-border:   #f4d56b;
  --c-approaching-bg:   #fff4d6;
  --c-approaching-text: #8a6a00;
  --c-overdue-bg:       #fde2e2;
  --c-overdue-text:     #b42318;
  --c-overdue-border:   #f5b8b8;     /* overdue notification badge border */
  --c-code-chip-bg:     #fdf2f2;     /* inline code chip on grey scenario-sub */

  /* Reminder cycle badges (recurring notifications) */
  --c-reminder-bg:           #fef3c7;
  --c-reminder-border:       #fcd34d;
  --c-reminder-text:         #92400e;   /* main badge text */
  --c-reminder-text-soft:    #a16207;   /* parenthetical "(2d before)" */
  --c-reminder-text-meta:    #a87000;   /* "(MAX)" / hardcoded notes */
  --c-reminder-text-overdue: #9b3a13;   /* parenthetical "(1d overdue)" */

  /* Inline field error */
  --c-error-bg: #fff5f5;
  --c-error:    #d33;                   /* used for both border and text */

  /* Timeline markers */
  --c-marker-healthy:     #d0d0d0;
  --c-marker-approaching: #f4c542;
  --c-marker-overdue:     #e84747;
  --c-marker-update:      #1e1e1e;

  /* Spacing */
  --s-page:          64px;          /* page padding */
  --s-section:       96px;          /* margin between sections */
  --s-scenario-pad:  32px;          /* scenario-block padding */
  --s-scenario-gap:  28px;          /* margin between scenario blocks */
  --s-frame:         18px;          /* default frame padding */
  --s-frame-form:    24px;          /* form frame padding */
  --s-frame-compact: 16px;          /* compact frame padding */
  --s-field:         14px;          /* field margin-bottom */
  --s-row-gap:       16px;
  --s-pill-gap:      4px;

  /* Radii */
  --r-frame:    12px;
  --r-section:  16px;
  --r-input:    6px;
  --r-button:   8px;
  --r-pill:     18px;
  --r-day-pill: 15px;               /* 30×30 round day pill */
  --r-badge:    12px;
  --r-toast:    8px;
  --r-logo:     4px;

  /* Shadows */
  --sh-card:   0 1px 3px rgba(0,0,0,0.04);
  --sh-sticky: 0 1px 2px rgba(0,0,0,0.04);
  --sh-toast:  0 4px 12px rgba(0,0,0,0.06);
  --sh-dialog: 0 8px 24px rgba(0,0,0,0.10);
}
```

## Type utilities

Paste verbatim. Apply via `class="t-h1"`, `class="t-section-title"`, etc.

```css
.t-h1            { font-weight: 700; font-size: 36px; letter-spacing: -0.01em; color: var(--c-text-primary); margin: 0 0 12px; }
.t-subtitle      { font-weight: 400; font-size: 14px; line-height: 1.5; color: var(--c-text-muted); margin: 0 0 56px; }
.t-section-title { font-weight: 700; font-size: 22px; letter-spacing: -0.01em; color: var(--c-text-primary); margin: 0 0 6px; }
.t-section-desc  { font-weight: 400; font-size: 13px; line-height: 1.55; color: var(--c-text-muted); }
.t-scenario-head { font-weight: 700; font-size: 18px; letter-spacing: -0.01em; color: var(--c-text-primary); margin: 0 0 6px; }
.t-scenario-sub  { font-weight: 400; font-size: 13px; line-height: 1.55; color: var(--c-text-muted); }
.t-intro-title   { font-weight: 700; font-size: 16px; color: var(--c-text-primary); }
.t-form-section  { font-weight: 700; font-size: 11px; letter-spacing: 1px; text-transform: uppercase; color: var(--c-text-muted); border-bottom: 1px solid var(--c-border-frame); margin: 20px 0 12px; padding-bottom: 6px; }
.t-form-section:first-child { margin-top: 0; }
.t-label         { font-weight: 500; font-size: 13px; color: var(--c-text-primary); margin-bottom: 6px; }
.t-input         { font-weight: 400; font-size: 13px; color: var(--c-text-primary); }
.t-body          { font-weight: 400; font-size: 13px; line-height: 1.55; color: var(--c-text-primary); }
.t-eyebrow       { font-weight: 700; font-size: 11px; letter-spacing: 0.8px; text-transform: uppercase; color: var(--c-text-muted); }
.t-thead         { font-weight: 600; font-size: 11px; letter-spacing: 0.6px; text-transform: uppercase; color: var(--c-text-muted); }
.t-tcell         { font-weight: 400; font-size: 12px; line-height: 1.4; color: var(--c-text-primary); }
.t-step-label    { font-weight: 600; font-size: 10px; color: var(--c-text-strong); }
.t-step-date     { font-weight: 400; font-size: 9px; color: var(--c-text-muted); }
.t-code          { font-family: var(--font-mono); font-weight: 400; font-size: 12px; color: var(--c-danger); }
.t-sticky        { font-weight: 400; font-size: 13px; line-height: 1.55; color: var(--c-sticky-text); }
```

## Base classes

Paste verbatim. Each class is the canonical implementation; component recipes (next section) describe when to combine them.

```css
/* Layout primitives */
.row   { display: flex; gap: var(--s-row-gap); align-items: flex-start; margin-bottom: 40px; flex-wrap: nowrap; }
.col   { display: flex; flex-direction: column; }
.arrow { display: flex; align-items: flex-start; justify-content: center; font-size: 22px; color: var(--c-text-arrow); padding-top: 90px; width: 28px; flex-shrink: 0; }

/* Containers */
.frame {
  background: var(--c-surface-page);
  border: 1px solid var(--c-border-frame);
  border-radius: var(--r-frame);
  padding: var(--s-frame);
  box-shadow: var(--sh-card);
}
.frame-form    { padding: var(--s-frame-form); width: 400px; }
.frame-tight   { padding: var(--s-frame-compact); width: 260px; }
.frame-dash    { padding: var(--s-frame-compact); width: 360px; }

.section-grey {
  background: var(--c-surface-grey);
  border: 1px solid var(--c-border-frame);
  border-radius: var(--r-section);
  padding: var(--s-scenario-pad);
}

.ref-card {
  background: var(--c-surface-page);
  border: 1px solid var(--c-border-frame);
  border-radius: var(--r-frame);
  padding: 24px 28px 40px;             /* +16px buffer – see SKILL.md text-content card pattern */
  max-width: 880px;
  box-shadow: var(--sh-card);
}

.scenario-intro {
  background: var(--c-surface-page);
  border: 1px solid var(--c-border-frame);
  border-radius: var(--r-frame);
  padding: 20px 24px 36px;             /* +16px buffer */
  max-width: 600px;
  box-shadow: var(--sh-card);
}

/* Sticky note */
.sticky {
  display: block;
  max-width: 320px;
  padding: 14px 16px 36px;             /* +22px buffer ≈ one full line of 13px text */
  background: var(--c-sticky-bg);
  color: var(--c-sticky-text);
  border-radius: var(--r-toast);
  box-shadow: var(--sh-sticky);
}

/* Status pill (chained modifiers) */
.label        { display: inline-block; width: fit-content; padding: 5px 14px; border-radius: var(--r-pill); font-size: 12px; font-weight: 600; letter-spacing: 0.2px; background: var(--c-text-primary); color: var(--c-text-inverse); }
.label.gray   { background: var(--c-text-primary); color: var(--c-text-inverse); }
.label.green  { background: var(--c-success); color: var(--c-text-inverse); }
.label.red    { background: var(--c-danger); color: var(--c-text-inverse); }
.label.yellow { background: var(--c-warning); color: var(--c-text-inverse); }

/* Numbered step (dark pill with white circle inside) */
.label.step   { padding: 4px 12px 4px 4px; display: inline-flex; align-items: center; gap: 8px; }
.step-num     { width: 22px; height: 22px; border-radius: 50%; background: rgba(255,255,255,0.2); color: var(--c-text-inverse); display: inline-flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 600; }

/* Form pill (selector) */
.pill         { display: inline-block; padding: 6px 14px; border: 1px solid var(--c-border-input); border-radius: var(--r-pill); background: var(--c-surface-page); color: var(--c-text-muted); font-size: 12px; cursor: default; }
.pill.active  { background: var(--c-text-primary); color: var(--c-text-inverse); font-weight: 500; border-color: var(--c-text-primary); }
.pill.day     { width: 30px; height: 30px; border-radius: var(--r-day-pill); padding: 0; display: inline-flex; align-items: center; justify-content: center; }

/* Form input */
.input             { display: block; width: 100%; height: 36px; padding: 8px 12px; background: var(--c-surface-page); border: 1px solid var(--c-border-input); border-radius: var(--r-input); font-size: 13px; color: var(--c-text-primary); }
.input.placeholder { color: var(--c-text-placeholder); }
.input.filled      { color: var(--c-text-strong); }

.field         { margin-bottom: var(--s-field); }

/* Buttons (kebab variants for type, chained for state) */
.btn           { display: inline-flex; align-items: center; gap: 6px; padding: 10px 14px; border-radius: var(--r-button); font-size: 13px; font-weight: 500; border: 1px solid transparent; cursor: default; }
.btn-primary   { background: var(--c-text-primary); color: var(--c-text-inverse); }
.btn-secondary { background: var(--c-surface-page); color: var(--c-text-primary); border-color: var(--c-text-primary); }
.btn-tertiary  { background: transparent; color: var(--c-text-muted); border-color: var(--c-border-input); }
.btn.chosen    { box-shadow: 0 0 0 2px var(--c-success); }
.btn.chosen::before { content: "✓ "; color: var(--c-success); }
.btn.dim       { opacity: 0.45; }

/* Toast (success) */
.toast         { display: flex; gap: 10px; padding: 12px 14px; background: var(--c-toast-bg); border: 1px solid var(--c-toast-border); border-radius: var(--r-toast); box-shadow: var(--sh-toast); }
.toast__icon   { width: 18px; height: 18px; border-radius: 50%; background: var(--c-success); color: var(--c-text-inverse); display: inline-flex; align-items: center; justify-content: center; font-size: 11px; flex-shrink: 0; }
.toast__title  { color: var(--c-toast-title); font-weight: 600; font-size: 13px; }
.toast__meta   { color: var(--c-success); font-size: 12px; }

/* Dialog */
.dialog        { background: var(--c-surface-page); border-radius: 10px; padding: 18px; box-shadow: var(--sh-dialog); display: flex; flex-direction: column; gap: 4px; }
.dialog__title { font-size: 15px; font-weight: 600; color: var(--c-text-primary); }

/* Inline */
b              { color: var(--c-text-primary); font-weight: 700; }
code           { font-family: var(--font-mono); color: var(--c-danger); font-size: 12px; }   /* NO bg/padding – see SKILL.md */
```

## Component recipes

Combine base classes – don't redeclare CSS.

- **Frame card** = `.frame` (default 300px) · `.frame-form` (400px, more padding) · `.frame-tight` (260px) · `.frame-dash` (360px). Subtle shadow; white pops against `.section-grey`.
- **Scenario block** = `.section-grey` wraps a `.row` of `.col` (frame + sticky) separated by `.arrow`.
- **Top-of-section reference card** = `.ref-card` with `.t-eyebrow` label, a rule, and a formula highlight inside.
- **Per-scenario intro** = `.scenario-intro` with `.t-intro-title` + bullet list. Use before each scenario flow.
- **Sticky annotation** = `.sticky` containing `.t-sticky` text. Inline `<b>` and `<code>` allowed.
- **Status pills** = `.label` + variant. Numbered step = `.label.step` + `.step-num` child.
- **Form selector pills** = `.pill` (default) / `.pill.active` (chosen). Day picker uses `.pill.day` for 30×30 round.
- **Inputs** = `.input` (+ `.input.filled` or `.input.placeholder`). Wrap in `.field` for margin.
- **Buttons** = `.btn` + variant. `.btn.chosen` adds the green outline + check.
- **Form section heading** = `<div class="t-form-section">`. First-child inside a frame resets margin automatically.
- **Required asterisk** = `<span style="color: var(--c-danger);">*</span>`.

### Custom one-off recipes

Patterns that don't get a base class because they only appear in one feature so far. Define them inline in the wireflow.

- **Dashboard frame**: `.frame` + dark topbar (`background: var(--c-text-primary)`, white logo square + title + `var(--c-text-disabled)` user) + pageheader (`14px 16px 12px` + bottom border `var(--c-border-frame)`) + table (thead bg `var(--c-surface-grey)`, cell separator `var(--c-border-table-cell)`, focus row `var(--c-surface-focus)`).
- **Public page** (citizen view): 600px-wide `.frame`. White topbar with `var(--c-text-primary)` logo square. Body = 2-col flex (main 2fr / sidebar 1fr). Sidebar: left border `var(--c-border-subdivider)`, 20px padding-left.

## HTML scaffold

```
<body>
  <div id="page">
    <h1 class="t-h1">…</h1>
    <p class="t-subtitle">…</p>
    <div class="ref-card"> <span class="t-eyebrow">…</span> … </div>

    <div class="section">
      <h2 class="t-section-title">…</h2>
      <p class="t-section-desc">…</p>

      <div class="scenario-intro">
        <div class="t-intro-title">…</div>
        <ul style="list-style:none; padding-left:0;">
          <li>&bull;&nbsp; <b>…</b> …</li>
        </ul>
      </div>

      <div class="section-grey">
        <div class="row">
          <div class="col">
            <div class="label gray">…</div>
            <div class="frame">…</div>
            <div class="sticky">…</div>
          </div>
          <div class="arrow">→</div>
          <div class="col">…</div>
        </div>
      </div>
    </div>
  </div>
</body>
```

## Iconography

Plain text characters only (`→` `✓` `&bull;` `&rarr;`). Logo squares = coloured `<div>`s with `border-radius: var(--r-logo)`. Avoid `<svg>` and `border-radius: 50%` for content (sometimes captures square; OK for tiny 10px legend dots).

## Quick start for new wireflows

1. Create `<feature>-wireflow/index.html` with `<script src="https://mcp.figma.com/mcp/html-to-design/capture.js" async></script>` in `<head>`.
2. Paste **Foundation**, **Tokens**, **Type utilities**, and **Base classes** from this doc into a single `<style>` block.
3. Use the **HTML scaffold** above as the page skeleton.
4. Adjust `#page { min-width: ... }` for the feature's horizontal extent.
5. Define one-off recipes (dashboards, public pages) inline beneath the base classes.
6. Run the capture procedure in `SKILL.md`.
