# Gradients and Backgrounds

This document defines approved gradient and background options and when to use them.

## Canonical Gradient Tokens

Use only these gradient tokens for production UIs.

Theme note:
- These gradient token names are stable across themes.
- Light mode uses canonical `body.theme-light` token overrides in `tokens/design-tokens.css`.

### App Shell Backgrounds
- `--gradient-bg-home-signature`
  - **Default and enforced shell background across products**.
- `--gradient-bg-product-standard`
  - Reserved fallback token (do not use by default).
- `--gradient-bg-ops-console`
  - Reserved exception token for specialized dense operations views.

### Surface Backgrounds
- `--gradient-surface-panel`
  - Use: primary cards and section panels.
- `--gradient-surface-card`
  - Use: feature cards and prominent grouped containers.
- `--gradient-surface-elevated`
  - Use: elevated layers (modal panel, sticky detail panes, high-emphasis cards).

### Action and State Gradients
- `--gradient-action-primary` for primary buttons.
- `--gradient-action-success` for success state actions only.
- `--gradient-action-disabled` for disabled/coming-soon actions only.

## Usage Rules

## 1) One Shell Gradient Per Screen
- Use `--gradient-bg-home-signature` at page/root level for all normal product screens.
- Do not blend multiple shell gradient families on the same screen.
- Any use of reserved shell gradients requires explicit design approval.

## 2) Surface Gradients Must Be Hierarchical
- Normal card: `surface-panel` or `surface-card`.
- Elevated card/modal: `surface-elevated`.
- Keep border and shadow tokens in sync with gradient depth.

## 3) Limit Visual Noise
- Avoid combining heavy glow + strong gradient + patterned overlay on every layer.
- Use decorative overlays only at shell level or hero sections.

## 4) Preserve Readability
- Text contrast must remain high against all gradient stops.
- In data-dense views, prefer `ops-console` shell plus calmer panel gradients.

## 5) Motion and Hover
- Hover can slightly shift border and elevation.
- Avoid dramatic animated gradient transitions for standard controls.

## Default Policy
- All repos use `--gradient-bg-home-signature` by default.
- Reserved tokens (`product-standard`, `ops-console`) are exception-only.

## Quick Example

```css
body {
  background: var(--gradient-bg-home-signature);
}

.panel {
  background: var(--gradient-surface-panel);
}

.btn-primary {
  background: var(--gradient-action-primary);
}
```
