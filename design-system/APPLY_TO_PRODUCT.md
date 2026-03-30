# Apply to Another Product

Use this guide to port the canonical Flag design system behavior into another Elcano app (`lens`, `explorer`, `home`, `moc`, or new products).

## Canonical Theme Contract (Do Not Change)

- Root selector: `html[data-theme="light"]` or `html[data-theme="dark"]`
- Preference storage key: `flag-theme-preference`
- Default mode: `system` (`prefers-color-scheme`)
- Explicit user preference (`light`/`dark`) persists and overrides system changes
- Shared iconography for theme toggle: `sun` and `moon` from `icons/core-icons.svg`

If a product needs additional behavior, extend this contract. Do not replace it with product-specific theme logic.

## 1) Copy Foundations First

Copy or import these sources before product component work:
- `tokens/design-tokens.css`
- `tokens/design-tokens.json`
- `icons/core-icons.svg`

Import token CSS first:

```html
<link rel="stylesheet" href="/path/to/design-tokens.css" />
```

## 2) Wire Theme in App Shell

Apply theme on initial load before main UI render when possible:

```js
var root = document.documentElement;
var key = "flag-theme-preference";
var media = window.matchMedia("(prefers-color-scheme: dark)");
var stored = window.localStorage.getItem(key);
var effectiveTheme = stored === "light" || stored === "dark"
  ? stored
  : (media.matches ? "dark" : "light");

root.setAttribute("data-theme", effectiveTheme);
```

Then add a listener for system theme changes that only runs while preference is unset/`system`.

## 3) Add Shared Sun/Moon Toggle

Use the canonical accessible toggle structure:

```html
<button id="toggleTheme" class="btn btn-secondary theme-toggle" type="button" aria-label="Switch to light mode" aria-pressed="true">
  <span class="theme-toggle__icon-wrap" aria-hidden="true">
    <svg class="icon-inline theme-toggle__icon theme-toggle__icon--sun" aria-hidden="true"><use href="../icons/core-icons.svg#sun"></use></svg>
    <svg class="icon-inline theme-toggle__icon theme-toggle__icon--moon" aria-hidden="true"><use href="../icons/core-icons.svg#moon"></use></svg>
  </span>
  <span class="theme-toggle__text">Dark mode</span>
</button>
```

Required behavior:
- click toggles between `light` and `dark`
- updates `aria-label` to describe next action
- updates `aria-pressed` to reflect dark mode state
- updates visible text/icon state

## 4) Consume Semantic Tokens in Product CSS

Do not write product-local theme color values.

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

## 5) Keep Accessibility + Persistence Intact

- Icon-only controls require `aria-label`.
- Decorative SVGs remain `aria-hidden="true"`.
- Keep keyboard behavior and `:focus-visible` (`var(--focus-ring)`) on custom controls.
- If using a live region, announce theme changes when users toggle manually.
- Persist only explicit user choice; do not persist inferred system value as explicit choice.

## 6) What to Configure

- Path aliases/import paths for tokens and icons in your app.
- Placement of the theme toggle in app shell/header.
- Optional wiring into app state/store (the root `data-theme` value remains the source of applied theme).

## 7) What Not to Change

- Do not replace `html[data-theme]` with ad hoc selectors.
- Do not rename `flag-theme-preference` per product unless there is a hard requirement.
- Do not swap in custom sun/moon artwork when the shared icon sprite is available.
- Do not add per-component local light/dark overrides when token overrides already exist.

## 8) Recommended Migration Order

1. Import tokens/icons and apply root `data-theme` selector contract.
2. Add theme controller (system default + persisted preference + system-change sync).
3. Add shared theme toggle and verify accessibility attributes.
4. Migrate component styles to semantic tokens only.
5. Validate visual parity and interaction/accessibility behavior in both themes.
