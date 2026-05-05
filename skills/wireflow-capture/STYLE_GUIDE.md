# Wireflow Visual Style

A starter house style for HTML wireflows so a set reads consistently in Figma. Treat tokens as a starting point – swap colours, type, and radii for your own brand. The component patterns and layout primitives are the durable bits.

## Foundation

```css
* { box-sizing: border-box; }
body {
  font-family: -apple-system, "Segoe UI", Roboto, sans-serif;
  margin: 0;
  padding: 0;
  background: #ffffff;
  color: #1e1e1e;
  font-size: 14px;
}
#page {
  min-width: 2300px;       /* horizontal scroll OK – multi-scenario flows are wide */
  width: max-content;
  padding: 64px;
  display: flex;
  flex-direction: column;
}
```

Monospace stack (inline code only): `ui-monospace, SFMono-Regular, Menlo, monospace`.

## Colour tokens

**Text:**
- `#1e1e1e` – primary text, primary buttons, dark pills, top bars, logos
- `#2e2e2e` – slightly softer body
- `#474747` – muted body
- `#686868` – captions, eyebrows, meta, placeholder labels
- `#a0a0a0` – placeholder text
- `#b0b0b0` – disabled / unchecked checkbox border
- `#9c9c9c` – arrow glyphs

**Borders / dividers:**
- `#d0d0d0` – input border
- `#e3e3e7` – frame / card / section border (workhorse)
- `#ececec` – sub-divider inside cards
- `#f0f0f3` – inner table cell separator
- `#e8e8ea` – thead cell separator

**Surfaces:**
- `#ffffff` – page background, all white frames
- `#f5f5f7` – scenario-block bg, table headers, code chip bg, sidebar grey
- `#fafafa` – focus row in dashboard table

**Status:**
- `#1e7d3a` – success / healthy / "chosen" outline
- `#b42318` – warning / overdue / required asterisk / inline code colour
- `#b8860b` – yellow status pill text-on-bg
- `#06502a` – toast title (dark green)
- `#abefc6` – toast border (light green)
- `#ecfdf3` – toast background

**Highlights:**
- `#fef7c0` / `#2e2400` – sticky bg / text
- `#fff7d6` / `#f4d56b` – formula highlight bg / border
- `#fff4d6` / `#8a6a00` – approaching badge bg / text
- `#fde2e2` / `#b42318` – overdue badge bg / text
- `#fdf2f2` – inline code chip bg (only on grey scenario-sub)

**Markers (timeline dots):**
- `#d0d0d0` healthy · `#f4c542` approaching · `#e84747` overdue · `#1e1e1e` update

## Type scale

| Use                      | Size  | Weight | Letter          | Colour    | Notes |
|--------------------------|-------|--------|-----------------|-----------|-------|
| Page title (`h1`)        | 36    | 700    | -0.01em         | `#1e1e1e` | margin `0 0 12px` |
| Page subtitle            | 14    | 400    | –               | `#686868` | margin `0 0 56px` |
| Section title (`h2`)     | 22    | 700    | -0.01em         | `#1e1e1e` | margin `0 0 6px` |
| Section description      | 13    | 400    | –               | `#686868` | line-height 1.55 |
| Scenario head            | 18    | 700    | -0.01em         | `#1e1e1e` | margin `0 0 6px` |
| Scenario sub             | 13    | 400    | –               | `#686868` | line-height 1.55 |
| Scenario intro title     | 16    | 700    | –               | `#1e1e1e` | inside scenario-intro |
| Form section title       | 11    | 700    | 1px upper       | `#686868` | bottom border 1px `#e3e3e7` |
| Field label              | 13    | 500    | –               | `#1e1e1e` | margin-bottom 6px |
| Input text               | 13    | 400    | –               | `#1e1e1e` | height 36px, padding 8px 12px |
| Body in cards            | 13    | 400    | –               | `#1e1e1e` | line-height 1.55 |
| Eyebrow caption          | 11    | 700    | 0.8px upper     | `#686868` | for ref-card sections |
| Table thead cell         | 10–11 | 600    | 0.5–0.6px upper | `#686868` | |
| Table body cell          | 12    | 400    | –               | `#1e1e1e` | line-height 1.4 |
| Step label (timeline)    | 10    | 600    | –               | `#2e2e2e` | |
| Step date (timeline)     | 9     | 400    | –               | `#686868` | |
| Inline code              | 12    | 400    | –               | `#b42318` | monospace, NO bg/padding |
| Sticky body              | 13    | 400    | –               | `#2e2400` | line-height 1.55 |
| Status pill / badge      | 11–12 | 600    | 0.2px           | varies    | bg-on-colour |
| Pill (form selector)     | 12    | 400/500| –               | `#686868` / `#fff` (active) | |

## Spacing

Page padding: **64px**. Section margin-bottom: **96px**. Scenario-block: **32px** padding, **28px** margin-bottom. Frame padding: **18px** default / **24px** form / **16px** compact. Card padding: **18–24px**. Field margin-bottom: **14px**. Row gap: **16px**. Pill gap: **4px**. Vertical rhythm in fields: **6–8–12–14**.

## Border radii

Frames / cards **12px** · Section-grey **16px** · Inputs / buttons **6–8px** · Pills **16–18px** · Day pill (round) **15px** (30×30) · Status badge **12px** · Toast / sticky **8px** · Logo squares **2–4px**.

## Shadows

- Frames / cards: `0 1px 3px rgba(0,0,0,0.04)`
- Sticky: `0 1px 2px rgba(0,0,0,0.04)`
- Toast: `0 4px 12px rgba(0,0,0,0.06)`
- Dialog: `0 8px 24px rgba(0,0,0,0.10)`
- Step marker: `0 0 0 1px #b0b0b0` ring + `2px solid #fff` border

## Component patterns

**Frame** (white card): white bg, `1px #e3e3e7` border, `12px` radius, `18px` padding, subtle shadow. Width varies (300 default, 400 form, 260 tight, 360 dashboard).

**Section-grey scenario block**: `#f5f5f7` bg, `1px #e3e3e7` border, `16px` radius, `32px` padding. White frames pop against the grey.

**Ref card** (top-of-section reference): white card with eyebrow + rule + formula highlight + example. Use for cadence rules, formulas, key constraints. `24px 28px 40px` padding (bottom buffer), max-width `880px`.

**Scenario intro card**: white card before each scenario flow. 16px title + bullet list. `20px 24px 36px` padding (bottom buffer), max-width `600px`.

**Sticky note** (yellow callout): `display: block`, `max-width: 320px`, padding `14px 16px 22px` (bottom buffer), bg `#fef7c0`, body `#2e2400`. Inline `<b>` for bold, inline `<code>` for code (no bg).

**Status pill** (`.label`): dark `#1e1e1e/white` neutral; variants `.green` `#1e7d3a`, `.red` `#b42318`, `.yellow` `#b8860b`. 12px / 600 / `5px 14px` / `16px` radius. `width: fit-content`.

**Numbered step label** (`.label.step` + `.step-num`): dark pill with white-circle number inside. Pill padding `4px 12px 4px 4px`. Number 22×22 round, semi-transparent white bg, white text.

**Form pill** (selector): default white bg / `1px #d0d0d0` / `#686868` text / `12px / 6px 14px / 18px` radius. Active: `#1e1e1e` bg / white / weight 500. Day pill: 30×30 round.

**Form input**: white bg, `1px #d0d0d0`, `6px` radius, `8px 12px` padding, `36px` height. `.filled` `#2e2e2e`, `.placeholder` `#a0a0a0`. Required asterisk: `<span style="color:#b42318;">*</span>`.

**Form section title**: 11px / 700 / uppercase / `1px` letter-spacing / `#686868`. Bottom border `1px #e3e3e7`. Margin `20px 0 12px`. First-child resets `margin-top: 0`.

**Button**: 13px / `10px 14px` / `8px` radius. Primary `#1e1e1e/white`. Secondary `white / #1e1e1e text / 1px #1e1e1e border`. Tertiary `transparent / #686868 / 1px #d0d0d0`. Chosen: `box-shadow: 0 0 0 2px #1e7d3a` + green check via `::before`. Dim alt: `opacity: 0.45`.

**Toast (success)**: `#ecfdf3` bg, `#abefc6` border, `#1e7d3a` icon circle with white check, `#06502a` title, `#1e7d3a` meta. `12px 14px` padding, `8px` radius.

**Dashboard frame**: white card, `#1e1e1e` topbar (white logo square + title + `#b0b0b0` user), pageheader (`14px 16px 12px` + bottom border), table body. Table thead bg `#f5f5f7`, cells `1px #f0f0f3` separator, focus row `#fafafa`.

**Public page** (citizen view): 600px wide white card. White topbar with `#1e1e1e` logo square. Body = 2-col flex (main 2fr / sidebar 1fr). Sidebar: left border `#ececec`, `20px` padding-left. Title 22px/700.

**Dialog**: white card, `10px` radius, `18px` padding, shadow `0 8px 24px rgba(0,0,0,0.10)`. Title 15px/600. Body: column flex with 4px gap.

**Inline elements**: `<b>` → `#1e1e1e/700`. `<code>` → `#b42318` monospace 12px, NO bg/padding/radius. Required: `<span style="color:#b42318;">*</span>`. Bullet in lists: `&bull;&nbsp;` inline (converter strips `<ul>` markers).

**Iconography**: plain text characters only (`→` `✓` `&bull;` `&rarr;`). Logo squares = coloured `<div>`s with `border-radius: 2–4px`. Avoid `<svg>` and `border-radius: 50%` for content (sometimes captures square; OK for tiny 10px legend dots).

## Layout primitives

```css
.row {
  display: flex;
  gap: 16px;
  align-items: flex-start;
  margin-bottom: 40px;
  flex-wrap: nowrap;
}
.col { display: flex; flex-direction: column; }
.arrow {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  font-size: 22px;
  color: #9c9c9c;
  padding-top: 90px;            /* aligns arrow with frame body, not frame top */
  width: 28px;
  flex-shrink: 0;
}
```

Arrows go in their own `.col` of width 28px. Arrow content = `→` character.

## Section structure

```
body
└─ #page
   ├─ h1 (page title)
   ├─ p.subtitle
   ├─ div.ref-card                     (top-of-page reference card)
   └─ div.section
      ├─ h2.section-title
      ├─ p.section-desc
      ├─ div.scenario-intro            (per scenario: title + bullets)
      ├─ div.section-grey              (or .scenario-block – grey container)
      │  └─ div.row
      │     ├─ div.col                 (frame + sticky)
      │     │  ├─ div.label.gray       (pill above frame)
      │     │  ├─ div.frame            (the UI mock)
      │     │  └─ div.sticky           (annotation)
      │     ├─ div.arrow
      │     └─ div.col                 (next frame...)
      └─ ...
```

## Quick start for new wireflows

Create `<feature>-wireflow/index.html` with the foundation block above plus the universals: `body`, `#page`, `h1`, `.subtitle`, `.section`, `.section-title`, `.section-desc`, `.row`, `.col`, `.label` (+ variants), `.frame`, `.sticky`, `.pill`, `.input`, `.field`, `.form-section-title`, `.scenario-block`, `.ref-card`, `.scenario-intro`, `.arrow`, `.btn` (+ variants).

Adjust `#page { min-width: ... }` for the feature's horizontal extent. Include the capture script in `<head>`:

```html
<script src="https://mcp.figma.com/mcp/html-to-design/capture.js" async></script>
```
