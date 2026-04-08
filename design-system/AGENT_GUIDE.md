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
- Use `design-system/email-safe.html` as the canonical base for every generated HTML email.
- Keep email layouts table-first for all structural regions; use `role="presentation"` on layout tables.
- Inline every critical visual style on the element that needs it. Do not rely on embedded or external CSS for core rendering.
- Use explicit text, border, and background colors on every important block so the email survives dark-mode inversion and client overrides.
- Stay with the email-safe font stack already used in `email-safe.html` (`'Segoe UI', Arial, sans-serif`). Do not use web fonts.
- Keep production email layouts single-column by default and within the canonical centered container pattern from `email-safe.html`.
- Use simple, resilient blocks: table sections, explicit padding, explicit borders, explicit cell backgrounds, and text links or bulletproof CTA buttons.
- Do not use JavaScript, forms, external CSS, gradients, background-image-dependent content, transparency-dependent text treatments, or complex positioned layouts.
- Avoid depending on unsupported selectors or modern layout features such as grid, flexbox-only structure, filters, backdrop blur, pseudo-element-critical content, or CSS variables.
- When adapting the reference, preserve the dark header plus light body structure unless there is a documented reason to change it.
- Always test generated emails in major clients before shipping, with Outlook and Gmail treated as required checks.

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
