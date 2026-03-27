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
- Type scale is tokenized in `rem` (Title `1.75rem`, Subtitle `1.125rem`, Body `0.75rem-0.875rem`).
- Do not introduce arbitrary values like `0.8125rem` radius or `0.98rem` body text outside token scale.
- Keep border/radius/shadow values on token scale only.
- Light mode is canonical and must use canonical theme tokens (`body.theme-light` override model in token CSS).
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
- Default theme uses `:root` tokens.
- Light theme uses `body.theme-light` token overrides from `tokens/design-tokens.css`.
- Do not define per-component ad hoc light-mode values in product CSS.
- If a theme value is missing, add it to token files first.

## Component Defaults
- Buttons: `primary`, `secondary`, `ghost`, `danger`.
- Interactive controls must define explicit `hover`, `active`, and `focus-visible` states.
- Inputs: `2.5rem` min height, `radius-md`, token border/focus styles.
- Include full input coverage: text, search, password, email, number, tel, url, textarea, select, date, time, datetime-local, file.
- Number input must use Explorer-style stepper (`.number-input`, `.number-input__field`, `.number-input__btn`) where increment/decrement controls are needed.
- Date picker must use Explorer-themed classes (`.custom-datepicker` and themed `.flatpickr-*` styles when Flatpickr is used).
- File upload must use Lens/MOC dropzone structure (`.file-upload-dropzone`, `.dropzone-content`, `.file-list`).
- Accordion disclosure should use Home-style plus/minus summary indicator.
- Single-file selection lists should use Lens custom radio file selector pattern.
- Checkbox controls should use the shared design-system checkbox pattern (custom box + visible focus ring).
- Tables: sticky headers optional, row hover subtle, status badges use semantic tokens.
- Clickable action cards must use Home-style featured structure (`featured-head`, kicker, title, description) and explicit selected state (accent border/top accent/elevation).
- Do not implement clickable action cards without both explicit `selected` and `focus-visible` states.
- Use full task status badge set where applicable: pending, scheduled, assigned, leased, running, analyzing, success, error, cancelled.
- For recipient selection in task forms, use MOC-style email selection pills (`chips-container`, `chip chip-email`, `chip-delete`).
- App header must use the common Home-style pattern (brand mark + `Elcano Internal` eyebrow + page title + right-side utility actions).
- Modals: surface container, max-width tokens, explicit close button and escape key.
- Empty/Loading/Error: always include heading, explanatory body text, and next action.
- Common icon glyphs must come from `icons/core-icons.svg` (`download`, `trash`, `logout`, `paperclip`, etc.).
- Logos must come from `design-system/logos/` and follow `LOGOS.md` usage mapping.

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
- Mixed font systems within one screen.
- Invisible focus states.
- Gradient-heavy controls for every element (reserve gradients for hero/high-emphasis surfaces).
