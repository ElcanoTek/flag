# Agent Implementation Guide

Use this when a prompt says: "Follow the design system in the flag repo."

## Hard Rules
- Use tokens from `tokens/design-tokens.css` or `tokens/design-tokens.json`; do not invent one-off colors/spacing.
- Typography is fixed:
  - Headlines and subheadlines: `Dubai Bold`.
  - Body/UI text: `Dubai Regular`.
- Type scale is tokenized in `rem`:
  - Title: `1.75rem`.
  - Subtitle: `1.125rem`.
  - Body: `0.75rem` to `0.875rem`.
- Do not hardcode font sizes in `px` except for hairline/border cases.
- Keep radius, border, and shadow values from token scales only.
- Use approved gradient/background tokens only; see `BACKGROUNDS.md`.
- Use only approved logo assets and contexts from `LOGOS.md`.
- Shell background default is `--gradient-bg-home-signature` across all repos unless an explicit exception is documented.
- Focus style must be visible and consistent (`2px` ring with offset).
- Primary actions must use the primary button variant.
- Danger actions must use danger semantic tokens; never repurpose primary color for destructive actions.

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

## Component Defaults
- Buttons: `primary`, `secondary`, `ghost`, `danger`.
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

## Disallowed Patterns
- External font/CDN dependencies for core UI styles.
- New ad hoc status colors.
- Mixed font systems within one screen.
- Invisible focus states.
- Gradient-heavy controls for every element (reserve gradients for hero/high-emphasis surfaces).
