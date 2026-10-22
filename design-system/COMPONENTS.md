# Component System

This spec standardizes shared components used across Lens, Explorer, Home, MOC, and Victoria Voice.

Implementation note:
- `components/components.css` implements the classes in this file, in plain
  CSS that reads tokens only. It is the vendorable component layer for
  server-rendered (Tier A) products: vendor it next to the tokens and fonts
  and use the markup below. The preview loads a byte-identical copy
  (`preview/components.css`, refreshed by `sync-preview.sh`), so what the
  preview shows is what products get; `preview/styles.css` holds only the
  preview page's own layout.
- It is safe next to third-party markup. Rules on bare elements are limited
  to what is harmless for any instance: `box-sizing` on `*`, the link color on
  `a`, `font: inherit` on form controls, tabular figures on `table`. The
  text-field shell reaches only text-like inputs (never checkbox, radio,
  range, color, file, button-type or hidden inputs), single selects and
  textareas; native appearance is removed only where Flag draws a
  replacement; labels, tables and cells are styled only inside `.field` and
  `.table-wrap`. `make check` enforces this, and the preview shows unclassed
  native controls keeping their browser rendering.
- Examples in this file are the markup `preview/index.html` uses.
- Keep class names and state contracts aligned with these examples for deterministic implementation.
- React (Tier B) products implement the same specs in their own components,
  reading the same tokens.

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
- Fill: `--gradient-action-fill` (dark) or a solid `--color-primary-fill`
  (light); label `--color-on-primary-fill`; hover `--gradient-action-fill-hover`
  / `--color-primary-hover`. Never a label on the raw `--color-primary` or
  `--gradient-action-primary`: white on `#7272AB` is 4.46:1, just under AA.
  See "Foreground on a saturated fill" below.

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
- Hover never lowers label contrast: no `filter: brightness()` or `opacity`
  fade on a filled button; move to the `-hover` fill instead.

### Foreground on a saturated fill
An element filled with a brand or status color needs a foreground chosen for
that fill, in both themes:

| Fill | Foreground |
|---|---|
| `--color-primary-fill` (hover `--color-primary-fill-hover`) | `--color-on-primary-fill` |
| `--gradient-action-fill` (hover `--gradient-action-fill-hover`) | `--color-on-primary-fill` |
| `--color-accent-strong` | `--color-on-accent-strong` |
| `--color-success` | `--color-on-success` |

`--color-text-primary` is the foreground for ordinary surfaces; on a filled
control it is the common mistake. The raw `--color-primary` is for things
with nothing painted on them (an active bar, a checkbox accent, tints,
borders). `scripts/check_tokens.py` measures every pair above, in both themes
and at every point of the gradients.

### Button and pill shapes
Shape tells a reader what can be pressed. Every text button uses
`--radius-md`. Full pills (`--radius-pill`) are for things that are not text
buttons: status badges, removable chips, segmented tracks, switch tracks,
avatars, count bubbles, round icon-only buttons and progress bars.

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
- Label always visible; helper and validation text below control
  (`.field-hint`, `.field-error`, `.field-warning`; tie them to the control
  with `aria-describedby`).
- Error state: `aria-invalid="true"` on the control (danger border) plus a
  `.field-error` message; warning: `.is-warning` on the control plus
  `.field-warning`. Disabled fields use the native `disabled` attribute.

Production baseline requirements:
- Number controls must use the canonical `number-input` stepper pattern (minus button, centered value, plus button, focus-within ring). A disabled stepper disables its field and buttons and marks the wrapper `.is-disabled`.
- Date and datetime controls must use the canonical `custom-datepicker` treatment (left-aligned value, right icon affordance, themed popover classes).
- File attachment controls must use the canonical dropzone pattern with drag-over state, browse action, and file queue list. An upload area that cannot take files is `.file-upload-dropzone.is-disabled` (or `aria-disabled="true"`) with its browse button disabled.

## Dropdowns
- Match input styling and radius.
- Selected/active options use `color.accent` tone.

## Segmented Control
- Use for a choice between 2-4 mutually exclusive options (theme, schedule
  mode, list/week view). One look everywhere: `.seg` / `.seg-option`, a pill
  track with the selected option on `--color-primary-fill` /
  `--color-on-primary-fill`; unselected options are `--color-text-muted` and
  turn `--color-text-primary` on hover.
- Selection is read from the ARIA state the control already uses:
  `aria-pressed` (button group, `role="group"` + `aria-label`),
  `aria-checked` (radiogroup) or `aria-selected` (tablist). Behavior stays
  with each caller; only the look is shared.
- `.seg--md` is the form-field size, for a segmented control that is the
  field itself.
- Focus: a 2px `--color-accent` outline outside the option, where it meets
  the page at 3:1 or more in both themes.
- Not for underlined page tabs, filter chips with counts, or choice cards.

```html
<div class="seg" role="group" aria-label="Calendar view">
  <button class="seg-option" type="button" aria-pressed="true">List</button>
  <button class="seg-option" type="button" aria-pressed="false">Week</button>
  <button class="seg-option" type="button" aria-pressed="false">Month</button>
</div>
```

## Date Pickers
- Tokenized shell, no third-party default styles left un-themed.
- Trigger/focus states must match input field behavior.
- Date range fields must use same spacing and validation treatments as text/select fields.

Theme contract:
- Input uses `.custom-datepicker` spacing and right-side icon affordance.
- Flatpickr-compatible classes (`.flatpickr-calendar`, `.flatpickr-day`, `.flatpickr-weekday`) must be themed to token colors.
- Selected date state uses `--gradient-action-fill` with `--color-on-primary-fill`.
- Light-theme clarification: selected day uses solid `--color-primary-fill` with `--color-on-primary-fill` text.
- Keyboard focus (`:focus-visible`) on a day is an inset 2px ring, never just a color change. Days sit edge to edge, so the ring is inset and takes the color that holds 3:1 on that day's fill: `--focus-ring-day` (`--color-accent`) on a plain, hovered or today day, `--focus-ring-day-on-range` (`--color-on-accent-strong`) on an in-range day, and `--focus-ring-day-on-fill` (`--color-on-primary-fill`) on a selected or range-end day. These rules come after every day-state rule so they win at equal specificity.

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
  - drag-over (`.file-upload-dropzone.is-dragover`)
  - uploading (`.file-item.uploading`, with `.file-item-progress` / `.file-item-percent`)
  - uploaded (`.file-item.uploaded`)
  - error (`.file-item.error`)
- Terminal rows say what happened in a `.file-item-status` caption
  ("Uploaded", "Too large"); color alone never carries the state.
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
- Disabled: the native `disabled` radio plus `.is-disabled` on the row (muted
  ring and dot, disabled text, not-allowed cursor, no row hover).

## Checkbox
- Use one shared checkbox style across all products.
- Required behavior:
  - visible checkmark on checked state
  - visible focus ring on keyboard focus
  - proper label hit area
  - disabled styling where applicable (`.ds-checkbox-input:disabled`: faded box, disabled text color, not-allowed cursor)
- Keep checkbox checked styling separate from focus styling (focus ring appears on keyboard focus only).
- Required structure contract:
  - visually hidden checkbox input (`.ds-checkbox-input`) immediately before its label
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
- Markup: a `<dialog>` opened with `showModal()`, or an element with
  `role="dialog"`, `aria-modal="true"` and `aria-labelledby` pointing at the
  title. Move focus into it on open, keep Tab inside it while open, and
  return focus to the control that opened it on close. The close control is
  a `<button type="button">` with an `aria-label` ("Close") when it shows
  only an icon.
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
- Wrap a data table in `.table-wrap` (scroll container, border, radius);
  the table component's width, padding, borders and header style apply
  inside it. Any table gets tabular figures.
- The wrapper scrolls sideways on narrow screens, so keyboard users must be
  able to reach and scroll it (WCAG 2.1.1): give it `tabindex="0"`,
  `role="region"` and an `aria-label` that names the table (it is announced
  when focus lands there). Header cells take `scope="col"`.

```html
<div class="table-wrap" tabindex="0" role="region" aria-label="Task status table (scrolls horizontally)">
  <table>
    <thead><tr><th scope="col">ID</th><th scope="col">Name</th><th scope="col">Status</th></tr></thead>
    <tbody>
      <tr><td>T-1023</td><td>Daily Optimization</td><td><span class="badge badge-success">success</span></td></tr>
    </tbody>
  </table>
</div>
```
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
- The code well is `--color-surface-inset` (not `--color-overlay-strong`,
  which is the modal scrim and reads as a muddy band in light).
- Syntax highlighting uses the `--color-syntax-*` tokens (keyword, string,
  number, comment, function, builtin, operator, punctuation); each holds
  4.5:1 in a well on every surface in both themes. A scrollable `<pre>` gets
  `tabindex="0"` and an `aria-label` so keyboard users can scroll it.
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
  <pre class="tool-call-code" tabindex="0" aria-label="run_python code"><code class="language-python">print("hello")</code></pre>
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
- The icon and title styling show the state only visually: hide the icon
  from assistive tech (`aria-hidden="true"`) and say the state in a
  `.sr-only` span ("Done:", "In progress:", "To do:").

Example:

```html
<div class="task-tracker-container" role="group" aria-label="Task tracker">
  <div class="task-tracker-cmd">Command: <strong>RECONCILE DELIVERY REPORT</strong></div>
  <div class="task-tracker-list">
    <div class="task-tracker-item status-done"><span class="tt-icon" aria-hidden="true">&#10003;</span><span class="sr-only">Done:</span><span class="tt-id">[1]</span><span class="tt-title">Validate file schema</span></div>
    <div class="task-tracker-item status-inprogress"><span class="tt-icon" aria-hidden="true">&#8635;</span><span class="sr-only">In progress:</span><span class="tt-id">[2]</span><span class="tt-title">Aggregate publisher metrics</span></div>
    <div class="task-tracker-item status-todo"><span class="tt-icon" aria-hidden="true">&#9675;</span><span class="sr-only">To do:</span><span class="tt-id">[3]</span><span class="tt-title">Write QA summary</span></div>
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
- `.spinner` draws its arc in `--color-link` on a faint `--color-overlay-soft`
  track (4.6:1 arc against track, 5:1 against the surface; the old
  `--color-primary` arc on `--color-border-strong` was 1.67:1); inside a primary
  button (`.btn-primary .spinner`) the arc takes `--color-on-primary-fill` and
  the track `--color-primary-fill-hover`, since a primary arc on the primary
  fill is invisible (1.01:1). Under `prefers-reduced-motion` it stays a static
  ring.
- Upload progress fills use `--color-link` (3:1+ on the track in both themes).
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
- Pill: `chip chip-email` with selectable state (`selected`). The pill is a
  plain container holding two sibling buttons: `chip-toggle`
  (`aria-pressed`) and `chip-delete`. Do not make the pill itself a
  `role="button"` around the delete button: a control inside a control is
  unreachable for assistive technology (axe `nested-interactive`).
- Remove affordance: small inline `x` control (`chip-delete`) for custom/saved entries.
- Interaction rules:
  - click pill toggles selection
  - Enter/Space on the focused `chip-toggle` toggles selection (native button behavior)
  - click delete removes pill
  - delete affordance must be keyboard and screen-reader accessible
  - custom email input can add new pills

Theme behavior:
- Chips must consume semantic tokens for default, selected, hover, and focus-visible states in both dark and light themes.

Example:

```html
<div class="chips-container" role="group" aria-label="Email recipients">
  <span class="chip chip-email selected" data-email="ads@example.com">
    <button class="chip-toggle" type="button" aria-pressed="true">ads@example.com</button>
    <button class="chip-delete" type="button" aria-label="Remove recipient ads@example.com">x</button>
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

## Connection Picker

The pieces of the chat Tools picker (the composer wrench popover and the tool
library modal). Each is general enough for any searchable, toggleable list.
Every color is a token from `tokens/design-tokens.css` ("Connection picker
components" block); light-mode values live there too.

### Switch
- Disabled (`:disabled` / `aria-disabled="true"`): 50% and not-allowed,
  though a row that cannot be switched should show a status icon instead.
- `button.switch[role="switch"][aria-checked]`, 30x18 (`.switch--lg` 38x22).
- Track: `--color-switch-track-on` when checked, else `--color-switch-track-off`.
  The off track must reach 3:1 against the surface and under the knob, so
  both themes use a mid gray rather than the design's faint track.
- Hover: a 3px `--color-pill-hover-bg` halo. Pressed: the track dims (92%).
- Knob: `--color-switch-knob` with `--shadow-switch-knob` (none in dark; a
  soft drop in light), 14px
  (16px large), 2px inset (3px large),
  slides 12px (16px large) with `--transition-base`.
- Accessible name is the thing it switches (`aria-label="Index Exchange"`).
- A row that cannot be switched shows a status icon instead (`lock`,
  `alert-circle`, `alert-triangle`), never a disabled switch.

### Compact Search Field
- Wrapper `.search-compact` with a leading `search` icon (15px,
  `--color-text-subtle`) and an optional clear button (`close`, 12px).
- Field 34px (36px in a rail), `--color-bg` fill, 1px
  `--color-selected-border`, `--radius-sm`, 0.875rem text; focus border
  `--color-accent`, plus `--focus-ring-picker` on `:focus-visible`.
- The popover's field is focused on open; Escape clears it first, then closes.

### Small Pill Button
- `.pill-btn`, 22-24px high, `--radius-pill`, 1px `--color-pill-border`,
  transparent fill, 0.75rem `--color-text-secondary`.
- Hover (enabled pills only): `--color-pill-hover-bg` fill, `--color-text-primary`.
- Pressed: `--color-selected-bg` fill and `--color-selected-border` (the icon
  button too).
- A pill whose action would change nothing is `aria-disabled="true"` with its
  text and border at 40% (color-mix, not `opacity`, so a focus ring on it
  stays full strength), not natively disabled, so focus does not drop. `aria-disabled`
  does not stop a click or Enter/Space on a native button: the handler must
  return early while it is set.

### Status Kicker
- `.kicker` + `.kicker--ok|--warn|--deny`: `--font-code`, 0.625rem, weight
  700, letter-spacing 0.08em, uppercase.
- Colors `--color-state-ok|warn|deny` (at least 4.5:1 on every picker
  surface in both themes; the light values are darker than the design's for
  that reason). Labels: ALWAYS ON, NEEDS SETUP,
  UNAVAILABLE. Status dots (7px circles) use the same three tokens, plus
  `--color-accent` (on) and `--color-text-subtle` (off).

### Group Header
- `.group-header`: `--font-code`, 0.6875rem, letter-spacing 0.12em,
  uppercase, `--color-text-subtle`; an optional right-aligned count at 0.75rem.
- Static: no collapse affordance.

### Match Highlight
- `mark.match`: `--color-match-bg` fill, `--color-text-primary`, 3px radius,
  no padding, so highlighted text does not shift.

### State Panels
- `.state-panel--ok|--warn|--deny`: 1px border and fill from
  `--color-panel-<state>-border` / `--color-panel-<state>-bg`,
  `--radius-md`, 0.625rem 0.875rem padding, 0.8125rem body text.
- One short sentence; at most one link (`external-link` icon). Links in the
  picker (Set up, Open library, panel links) use `--color-link`, and keep it
  on hover and focus (underline instead of a color change). A link inside a
  sentence (the state panel's) is underlined at rest too: color alone does
  not distinguish it from the surrounding text (WCAG 1.4.1).

### Popover and Modal Surfaces
- Popover: 21.75rem wide, `max-width: 100%` on narrow screens;
  `--color-surface-2`, 1px `--color-selected-border`,
  `--radius-lg`, `--shadow-popover`. Rows 64px with 2-line descriptions
  (`--color-text-subtle`); the active row is `--color-selected-bg` with an
  inset 1px `--color-row-active-border` ring (at least 3:1 on the popover),
  and its description/meta step up to `--color-text-muted` (text-subtle is
  4.2:1 on that tint). A dimmed (unavailable) row keeps readable text: its
  status icon carries the state and its name steps down to
  `--color-text-secondary` at weight 500. Never fade row text with
  `opacity`.
- Modal: `--color-surface-1`, 1px `--color-selected-border`, `--radius-xl`,
  `--shadow-popover`, header icon in a `--color-icon-tile` square
  (`--color-accent` glyph). Filter rail on `--color-rail-bg`; the selected
  filter uses the active-row treatment.
- Scrim: `.scrim`, `--color-scrim` with a 3px backdrop blur.
- Divider lines inside both: `--color-divider`.
- Count badge on the trigger: `--color-accent-strong` fill,
  `--color-on-accent-strong` digits, pill, 0.6rem.

## Do / Don't
- Do use one canonical component variant per intent.
- Do use status badges consistently across tables.
- Do reuse the canonical upload dropzone pattern defined in this system.
- Don't mix wildly different button typography in the same screen.
- Don't ship un-themed third-party UI defaults.
