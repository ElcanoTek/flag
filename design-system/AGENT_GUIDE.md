# Agent Implementation Guide

Use this when a prompt says: "Follow the design system in the flag repo."

## Source of Truth
Use this precedence when implementing:
1. `tokens/design-tokens.css`
2. `tokens/design-tokens.json`
3. this guide
4. `COMPONENTS.md` and `INTERACTION_ACCESSIBILITY.md`

## Required Setup Order
1. Import `tokens/design-tokens.css` first.
2. Add component styles that consume token variables.
3. Add markup that follows canonical component structures in `COMPONENTS.md`.
4. Add required interaction states and accessibility attributes.

## Hard Rules
- Use token variables from `tokens/design-tokens.css` / `tokens/design-tokens.json`; do not invent one-off values.
- Do not hardcode visual values where semantic/scale tokens exist (color, spacing, radius, shadow, transition, opacity).
- Typography is fixed:
  - Headlines/subheadlines: `Dubai Bold`
  - Body/UI text: `Dubai Regular`
- Exception: logs code display and task tracker components use code fonts (`--font-code`, `--font-code-ui`) to match canonical MOC baseline.
- Type scale is tokenized in `rem` (Title `1.75rem`, Subtitle `1.125rem`, Body `0.75rem-0.875rem`).
- Do not introduce arbitrary values like `0.8125rem` radius or `0.98rem` body text outside token scale.
- Keep border/radius/shadow values on token scale only.
- The canonical theme contract is root-level `html[data-theme="light|dark"]`.
- Theme behavior must default to system preference and only persist explicit user choice (`flag-theme-preference`).
- Shared theme toggle must use sun/moon icons from `icons/core-icons.svg`.
- Do not invent product-specific theme state logic when the shared flag pattern applies.
- Shell background default is `--gradient-bg-home-signature` unless exception is explicitly documented.
- Primary actions must use primary variant semantics.
- Danger actions must use danger semantics.
- Focus ring must use `var(--focus-ring)` and remain stronger than hover.

## Quick Token Map
- Primary: `--color-primary`
- Secondary: `--color-secondary`
- Accent: `--color-accent`
- White/Black: `--color-white`, `--color-black`
- Background: `--color-bg`
- Surface: `--color-surface-1`, `--color-surface-2`
- Border: `--color-border`
- Text: `--color-text-primary`, `--color-text-secondary`, `--color-text-muted`
- Status: `--color-success`, `--color-warning`, `--color-danger`, `--color-info`
- Shell gradient default: `--gradient-bg-home-signature`
- Shell reserved exceptions: `--gradient-bg-product-standard`, `--gradient-bg-ops-console`
- Surface gradients: `--gradient-surface-panel`, `--gradient-surface-card`, `--gradient-surface-elevated`

## Theme Rules
- Default mode is `system` (`prefers-color-scheme`) with no stored explicit preference.
- Root selector contract is `html[data-theme="light"]` or `html[data-theme="dark"]`.
- Token overrides for light mode live in `tokens/design-tokens.css` under `:root[data-theme="light"]`.
- Store explicit user preference in `localStorage` with key `flag-theme-preference`.
- System theme changes should auto-apply only when preference is unset/`system`.
- Do not define per-component ad hoc light-mode values in product CSS.
- If a theme value is missing, add it to token files first.

Recommended implementation order for new product adoption:
1. Import `tokens/design-tokens.css` and apply root `data-theme` attribute contract.
2. Add the shared theme controller (resolve stored preference -> resolve system preference -> apply root theme).
3. Add the shared sun/moon toggle control and wire accessible labels/states (`aria-label`, `aria-pressed`).
4. Add localStorage persistence using `flag-theme-preference` and system-change listener behavior.
5. Verify theme parity for all canonical component states and announce theme changes when appropriate.

## Component Defaults
- Buttons: `primary`, `secondary`, `ghost`, `danger`.
- Interactive controls must define explicit `hover`, `active`, and `focus-visible` states.
- Inputs: `2.5rem` min height, `radius-md`, token border/focus styles.
- Include full input coverage: text, search, password, email, number, tel, url, textarea, select, date, time, datetime-local, file.
- Number input must use the canonical stepper pattern (`.number-input`, `.number-input__field`, `.number-input__btn`) where increment/decrement controls are needed.
- Date picker must use canonical themed classes (`.custom-datepicker` and themed `.flatpickr-*` styles when Flatpickr is used).
- File upload must use the canonical dropzone structure (`.file-upload-dropzone`, `.dropzone-content`, `.file-list`).
- Accordion disclosure should use the canonical plus/minus summary indicator.
- Single-file selection lists should use the canonical custom radio file selector pattern.
- Checkbox controls should use the shared design-system checkbox pattern (custom box + visible focus ring).
- Tables: sticky headers optional, row hover subtle, status badges use semantic tokens.
- Clickable action cards must use the canonical featured structure (`featured-head`, kicker, title, description) and explicit selected state (accent border/top accent/elevation).
- Do not implement clickable action cards without both explicit `selected` and `focus-visible` states.
- Use full task status badge set where applicable: pending, scheduled, assigned, leased, running, analyzing, success, error, cancelled.
- For recipient selection in task forms, use canonical email selection pills (`chips-container`, `chip chip-email`, `chip-delete`).
- App header must use the common canonical pattern (brand mark + `Elcano Internal` eyebrow + page title + right-side utility actions).
- Modals: surface container, max-width tokens, explicit close button and escape key.
- Empty/Loading/Error: always include heading, explanatory body text, and next action.
- Common icon glyphs must come from `icons/core-icons.svg` (`download`, `trash`, `logout`, `paperclip`, etc.).
- Logos must come from `design-system/logos/` and follow `LOGOS.md` usage mapping.
- Logs code display must use canonical classes: `.tool-call-item`, `.tool-call-name`, `.tool-call-id`, `.tool-call-code`, `.tool-call-other-args`.
- Task tracker must use canonical classes: `.task-tracker-container`, `.task-tracker-cmd`, `.task-tracker-list`, `.task-tracker-item`, `.tt-icon`, `.tt-id`, `.tt-title` with `status-done|status-inprogress|status-todo`.

## Email Rules

### Canonical Reference
- Use `design-system/email-safe.html` as the canonical base for every generated HTML email.
- When adapting the reference, preserve the dark header plus light body structure unless there is a documented reason to change it.
- Use `{{placeholder}}` markers for all dynamic content (dates, names, URLs, metrics). The agent populates these at generation time; the template defines the structure.
- Treat `design-system/preview/email-safe.html` as a deployed preview artifact, not an authored source file. Sync it from the canonical template with `bash design-system/sync-email-preview.sh` after canonical email changes.

### Layout and Structure
- Keep email layouts table-first for all structural regions; use `role="presentation"` on layout tables.
- Enforce a strict maximum content width of **600px**. The inner container table must use `max-width:600px` in CSS and be wrapped in MSO conditional ghost tables (`<!--[if mso]><table width="600">...<![endif]-->`) so Outlook desktop also respects the constraint.
- Keep production email layouts single-column by default and within the canonical centered container pattern from `email-safe.html`.
- Include the Outlook DPI scaling fix in the `<head>` inside an MSO conditional block:
  ```html
  <!--[if mso]>
  <xml>
    <o:OfficeDocumentSettings>
      <o:AllowPNG/>
      <o:PixelsPerInch>96</o:PixelsPerInch>
    </o:OfficeDocumentSettings>
  </xml>
  <![endif]-->
  ```
- Add the XHTML namespaces to the `<html>` tag: `xmlns:v="urn:schemas-microsoft-com:vml"` and `xmlns:o="urn:schemas-microsoft-com:office:office"`.
- Do not use `<div>` for structural width or height; Outlook ignores div dimensions. Use `<table>` and `<td>` instead.

### Styling
- Inline every critical visual style on the element that needs it. Do not rely on embedded or external CSS for core rendering.
- Use explicit text, border, and background colors on every important block so the email survives dark-mode inversion and client overrides.
- Avoid pure white (`#FFFFFF`) for large backgrounds; prefer off-whites like `#F4F6FB` or `#FAFAFA`. Avoid pure black (`#000000`) for text; prefer dark greys like `#141824` or `#222222`. This mitigates aggressive dark mode inversion in Gmail iOS and Outlook desktop.
- Stay with the email-safe font stack (`'Segoe UI', Arial, sans-serif`). Do not use web fonts; they are unsupported in Outlook (falls back to Times New Roman) and Gmail (strips `@font-face`).
- Use pixel (`px`) values for all padding, margin, and font sizes. Do not use `rem`, `em`, percentages, or CSS variables.
- Use simple, resilient blocks: table sections, explicit padding, explicit borders, explicit cell backgrounds, and text links or bulletproof CTA buttons.
- Add `-webkit-text-size-adjust:100%` and `-ms-text-size-adjust:100%` to the `<body>` style to prevent mobile clients from auto-scaling text.

### Data Table Pattern
- Data tables in email must remain semantic tables on desktop: use `<table>`, `<thead>`, `<tbody>`, and `scope="col"` on header cells.
- Zebra striping is allowed on desktop tables, but the stripe must cover the full row, not just the first column.
- On mobile, convert data tables into stacked card rows rather than relying on horizontal scrolling.
- In stacked mobile mode, the first cell becomes the card header and should use the highlighted header background (`#EEF3FF`) with stronger weight.
- In stacked mobile mode, metric cells should share one neutral body background (`#FAFAFA`) so the row reads as a single card.
- In stacked mobile mode, borders must be applied to cells, not `tr` wrappers, to avoid right-edge bleed in clients that blockify table rows.
- Mobile stacked rows should preserve label/value clarity by surfacing compact inline labels such as `Campaign`, `Current`, `Prior`, and `WoW`.
- Dark-mode preview behavior for stacked tables must remap both backgrounds and border colors to the same dark palette used by larger-screen preview modes.

### Typography and Sizing
- Minimum body text size: **16px**. Minimum heading size: **22px**. Minimum overline/label size: **12px**.
- Minimum tap target size for buttons and links: **44x44 pixels**.
- CTA button text must not exceed **25 characters**. Use one primary CTA per email.
- Heading text must not exceed **60 characters**; truncate with ellipsis if exceeded.
- Data-dense contexts (tables, dashboards) may use **15px** for cell text and **13px** for table headers, but never below these floors.
- Use the bulletproof CTA button pattern from `email-safe.html`: a `<table>` with a `<td>` that has explicit `background-color` and `padding`, containing an `<a>` with matching inline styles. Include a VML `<v:roundrect>` fallback inside `<!--[if mso]>` for Outlook.

### Images
- All images must include explicit `width` and `height` HTML attributes plus `style="max-width:100%; height:auto;"`.
- All images must include descriptive `alt` text. Style the `alt` text with inline `font-size`, `color`, and `font-family` so the email is readable when images are blocked.
- Prefer PNG for graphics and JPEG for photographs. WebP is acceptable for non-Outlook audiences but lacks Outlook desktop support.
- Do not use CSS background images unless a VML fallback is provided for Outlook.
- Keep total email weight (HTML + all hosted images) under **800KB**.

### Size and Performance
- Keep the total raw HTML payload under **100KB** to prevent clipping in Gmail (~102KB threshold) and Yahoo Mail.
- Minify HTML output when the payload approaches the limit.
- Include a hidden preheader text block immediately after the `<body>` tag for inbox preview optimization. Use `display:none; max-height:0px; overflow:hidden;` and pad with `&zwnj;&nbsp;` entities to push other content out of the preview.

### Prohibited Features
- Do not use JavaScript, `<form>` elements, external CSS (`<link>` or `@import`), CSS gradients, `background-image`-dependent content, transparency-dependent text treatments, or complex positioned layouts.
- Avoid depending on unsupported selectors or modern layout features such as `display:grid`, flexbox-only structure, `filter`, `backdrop-filter`, pseudo-element-critical content, CSS variables (`var()`), `calc()`, or `rem`/`em` units.
- Avoid `<p>` tags for spacing; Outlook adds inconsistent margins. Use `<td>` with explicit padding instead.
- Do not place `background-image: url(...)` inside `<style>` blocks; Gmail strips the entire style block if any rule contains it.
- Keep embedded `<style>` blocks under **8,192 characters** (Gmail's limit). One syntax error causes Gmail to strip the entire block.

### Dark Mode Resilience
- Include `<meta name="color-scheme" content="light dark">` and `<meta name="supported-color-schemes" content="light dark">` in the `<head>`.
- Use off-white backgrounds (`#F4F6FB`, `#FAFAFA`) and dark grey text (`#141824`, `#222222`) instead of pure white/black. These produce less jarring results when clients like Gmail iOS and Outlook desktop apply automatic color inversion.
- Do not rely on `@media (prefers-color-scheme: dark)` for critical styling; only Apple Mail, Outlook Mac, and Thunderbird fully support it. Gmail iOS and Outlook desktop apply their own inversion with no developer override.
- Ensure all foreground-background color pairings maintain at least **4.5:1 contrast** in both their original and inverted states.
- The preview page's dark-mode simulation is a review aid only. Keep preview-specific color remapping logic in `design-system/preview/email-preview.html`, and do not treat that simulation code as the production email contract.

### Accessibility
- Maintain a minimum text-to-background contrast ratio of **4.5:1** (WCAG AA).
- Use semantic heading structure: one primary heading per email, logical heading order.
- Use `role="presentation"` on all layout tables.
- Include a plain-text version of every HTML email when the sending infrastructure supports it.
- Ensure all links have descriptive text (avoid bare "click here").

### Compliance and Footer
- Every email must include a locked footer section that the agent cannot modify or remove.
- The footer must contain: the sender's physical mailing address, a clear unsubscribe link (minimum **14px**, visually distinct with underline), and a brief explanation of why the recipient received the email.
- The canonical footer pattern is defined in `email-safe.html`.

### Testing Matrix
- Always test generated emails before shipping. The minimum required testing matrix is:

| Client | Priority | Key Concerns |
|---|---|---|
| Gmail (Web) | Required | Strips most CSS; 102KB clipping; no media queries on desktop |
| Gmail (iOS/Android) | Required | Supports media queries; iOS applies dark mode inversion |
| Outlook Desktop (Word engine) | Required | Word rendering; no modern CSS; needs ghost tables and VML |
| Outlook (New/Chromium) | Required | Modern rendering; ignores MSO conditionals |
| Apple Mail (macOS/iOS) | Recommended | Gold standard; full CSS support |
| Yahoo Mail | Recommended | `height`-to-`min-height` bug; no dark mode inversion |
| Samsung Mail | Recommended | Auto-fit content from HTML width attributes |

### QA Checklist
- Verify subject and preheader lengths are sane and preview cleanly in inbox snippets.
- Verify desktop light preview.
- Verify desktop dark preview simulation.
- Verify mobile light preview.
- Verify mobile dark preview simulation.
- Verify long campaign names do not break stacked mobile cards.
- Verify the data table still reads clearly when there is only one row.
- Verify the data table still reads clearly when there are many rows.
- Verify CTA copy stays within the 25-character limit and remains tappable.
- Verify footer address, unsubscribe link, and recipient-reason text are present.
- Verify the plain-text companion version is updated when the sending system supports it.

## Accessibility Requirements
- Icon-only controls require `aria-label`.
- Interactive custom controls require keyboard support:
  - Enter/Space activation where `role="button"` is used
  - visible `focus-visible` state using `var(--focus-ring)`
- Forms must have explicit label/input association.
- Table headers must use semantic scope (`scope="col"`).
- Dynamic processing/loading text should be announced via polite live regions when status changes.

## Disallowed Patterns
- External font/CDN dependencies for core UI styles.
- New ad hoc status colors.
- Mixed font systems within one screen (except canonical MOC-baseline code display/task tracker components).
- Invisible focus states.
- Gradient-heavy controls for every element (reserve gradients for hero/high-emphasis surfaces).
