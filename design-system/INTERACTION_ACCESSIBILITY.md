# Interaction and Accessibility Rules

## State Rules

### Hover
- Interactive controls: subtle visual delta only (slight lift or stronger border/fill).
- Avoid large positional movement in data-heavy interfaces.

### Focus
- Use `2px` visible ring + `2px` offset.
- Focus ring color: `color.accent`.

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
