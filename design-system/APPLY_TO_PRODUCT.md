# Apply to Another Product

Use this guide to adopt the Elcano Design System in another repo (for example `lens`, `explorer`, or a new UI).

## 1) Import Tokens First

Import canonical token CSS before product styles.

```html
<link rel="stylesheet" href="/path/to/design-tokens.css" />
```

Do not start component work until tokens are available.

## 2) Enable Theme Model

Default theme uses `:root` token values.

Light theme uses `body.theme-light` token overrides from `tokens/design-tokens.css`.

Example toggle:

```js
document.body.classList.toggle("theme-light")
```

## 3) Use Semantic Tokens in Product CSS

```css
.page {
  background: var(--gradient-bg-home-signature);
  color: var(--color-text-primary);
}

.panel {
  background: var(--gradient-surface-panel);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
}
```

## 4) Use Canonical Icon Sprite

```html
<button class="icon-action" type="button" aria-label="Delete">
  <svg class="icon" aria-hidden="true"><use href="../icons/core-icons.svg#trash"></use></svg>
</button>
```

## 5) Implement Component Contracts

Use `COMPONENTS.md` class/state contracts directly.

Examples:
- buttons: `.btn btn-primary|btn-secondary|btn-ghost|btn-danger`
- action cards: `.featured-link` + selected/disabled contracts
- chips: `.chip chip-email` + keyboard-accessible delete control

## 6) Required Interaction and A11y

Every interactive control must implement:
- `:hover`
- `:focus-visible` using `var(--focus-ring)`
- `:active`
- `:disabled` (when applicable)

Accessibility requirements:
- `aria-label` for icon-only controls
- explicit label/input association
- keyboard support for custom `role="button"` controls

## 7) Common Mistakes to Avoid

- Using hardcoded hex values instead of token variables.
- Using px one-offs instead of token scale (`var(--space-*)`, `var(--radius-*)`).
- Mixing non-Dubai fonts with system UI.
- Creating local light-mode values instead of token overrides.
- Missing focus-visible state on custom controls.

## 8) Migration Order (Recommended)

1. tokens and typography
2. buttons/inputs/badges/cards
3. complex components (dropzone, datepicker, chips)
4. final accessibility and parity verification
