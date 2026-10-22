# Interaction and Accessibility Rules

## State Rules

Every interactive control must define all of:
- `:hover`
- `:focus-visible`
- `:active`
- `:disabled` (where applicable)

### Hover
- Interactive controls: subtle visual delta only (slight lift or stronger border/fill).
- Avoid large positional movement in data-heavy interfaces.

### Focus
- Use `2px` visible ring + `2px` offset.
- Use `var(--focus-ring)` token.
- Focus must remain more prominent than hover.

### Active
- Reduce elevation and slightly darken fill.

### Disabled
- Opacity ~`0.5` and `cursor: not-allowed`.
- Remove hover transforms/glows.

### Loading
- Preserve button width to avoid layout shift.
- Use spinner + loading text when operation exceeds instant response.

### Cursor
- `pointer` for clickable controls.
- `not-allowed` for disabled controls.
- No fake pointer on non-interactive elements.

## Motion
- Standard transition: `140ms` to `200ms` ease.
- Use meaningful animation only:
  - mount/reveal for cards/rows
  - progress/loader motion
  - modal enter/exit
- Respect `prefers-reduced-motion: reduce`.

## Contrast
- Text, including placeholder-free labels, badges and links: at least 4.5:1
  against what it actually sits on (a tint over a surface, a fill, every point
  of a gradient), in both themes.
- Non-text that conveys state (focus rings, switch tracks, the active-row
  ring, input borders that are the only affordance): at least 3:1.
- A label on a brand or status fill uses that fill's foreground token, never
  `--color-text-primary`: see COMPONENTS.md "Foreground on a saturated fill".
- Never reach contrast by eye and never lower it with `opacity` on text
  (dimmed rows, faded hovers). If a state needs to look quieter, step to a
  quieter token that still passes.
- The token palette is measured by `scripts/check_tokens.py` on every PR, and
  `scripts/check_refs.py` fails when `components.css` lacks a documented
  class, an interaction state, a reduced-motion override, or a token override
  for a vendored (flatpickr) color. `make audit` renders the preview and
  checks what is painted: axe WCAG 2 A/AA, computed text contrast (over
  gradients too), visible focus on every control, in both themes at 1440 and
  390, with the pickers open.
- Third-party widgets (flatpickr) are themed part by part, every sub-part
  included (range days, time inputs, steppers, week numbers, the pointer
  triangle): a vendor default color that survives is a bug in dark mode.

## Accessibility Baseline
- All icon-only controls require `aria-label`.
- Form controls must have labels and error association.
- Color contrast must be accessible for text and state indicators.
- Keyboard interactions:
  - modals: trap focus and close on escape
  - menus/dropdowns: keyboard navigation
  - custom controls: proper role and state attributes
  - chip-style controls: a real `<button>` for each action (toggle, delete);
    never an interactive control nested inside another
  - scrollable regions (wide tables, code blocks): focusable (`tabindex="0"`)
    with an accessible name
  - delete/remove affordances: keyboard focusable and screen-reader labeled

Dynamic status messaging:
- Loading/progress text should use a polite live region (`aria-live="polite"`) when content changes dynamically.
