# Component System

This spec standardizes shared components used across Lens, Explorer, Home, MOC, and Victoria Voice.

## Logos and Logo Usage
- Use monochrome SVG mark in product header.
- Minimum clear space: `8px` all sides.
- Do not apply random glow/filter values outside tokenized shadows.

## Icons and Icon Style
- Use stroke icons, `1.75` to `2` stroke width, rounded caps.
- Default icon size: `16px` in controls, `20px` in standalone action buttons.
- Icon-only buttons require visible tooltip/title and `aria-label`.

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
- Text input, password, email, number, textarea, select.
- Height: min `40px`; radius: `radius-md`.
- Label always visible; helper and validation text below control.
- Error state uses `color.danger`; warning uses `color.warning`.

## Dropdowns
- Match input styling and radius.
- Selected/active options use `color.accent` tone.

## Date Pickers
- Tokenized shell, no third-party default styles left un-themed.
- Trigger/focus states must match input field behavior.

## Modals
- Surface: `surface.1`; border `strong`; shadow `lg`.
- Must include: title, close affordance, escape key close, backdrop close policy.
- Actions aligned right on desktop; stacked on narrow screens.

## Cards
- Base: `surface.1`, border standard, radius `lg`, shadow `sm`.
- Interactive card hover: subtle lift and border strengthen.

## Tables and List Rows
- Head row: uppercase optional, but consistent across app.
- Row hover allowed for clickable rows only.
- Status columns should use standardized status badge tokens.

## Navigation Patterns
- Topbar with product title + single primary context action area.
- Section navigation uses tabs or segmented buttons, not ad hoc card toggles unless justified.

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

## Do / Don't
- Do use one canonical component variant per intent.
- Do use status badges consistently across tables.
- Do reuse upload dropzone pattern from Lens/MOC.
- Don't mix wildly different button typography in the same screen.
- Don't ship un-themed third-party UI defaults.
