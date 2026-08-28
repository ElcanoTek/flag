# Component System

This spec standardizes shared components used across Lens, Explorer, Home, MOC, and Victoria Voice.

Implementation note:
- Examples in this file are based on real patterns in `preview/index.html` and `preview/styles.css`.
- Keep class names and state contracts aligned with these examples for deterministic implementation.

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

## Theme Toggle (Shared Control)
- Purpose: provide a single canonical control for switching between light and dark modes across Elcano products.
- Icon usage: use shared sprite icons `sun` and `moon` from `icons/core-icons.svg`; icons are decorative (`aria-hidden="true"`).
- Preferred shell placement: top-right of the shared `.page-header` / app header action row.
- Header behavior on mobile: theme toggle and other icon-only header actions stay in a single non-wrapping row aligned top-right.
- When paired with other icon-only header actions, theme toggle should use the same `icon-action` sizing contract (`2rem` square) rather than a wider text button.
- Visible text is optional. If the control is icon-only, keep `aria-label` and `aria-pressed` accurate.
- Root contract: toggle updates `html[data-theme]` (`light` or `dark`); components must react via token variables.
- Default behavior: if no explicit user preference exists, active theme follows `prefers-color-scheme`.
- Persistence behavior: explicit user selection is stored at `localStorage` key `flag-theme-preference`.
- System behavior: system theme changes auto-apply only while preference is unset/`system`.
- Accessibility requirements:
  - control keeps an explicit `aria-label` that describes next action (`Switch to dark mode` / `Switch to light mode`)
  - use `aria-pressed` to expose current dark-mode state
  - preserve keyboard activation and `focus-visible` treatment

Example:

```html
<button class="btn btn-secondary theme-toggle" type="button" aria-label="Switch to light mode" aria-pressed="true">
  <span class="theme-toggle__icon-wrap" aria-hidden="true">
    <svg class="icon-inline theme-toggle__icon theme-toggle__icon--sun" aria-hidden="true"><use href="../icons/core-icons.svg#sun"></use></svg>
    <svg class="icon-inline theme-toggle__icon theme-toggle__icon--moon" aria-hidden="true"><use href="../icons/core-icons.svg#moon"></use></svg>
  </span>
  <span class="theme-toggle__text">Dark mode</span>
</button>
```

## Buttons

Theme behavior:
- Button variants are theme-aware through canonical tokens; do not hardcode light/dark button values in component styles.
- Each variant must explicitly define `hover`, `active`, and `focus-visible` states.

### Primary
- Purpose: strongest positive action (`Submit`, `Start`, `Save`).
- Fill: `color.primary`; text: `color.text.primary`.
- Light-theme clarification: primary buttons use a solid `color.primary` fill with `color.white` text.

### Secondary
- Purpose: alternative actions.
- Surface: `color.surface.2`; border: `color.border`.

### Ghost
- Purpose: low-emphasis actions in dense UI.
- Transparent or low-contrast fill; must keep visible focus ring.

### Danger
- Purpose: destructive actions (`Delete`, `Cancel Task`).
- Use `color.danger` semantics only.

States for all button variants:
- Default, hover, focus-visible, active, disabled, loading.

Example:

```html
<button class="btn btn-primary" type="button">Primary</button>
<button class="btn btn-secondary" type="button">Secondary</button>
<button class="btn btn-ghost" type="button">Ghost</button>
<button class="btn btn-danger" type="button">Delete</button>
```

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
- Number controls must use the canonical `number-input` stepper pattern (minus button, centered value, plus button, focus-within ring).
- Date and datetime controls must use the canonical `custom-datepicker` treatment (left-aligned value, right icon affordance, themed popover classes).
- File attachment controls must use the canonical dropzone pattern with drag-over state, browse action, and file queue list.

## Dropdowns
- Match input styling and radius.
- Selected/active options use `color.accent` tone.

## Date Pickers
- Tokenized shell, no third-party default styles left un-themed.
- Trigger/focus states must match input field behavior.
- Date range fields must use same spacing and validation treatments as text/select fields.

Theme contract:
- Input uses `.custom-datepicker` spacing and right-side icon affordance.
- Flatpickr-compatible classes (`.flatpickr-calendar`, `.flatpickr-day`, `.flatpickr-weekday`) must be themed to token colors.
- Selected date state uses primary gradient and maintains accessible contrast.
- Light-theme clarification: selected day uses solid `color.primary` with `color.white` text.

Shared disclosure/search-panel spacing:
- When date filters and secondary search filters appear in the same disclosure block, keep visible spacing between the date range area, any add/remove controls, and the next filter group.
- Secondary filter groups may add spacing/padding, but should not introduce a new contrasting panel background unless that nested surface is intentionally part of the component spec.

## File Upload Dropzone
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
- Use semantic `<details>/<summary>` structure where feasible.
- Summary indicator uses `+` when collapsed and `-` when expanded.
- Use for grouped secondary content, tool directories, and progressive disclosure.
- When used for internal launchpads/resource hubs, prefer a stack of `.link-tile` entries with consistent meta copy length and icon alignment.

Example:

```html
<div class="ds-accordion">
  <details open>
    <summary>Trading and Supply</summary>
    <div class="links">
      <a class="link-tile" href="#">
        <span class="link-title">OpenX</span>
        <span class="link-meta">Manage deals within SSP workflows.</span>
      </a>
    </div>
  </details>
</div>
```

## Custom File Radio Select
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
- Keep checkbox checked styling separate from focus styling (focus ring appears on keyboard focus only).
- Required structure contract:
  - visually hidden checkbox input immediately before its label
  - label uses `.ds-checkbox`
  - visual box uses `.ds-checkbox__box`
  - label text uses `.ds-checkbox__label`
- Checkmark contract:
  - use a guaranteed-available checkmark asset or inline path inside `.ds-checkbox__box`
  - do not reference a sprite symbol name that is not present in `icons/core-icons.svg`
- Reuse the same checkbox pattern in filter popovers, settings lists, and dense forms; do not create alternate checkbox implementations per product.

## App Header
- Use the shared `.page-header` with `.ds-app-header` brand/actions anatomy as the default page-level header.
- Optional support copy (`header_intro`) may be omitted when the page already communicates purpose through surrounding UI.
- Login pages may reuse the same shared page header instead of introducing a separate hero/header pattern.

## Modals
- Surface: `surface.1`; border `strong`; shadow `lg`.
- Must include: title, close affordance, escape key close, backdrop close policy.
- Actions aligned right on desktop; stacked on narrow screens.

Modal action-grid variant:
- Use when a modal presents 2-4 mutually exclusive next-step destinations or workflow entry points.
- Required parts:
  - close action in top-right
  - kicker/eyebrow (optional)
  - title
  - support copy
  - grid of action tiles or buttons
- Action tiles may reuse `.link-tile` or a product-local modal option class, but must preserve standard hover/focus-visible behavior and accessible labeling.

## Cards
- Base: `surface.1`, border standard, radius `lg`, shadow `sm`.
- Interactive card hover: subtle lift and border strengthen.

Clickable action card standard (required for card-based navigation actions):
- Required structure:
  - `featured-head` block with `featured-kicker` + title
  - support/meta description text
- Required class mapping:
  - base: `.featured-link`
  - selected: `.is-selected` or `[aria-current="true"]`
  - disabled: `.is-disabled` or `[aria-disabled="true"]` and `tabindex="-1"`
- Required internal anatomy:
  - kicker: `.featured-kicker`
  - title: `h4`
  - description: `.description`
- Required states:
  - default
  - hover
  - focus-visible
  - selected
  - disabled
- Selected state must be explicit (accent border + top accent treatment + elevation change) and keyboard-discernible.
- Visual treatment must follow the canonical featured card structure using design-system tokenized colors, spacing, and typography.
- In launchpads, featured cards may optionally include an approved product/app icon when icon presence is consistent across the sibling set.

Example:

```html
<a class="card featured featured-link is-selected" href="#" aria-current="true">
  <div class="featured-head">
    <p class="featured-kicker">Operations</p>
    <h4>MOC</h4>
  </div>
  <p class="description">Manage active automation workflows.</p>
</a>
```

## App Iconography
- Use app/service icons in launchpads, resource directories, and modal action grids when they help users distinguish destinations quickly.
- Two approved icon container modes:
  - neutral service icon container for external/vendor destinations
  - branded/internal product icon container for first-party Elcano products
- Required structure for icon-bearing tiles:
  - wrapper tile (`.link-tile`, `.featured-link`, or modal action tile)
  - icon container (`.link-app-icon`)
  - icon image (`.link-app-icon__img`)
  - title/meta text aligned consistently beside or below the icon depending on tile density
- Recommended layout contract for dense directory tiles:
  - tile gets `.link-has-app-icon`
  - title/meta stack remains separate from the icon container
- Asset rules:
  - first-party Elcano product destinations use approved assets from `design-system/logos/`
  - external services use approved product-local service icons/favicons
  - if no approved service icon exists, fall back to `elcano-mark-primary.svg` until the correct asset is added
- Theme rules:
  - if an icon has theme-specific variants, switch source assets by theme
  - do not recolor icon artwork in CSS
  - branded/internal icon containers may use a richer gradient/background treatment than neutral service icon containers

## Link Tile
- Base use cases:
  - resource directories
  - launchpad sections
  - modal action grids
- Required anatomy:
  - `.link-title`
  - `.link-meta`
- Optional anatomy:
  - `.link-app-icon`
  - `.link-app-icon__img`
  - `.link-has-app-icon`
- Interaction rules:
  - full tile remains clickable
  - title and meta stay aligned regardless of icon presence
  - icon-bearing and icon-less tiles should not mix within the same tightly grouped directory unless intentionally staged

Example with app icon:

```html
<a class="link-tile link-has-app-icon" href="#">
  <span class="link-app-icon" aria-hidden="true">
    <img class="link-app-icon__img" src="../logos/explorer-favicon.svg" alt="" />
  </span>
  <span class="link-title">Explorer</span>
  <span class="link-meta">View reporting that keeps Victoria optimizations aligned.</span>
</a>
```

## Launchpad / Directory Pattern
- Use for internal home screens, resource hubs, and multi-product launch surfaces.
- Recommended composition:
  - shared `.page-header`
  - optional high-priority featured workflow cards
  - one or more accordion directory groups
  - docs/resources group that may include the live design-system link
  - optional modal action-grid for workflow entry choices
- Consistency rules:
  - icon usage should be systematic across sibling entries
  - first-party product destinations should use shared product marks where available
  - external vendor destinations should use approved service icons or the documented fallback

## Tables and List Rows
- Head row: uppercase optional, but consistent across app.
- Row hover allowed for clickable rows only.
- Status columns should use standardized status badge tokens.

## Logs Code Display and Task Tracker (MOC Baseline)
- This component set is canonical for logs UIs that render agent tool calls.
- Preserve MOC class contracts and structure for cross-product reuse.
- Typography: these components use the code face instead of the text face (`--font-heading`/`--font-body`):
  - code/content: `font.code` (`--font-code`, Hack stack)
  - command/terminal labels: `font.codeUi` (`--font-code-ui`, Hack stack)
  - Both tokens now resolve to Hack. They remain distinct so existing markup keeps
    working, but the two-face retro pairing (Share Tech Mono + VT323) is retired —
    see [`FONTS.md`](FONTS.md).
- Font sourcing requirement: self-host fonts and load `design-system/fonts/fonts.css` before component styles.

### Code Display Block
- Use this for code execution payloads (for example, `run_python` tool calls).
- Required classes:
  - `.tool-call-item`
  - `.tool-call-name`
  - `.tool-call-id`
  - `.tool-call-code`
  - `.tool-call-other-args` (optional)

Example:

```html
<div class="tool-call-item">
  <div class="tool-call-name"><strong>run_python</strong></div>
  <div class="tool-call-id">ID: <code>call_9f8a2ce1</code></div>
  <pre class="tool-call-code"><code class="language-python">print("hello")</code></pre>
  <div class="tool-call-other-args">Other arguments: <code>{"timeout": 45}</code></div>
</div>
```

### Task Tracker Block
- Use this for `task_tracker` tool call arguments and progress snapshots.
- Required classes:
  - `.task-tracker-container`
  - `.task-tracker-cmd`
  - `.task-tracker-list`
  - `.task-tracker-item`
  - `.tt-icon`, `.tt-id`, `.tt-title`
- Supported item state classes:
  - `.status-done`
  - `.status-inprogress`
  - `.status-todo`

Example:

```html
<div class="task-tracker-container" role="group" aria-label="Task tracker">
  <div class="task-tracker-cmd">Command: <strong>RECONCILE DELIVERY REPORT</strong></div>
  <div class="task-tracker-list">
    <div class="task-tracker-item status-done"><span class="tt-icon">&#10003;</span><span class="tt-id">[1]</span><span class="tt-title">Validate file schema</span></div>
    <div class="task-tracker-item status-inprogress"><span class="tt-icon">&#8635;</span><span class="tt-id">[2]</span><span class="tt-title">Aggregate publisher metrics</span></div>
    <div class="task-tracker-item status-todo"><span class="tt-icon">&#9675;</span><span class="tt-id">[3]</span><span class="tt-title">Write QA summary</span></div>
  </div>
</div>
```

## Navigation Patterns
- Topbar with product title + single primary context action area.
- Section navigation uses tabs or segmented buttons, not ad hoc card toggles unless justified.

## Common App Header
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

Email selection pills:
- Use this when selecting one or more recipient emails.
- Container: `chips-container` style region with wrap and spacing.
- Pill: `chip chip-email` with selectable state (`selected`).
- Remove affordance: small inline `x` control (`chip-delete`) for custom/saved entries.
- Interaction rules:
  - click pill toggles selection
  - Enter/Space toggles selection when pill is focused
  - click delete removes pill
  - delete affordance must be keyboard and screen-reader accessible
  - custom email input can add new pills

Theme behavior:
- Chips must consume semantic tokens for default, selected, hover, and focus-visible states in both dark and light themes.

Example:

```html
<div class="chips-container" role="group" aria-label="Email recipients">
  <span class="chip chip-email selected" data-email="ads@elcanotek.com" role="button" tabindex="0" aria-pressed="true" aria-label="Toggle recipient ads@elcanotek.com">
    ads@elcanotek.com
    <button class="chip-delete" type="button" aria-label="Remove recipient ads@elcanotek.com">x</button>
  </span>
</div>
```

Task status badge set:
- `pending`
- `scheduled`
- `assigned`
- `leased`
- `running`
- `analyzing`
- `success`
- `error`
- `cancelled`

| Status | CSS Class |
|---|---|
| pending | `.badge-pending` |
| scheduled | `.badge-scheduled` |
| assigned | `.badge-assigned` |
| leased | `.badge-leased` |
| running | `.badge-running` |
| analyzing | `.badge-analyzing` |
| success | `.badge-success` |
| warning | `.badge-warning` |
| error | `.badge-danger` |
| cancelled | `.badge-cancelled` |

Node status badge set (recommended):
- `idle`
- `busy`
- `offline`
- `error`

## Do / Don't
- Do use one canonical component variant per intent.
- Do use status badges consistently across tables.
- Do reuse the canonical upload dropzone pattern defined in this system.
- Don't mix wildly different button typography in the same screen.
- Don't ship un-themed third-party UI defaults.
