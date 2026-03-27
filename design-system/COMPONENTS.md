# Component System

This spec standardizes shared components used across Lens, Explorer, Home, MOC, and Victoria Voice.

## Logos and Logo Usage
- Approved logo assets and rules are defined in `LOGOS.md`.
- Use the correct mark for the correct context (global brand vs product brand).
- Minimum clear space: `0.5rem` all sides.
- Preserve aspect ratio; do not recolor, stretch, rotate, or add effects.

## Icons and Icon Style
- Use stroke icons, `1.75` to `2` stroke width, rounded caps.
- Default icon size: `1rem` in controls, `1.25rem` in standalone action buttons.
- Icon-only buttons require visible tooltip/title and `aria-label`.
- Canonical icon set and names live in `ICONS.md` and `icons/core-icons.svg`.

## Buttons

### Primary
- Purpose: strongest positive action (`Submit`, `Start`, `Save`).
- Fill: `color.primary`; text: `color.text.primary`.

### Secondary
- Purpose: alternative actions.
- Surface: `color.surface.2`; border: `color.border`.

### Tertiary/Ghost
- Purpose: low-emphasis actions in dense UI.
- Transparent or low-contrast fill; must keep visible focus ring.

### Danger
- Purpose: destructive actions (`Delete`, `Cancel Task`).
- Use `color.danger` semantics only.

States for all button variants:
- Default, hover, focus-visible, active, disabled, loading.

## Form Inputs
- Canonical input types:
  - text
  - search
  - password (+ optional reveal toggle)
  - email
  - number
  - tel
  - url
  - textarea
  - select
  - date
  - time
  - datetime-local
  - file attachment
- Height: min `2.5rem`; radius: `radius-md`.
- Label always visible; helper and validation text below control.
- Error state uses `color.danger`; warning uses `color.warning`.

Production baseline requirements:
- Number controls must use the Explorer `number-input` stepper pattern (minus button, centered value, plus button, focus-within ring).
- Date and datetime controls must use the Explorer `custom-datepicker` treatment (left-aligned value, right icon affordance, themed popover classes).
- File attachment controls must use the Lens/MOC dropzone pattern with drag-over state, browse action, and file queue list.

## Dropdowns
- Match input styling and radius.
- Selected/active options use `color.accent` tone.

## Date Pickers
- Tokenized shell, no third-party default styles left un-themed.
- Trigger/focus states must match input field behavior.
- Date range fields must use same spacing and validation treatments as text/select fields.

Theme contract (Explorer-aligned):
- Input uses `.custom-datepicker` spacing and right-side icon affordance.
- Flatpickr-compatible classes (`.flatpickr-calendar`, `.flatpickr-day`, `.flatpickr-weekday`) must be themed to token colors.
- Selected date state uses primary gradient and maintains accessible contrast.

## File Upload Dropzone
- Canonical pattern source: Lens + MOC.
- Required parts:
  - `.file-upload-dropzone`
  - `.dropzone-content`
  - `.dropzone-browse-btn`
  - `.file-list` and `.file-item`
- Required states:
  - default
  - hover
  - drag-over
  - uploading
  - uploaded
  - error
- Required metadata:
  - file name
  - file size
  - progress indicator (when uploading)

## Accordion / Disclosure
- Canonical pattern source: Home.
- Use semantic `<details>/<summary>` structure where feasible.
- Summary indicator uses `+` when collapsed and `-` when expanded.
- Use for grouped secondary content, tool directories, and progressive disclosure.

## Custom File Radio Select
- Canonical pattern source: Lens "Select existing input file" list.
- Use for single-choice file selection before an action.
- Required elements:
  - list row container
  - custom circular radio control
  - truncated file name
  - optional action icons (download/delete)
- Hover and focus-within states must be visible on the row.

## Checkbox
- Use one shared checkbox style across all products.
- Required behavior:
  - visible checkmark on checked state
  - visible focus ring on keyboard focus
  - proper label hit area
  - disabled styling where applicable

## Modals
- Surface: `surface.1`; border `strong`; shadow `lg`.
- Must include: title, close affordance, escape key close, backdrop close policy.
- Actions aligned right on desktop; stacked on narrow screens.

## Cards
- Base: `surface.1`, border standard, radius `lg`, shadow `sm`.
- Interactive card hover: subtle lift and border strengthen.

Clickable action card standard (Home-modeled, required for card-based navigation actions):
- Required structure:
  - `featured-head` block with `featured-kicker` + title
  - support/meta description text
- Required states:
  - default
  - hover
  - focus-visible
  - selected
  - disabled
- Selected state must be explicit (accent border + top accent treatment + elevation change) and keyboard-discernible.
- Visual treatment should follow Home-style featured cards using design-system tokenized colors, spacing, and typography.

## Tables and List Rows
- Head row: uppercase optional, but consistent across app.
- Row hover allowed for clickable rows only.
- Status columns should use standardized status badge tokens.

## Navigation Patterns
- Topbar with product title + single primary context action area.
- Section navigation uses tabs or segmented buttons, not ad hoc card toggles unless justified.

## Common App Header
- Canonical pattern source: Home topbar (`Elcano Internal` + page title).
- Structure:
  - left: brand mark + suite label (eyebrow) + current page title
  - right: utility and session actions (`Settings`, `Log out`, profile)
- Use the same header pattern across all products for cohesion.
- Keep eyebrow text `Elcano Internal` for internal suite apps unless formally rebranded.

## Tabs
- Active tab: accent border/fill and clear selected state.
- Inactive tabs: low-emphasis surface with hover indication.

## Empty States
- Include icon (optional), title, explanation, and next action.
- No empty state should be plain "No data" text only.

## Loaders
- Spinner size: `12px` inline, `32px` panel-level.
- Use semantic loading text for long operations.

## Error States
- Inline field error for validation.
- Banner/toast/modal error for process-level failures.
- Always include corrective guidance.

## Badges/Pills/Chips
- Use pill radius.
- Status and priority colors must map to semantic token set.
- Chips in multi-select/email patterns should support remove affordance.

Email selection pills (MOC task modal pattern):
- Use this when selecting one or more recipient emails.
- Container: `chips-container` style region with wrap and spacing.
- Pill: `chip chip-email` with selectable state (`selected`).
- Remove affordance: small inline `x` control (`chip-delete`) for custom/saved entries.
- Interaction rules:
  - click pill toggles selection
  - click delete removes pill
  - custom email input can add new pills

Task status badge set (required for MOC-aligned workflows):
- `pending`
- `scheduled`
- `assigned`
- `leased`
- `running`
- `analyzing`
- `success`
- `error`
- `cancelled`

Node status badge set (recommended):
- `idle`
- `busy`
- `offline`
- `error`

## Do / Don't
- Do use one canonical component variant per intent.
- Do use status badges consistently across tables.
- Do reuse upload dropzone pattern from Lens/MOC.
- Don't mix wildly different button typography in the same screen.
- Don't ship un-themed third-party UI defaults.
