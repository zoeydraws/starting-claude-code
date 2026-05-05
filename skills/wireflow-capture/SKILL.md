---
name: wireflow-capture
description: Authoring + capture workflow for HTML wireflows pushed into Figma via the html-to-design MCP. Use whenever the user works on a wireflow file (e.g. `<feature>-wireflow/index.html`) – editing markup, fixing layout, pushing to Figma, or making small text/style edits to an already-captured frame. Covers converter quirks, autolayout authoring rules, the serve-capture-poll loop, and the in-place edit path via `mcp__figma__use_figma`.
---

# Wireflow Authoring & Capture

Pushes a local HTML wireflow into a Figma file via `mcp__figma__generate_figma_design`. The converter is closed-source and inconsistent about producing autolayout, so authoring follows specific rules.

## When to use

- Editing wireflow HTML in your wireflow folder (e.g. `<feature>-wireflow/index.html`) – apply authoring rules
- Pushing to Figma ("re-capture", "push to figma", "update the wireflow") – run the capture procedure
- Making a small text or style tweak to an already-captured frame ("change this text in Figma", "update the colour on frame X") – use the in-place edit path
- Captured frame looks broken – diagnose via failure modes

**Visual style spec lives in `./STYLE_GUIDE.md`** – read it before authoring new components or starting a new wireflow. It covers tokens, type scale, spacing, component patterns. The included guide is a starting point; swap tokens for your own brand if needed.

## Capture vs in-place edit – decision tree

| Type of change | Path | Why |
|---|---|---|
| New scenario, new layout, structural HTML edit, multi-frame change | Capture procedure (creates a new frame) | HTML is the source of truth; structural edits are easier to author in HTML and re-capture |
| Small text/style/colour tweak on one specific frame | In-place edit via `mcp__figma__use_figma` | Faster than re-capture, no stale frame to clean up, no waiting on poll loop |

**HTML is always the source of truth.** Whichever path you use, also patch `<feature>-wireflow/index.html` to match. Otherwise the next re-capture will re-introduce the old text and silently undo the in-place edit. No exceptions.

## Authoring rules

**Container vs text-content:**
- Container boxes (sections, cards, dashboards, page wrappers): `display: flex` – captures as autolayout.
- Text-content boxes with mixed inline children (`<b>` / `<code>` / text): `display: block` – flex parents fragment inline children.

**Page wrapper rule:** never make `<body>` the flex container. Keep body as a plain block and wrap all top-level content in a `<div id="page">` that owns `display: flex; flex-direction: column` and the page padding/width. The converter mishandles body's bounding box when body is flex – top children render above the captured frame's top edge, sticking out of the wrapper.

```html
<body>
  <div id="page"> ... all content ... </div>
</body>
```
```css
body { margin: 0; padding: 0; }
#page { min-width: 2300px; width: max-content; padding: 64px; display: flex; flex-direction: column; }
```

**Page width rule:** use `min-width: <baseline>; width: max-content` on `#page`, never a fixed `width`. A fixed page width clips when any row exceeds it – content drifts outside the captured Figma frame on the right side (same visual symptom as the body-as-flex bug, different cause). `max-content` lets the page grow horizontally to contain its widest row; `min-width` keeps short pages from collapsing narrower than the baseline.

**Inline `<code>`:** strip `background`, `padding`, `border-radius`. Keep only `color` + monospace `font-family`. Styled inline code captures as a floating frame that overlaps surrounding text.

**Hurts autolayout:** `display: block` (HTML default), `position: absolute` children, `::before` / `::after` for visual content (converter strips them), `display: table`, `border-radius: 50%` for content.

**Helps autolayout:** `display: flex` containers with non-mixed children. Explicit `width` (not `max-width`) on flex containers.

**Bullet lists:** converter strips `list-style: disc` and `::before` pseudo-bullets. Inline the bullet character:
```html
<ul style="list-style: none; padding-left: 0;">
  <li>&bull;&nbsp; <b>Setup:</b> Weekly cadence...</li>
</ul>
```

**Text-content card pattern (stickies, scenario-intro, dialogs).** Cards with wrapping prose are captured as fixed-height. Figma re-renders text and often wraps to one extra line, overflowing the frame. Flex doesn't fix this – tested. Add a bottom-padding buffer instead:

```css
.sticky          { padding: 14px 16px 22px; }    /* +8px  ≈ half line of 13px text */
.scenario-intro  { padding: 20px 24px 36px; }    /* +16px ≈ one line of 13px text */
.ref-card        { padding: 24px 28px 40px; }    /* +16px */
```

Buffer rule: roughly `1.2× line-height` of body text inside. Add buffers reactively when a card overflows, not pre-emptively. Candidates if they break: `.ref-example`, `.dialog`, `.sched-card`.

**Optional – em-dash hook:** if your repo blocks `U+2014` in writes (some teams enforce this via a pre-tool-use hook), use en-dash, comma, or parens. Normalise user-pasted content before writing.

## Procedure

**Prerequisites:** wireflow HTML must include `<script src="https://mcp.figma.com/mcp/html-to-design/capture.js" async></script>` in `<head>`. Need target Figma `fileKey` + page `nodeId` – ask the user if unknown. Extract from the Figma URL: `figma.com/design/<fileKey>/...?node-id=<nodeId>` (convert `-` to `:` in nodeId).

### 1. Server

```bash
cd <feature>-wireflow && python3 -m http.server 8765 > /tmp/wireflow-server.log 2>&1 &
sleep 1
```

If already running (`curl -sI http://localhost:8765/ | head -1` returns `200`), skip. If port busy, pick another and use consistently.

### 2. Generate captureId

Call `mcp__figma__generate_figma_design` with `outputMode: "existingFile"`, `fileKey`, `nodeId`. Returns a `captureId` (UUID).

### 3. Open with capture hash

```bash
open "http://localhost:8765/#figmacapture=<captureId>&figmaendpoint=https%3A%2F%2Fmcp.figma.com%2Fmcp%2Fcapture%2F<captureId>%2Fsubmit&figmadelay=2500"
sleep 9
```

For wireflows >1500 lines, bump to `sleep 12`.

### 4. Poll

Call `mcp__figma__generate_figma_design` with just `captureId`. If `processing`, sleep 5s and retry. Stop when response includes the new node URL. Don't generate a new captureId mid-poll – the converter is idempotent on the same id.

### 5. Leave server running

Iterate fast: don't stop the server between captures. Only stop if the user says they're done.

### 6. Report

Give the user the new node URL (e.g. `figma.com/design/.../?node-id=215-2`). Mention prior capture node ids so they can delete stale frames.

## Procedure: in-place edit (small tweaks to one frame)

Use this when the user wants to change text, colour, or a similar small property on a specific captured frame, *not* re-author + re-capture.

### 1. Get the target node ID

The user must point at a specific frame. Accept any of:
- A Figma URL containing `?node-id=238-1835` – convert hyphens to colons → `238:1835`.
- A bare node ID like `238:1835`.

If they say "this frame" without a link, ask for the URL or node ID. Don't guess – the file has many captured frames.

### 2. Run `mcp__figma__use_figma`

`fileKey` from the URL (`figma.com/design/:fileKey/...`) – ask the user if unknown. `code` is a small Plugin API script that finds the target nodes inside the frame and edits them.

### 3. Font-loading rule for text edits

Setting `node.characters` on a TEXT node throws unless every font used in that node is loaded first. The correct call is `getRangeFontName(i, i+1)` per character index – there is no `getRangeAllFontNames` method, contrary to what intuition suggests.

```js
const fonts = new Set();
for (let i = 0; i < t.characters.length; i++) {
  const f = t.getRangeFontName(i, i + 1);
  if (f !== figma.mixed) fonts.add(JSON.stringify(f));
}
for (const fStr of fonts) await figma.loadFontAsync(JSON.parse(fStr));
t.characters = "new value";
```

For a single-font node, just `loadFontAsync(t.fontName)` works. The loop above handles mixed-font nodes safely.

### 4. Patch the HTML to match (mandatory)

After every successful in-place edit, update `<feature>-wireflow/index.html` with the same change. Skipping this step lets the next re-capture silently overwrite the in-place edit and brings back the old value. HTML is the source of truth.

### 5. Report

Tell the user how many nodes were updated, the node IDs touched, and confirm the HTML was patched.

## Failure modes

- **Polling never completes:** browser didn't load the page. Check the tab focused / opened. After 10 polls, inspect `/tmp/wireflow-server.log` for 404s on the capture script.
- **Figma page empty:** zero-height content (e.g. `display: flex` without sized children). Verify in browser.
- **Layout broken in Figma but fine in browser:** see Authoring rules. Common: `display: table`, `position: absolute`, `::before` for visual content, styled inline `<code>`, mixed inline content in flex parent.
- **Text frame overflows / clips:** apply the text-content card buffer (see Authoring rules). Don't try flex – makes it worse.
- **Top content sticks out above the wrapper frame** (h1 / subtitle / first card render above the white page background): `<body>` is the flex container. Move flex layout to a `<div id="page">` wrapper – see Page wrapper rule.
- **Right-side content drifts outside the page background** (rightmost columns of a row render past the white page edge, sometimes off the captured frame): `#page` has a fixed `width` smaller than the widest row. Switch to `min-width + width: max-content` – see Page width rule.

## Notes

- Each capture creates a NEW frame; the html-to-design converter never edits existing ones. Stale frames accumulate – delete in Figma when crowded. (Note: the in-place edit path via `mcp__figma__use_figma` *can* update existing frames – use it for small tweaks; see decision tree above.)
- Capture script tag is harmless to leave in production.
- Parallel captures supported (each gets its own captureId), but for iterate-recapture, keep them sequential.
