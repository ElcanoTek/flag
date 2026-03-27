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

## Accessibility Baseline
- All icon-only controls require `aria-label`.
- Form controls must have labels and error association.
- Color contrast must be accessible for text and state indicators.
- Keyboard interactions:
  - modals: trap focus and close on escape
  - menus/dropdowns: keyboard navigation
  - custom controls: proper role and state attributes
  - chip-style controls: Enter/Space support when using `role="button"`
  - delete/remove affordances: keyboard focusable and screen-reader labeled

Dynamic status messaging:
- Loading/progress text should use a polite live region (`aria-live="polite"`) when content changes dynamically.
