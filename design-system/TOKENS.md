# Foundations and Tokens

All values below are canonical for Elcano products.

Canonical token files:
- Runtime CSS: `tokens/design-tokens.css`
- Machine-readable JSON: `tokens/design-tokens.json`

When docs/examples conflict, token files win.

## 1) Color System

Palette roots observed across products:
- Deep Purple: `#1A0B1E`
- Payne's Gray: `#586F7C`
- Glaucous: `#7272AB`
- White: `#FFFFFF`
- Black: `#000000`

Canonical semantic tokens:

| Token | Value | Purpose | Rules |
|---|---|---|---|
| `color.primary` | `#7272AB` | Primary CTA and key emphasis | Use only for primary actions and active states |
| `color.secondary` | `#586F7C` | Secondary controls and supportive accents | Never used as danger/success |
| `color.accent` | `#9DA7EF` | Highlights, focus, selected states | Use sparingly for emphasis |
| `color.bg` | `#1A0B1E` | App background base | Default shell background |
| `color.surface.1` | `#241B31` | Primary panel/card surface | Main content containers |
| `color.surface.2` | `#2F2741` | Elevated/interactive surface | Hovered cards, modal nesting |
| `color.border` | `rgba(114, 114, 171, 0.35)` | Standard border | Default border token |
| `color.text.primary` | `#FFFFFF` | High-emphasis text | Headings, key labels |
| `color.text.secondary` | `#D2D9DE` | Secondary text | Metadata, support copy |
| `color.text.muted` | `#BEB6CD` | Tertiary text | Placeholders and low-emphasis labels |
| `color.success` | `#50FA7B` | Positive state | Status/success messages only |
| `color.warning` | `#FFB86C` | Warning state | Caution messages only |
| `color.danger` | `#FF5555` | Error/destructive | Error and destructive actions only |
| `color.info` | `#8A8BC0` | Informational state | Neutral/informational badges |

Neutral utility tokens:
- `color.white` = `#FFFFFF`
- `color.black` = `#000000`

Default semantic usage clarifications:
- Links and email-address affordances default to `color.secondary`.
- Primary buttons in light theme use a solid `color.primary` fill with `color.white` text.
- Selected calendar days in light theme use a solid `color.primary` fill with `color.white` text.

Status mapping for task/node badges:

| Status | Foreground | Background | Border |
|---|---|---|---|
| `pending` | `color.text.secondary` | `rgba(88,111,124,0.18)` | `rgba(88,111,124,0.55)` |
| `scheduled` | `#E9DBB8` | `rgba(255,184,108,0.14)` | `rgba(255,184,108,0.55)` |
| `assigned` | `#D4DEFF` | `rgba(138,139,192,0.18)` | `rgba(138,139,192,0.55)` |
| `leased` | `#D4DEFF` | `rgba(138,139,192,0.14)` | `rgba(114,114,171,0.55)` |
| `running` | `#D4DEFF` | `rgba(114,114,171,0.2)` | `rgba(114,114,171,0.6)` |
| `analyzing` | `#D8E5FF` | `rgba(62,146,196,0.18)` | `rgba(62,146,196,0.52)` |
| `success` | `#CBFDD8` | `rgba(80,250,123,0.14)` | `rgba(80,250,123,0.6)` |
| `error` | `#FFD2D2` | `rgba(255,85,85,0.14)` | `rgba(255,85,85,0.6)` |
| `cancelled` | `#D2D9DE` | `rgba(88,111,124,0.2)` | `rgba(88,111,124,0.52)` |

## 2) Typography

Required family:
- Headlines/Subheadlines: `Dubai Bold`, weight `700`
- Body/UI: `Dubai Regular`, weight `400`

Dubai font files are self-hosted in `design-system/fonts/dubai/` and loaded via `design-system/fonts/dubai-fonts.css`.
Include this stylesheet before `design-tokens.css` in any product that needs to load Dubai locally:
```html
<link rel="stylesheet" href="/path/to/design-system/fonts/dubai-fonts.css" />
```
Font files provided: `DubaiW23-Regular.woff2`, `DubaiW23-Regular.ttf`, `DubaiW23-Bold.woff2`, `DubaiW23-Bold.ttf`.

Code-component typography (logs code display + task tracker only):
- `font.code` / `--font-code`: `Share Tech Mono`
- `font.codeUi` / `--font-code-ui`: `VT323`
- Font files are provided in `design-system/fonts/` and loaded via `design-system/fonts/code-fonts.css`.

Use `rem` as the canonical unit (not hard-coded `px`) for type sizing.

Core scale:

| Role | Token | Size | Line Height | Weight | Approx px at 16px root |
|---|---|---|---|---|---|
| Display | `font.size.display` | `clamp(2rem, 1.75rem + 0.8vw, 2.5rem)` | `1.15` | `700` | `32-40px` |
| Title | `font.size.title` | `1.75rem` | `1.2` | `700` | `28px` |
| Subtitle | `font.size.subtitle` | `1.125rem` | `1.3` | `700` | `18px` |
| Body Large | `font.size.bodyLarge` | `1.0625rem` | `1.5` | `400` | `17px` |
| Body Base | `font.size.body` | `1rem` | `1.5` | `400` | `16px` |
| Body Medium | `font.size.bodyMedium` | `0.9375rem` | `1.5` | `400` | `15px` |
| Caption | `font.size.caption` | `0.8125rem` | `1.4` | `400` | `13px` |
| Overline | `font.size.overline` | `0.75rem` | `1.4` | `700` | `12px` |

PowerPoint baseline mapping (for compatibility with existing slide conventions):
- `Title 28px` -> `1.75rem`
- `Subtitle 18px` -> `1.125rem`
- `Body 16-17px` -> `1rem` to `1.0625rem`
- `Caption 13px` -> `0.8125rem`

Hierarchy usage:
- One Title per page region.
- Subtitles for section starts and modal titles.
- Body Base (`1rem` / 16px) default for controls, tables, and cards. This size prevents iOS Safari auto-zoom on form inputs and aligns with Material 3 and Apple HIG body text norms.
- Body Large (`1.0625rem` / 17px) for emphasized body copy or long-form reading contexts.
- Caption (`0.8125rem` / 13px) only for helper, caption, and metadata.
- Overline (`0.75rem` / 12px) for uppercase labels and kickers. 12px is the conventional minimum for legibility.

Line height rationale:
- Headings (display, title): `1.15`-`1.2` for tight, compact headings.
- Subtitles: `1.3` for a moderate reading rhythm.
- Body and body-lg: `1.5` for comfortable paragraph reading and accessibility.
- Caption and overline: `1.4` for compact but legible secondary text.

## 3) Spacing, Radius, Borders, Shadows

Use `rem` spacing tokens. Numeric token scale:

| Token | Value | Approx px |
|---|---|---|
| `space.1` | `0.25rem` | `4px` |
| `space.2` | `0.5rem` | `8px` |
| `space.3` | `0.75rem` | `12px` |
| `space.4` | `1rem` | `16px` |
| `space.5` | `1.25rem` | `20px` |
| `space.6` | `1.5rem` | `24px` |
| `space.7` | `2rem` | `32px` |
| `space.8` | `2.5rem` | `40px` |
| `space.9` | `3rem` | `48px` |

Common spacing primitives:
- `space.controlInline = 0.75rem`
- `space.controlStack = 0.5rem`
- `space.cardPadding = 1.5rem`
- `space.sectionStack = 2rem`
- `space.pageGutter = 1.5rem`

Usage:
- Control vertical rhythm: `space.2` to `space.3`.
- Card internal padding: `space.4` to `space.6`.
- Section spacing: `space.6` to `space.7`.
- Page gutters: `space.pageGutter` desktop, `space.4` mobile.

Radius scale:
- `radius.sm = 0.5rem`
- `radius.md = 0.625rem`
- `radius.lg = 0.875rem`
- `radius.xl = 1.125rem`
- `radius.pill = 999rem`

Borders:
- Standard: `1px solid color.border`
- Strong: `1px solid rgba(114,114,171,0.55)`
- Dashed dropzone/empty: `2px dashed rgba(88,111,124,0.72)`

Shadows:
- `shadow.sm = 0 10px 24px rgba(0,0,0,0.28)`
- `shadow.md = 0 12px 24px rgba(0,0,0,0.34)`
- `shadow.lg = 0 22px 54px rgba(0,0,0,0.52)`

## 4) Sizing and Layout

Container widths:
- Default page max width: `72.5rem` (`1160px` at 16px root)
- Data-dense workspace max width: `87.5rem` (`1400px` at 16px root)

Control sizing:
- Inputs/selects/buttons min height: `2.5rem`
- Icon button: `2rem` to `2.25rem`

Responsive breakpoints:
- `sm`: `640px`
- `md`: `768px`
- `lg`: `1024px`
- `xl`: `1280px`

App shell:
- Header + main content + optional right panel/modal overlay.
- Keep one-column base below `md`; introduce side-by-side layouts at `lg`.

## 5) Gradients and Backgrounds

Use gradient tokens for shell and surfaces; do not create ad hoc gradients in product code.

Shell/background gradients:
- `gradient.background.homeSignature` (`--gradient-bg-home-signature`)
- `gradient.background.productStandard` (`--gradient-bg-product-standard`)
- `gradient.background.opsConsole` (`--gradient-bg-ops-console`)

Default policy:
- Use `gradient.background.homeSignature` across all repos.
- `productStandard` and `opsConsole` are reserved exception tokens.

Surface gradients:
- `gradient.surface.panel` (`--gradient-surface-panel`)
- `gradient.surface.card` (`--gradient-surface-card`)
- `gradient.surface.elevated` (`--gradient-surface-elevated`)

Action/state gradients:
- `gradient.action.primary` (`--gradient-action-primary`)
- `gradient.action.success` (`--gradient-action-success`)
- `gradient.action.disabled` (`--gradient-action-disabled`)

Usage reference and rationale are in `BACKGROUNDS.md`.

## 6) Theme Support

Theme behavior is canonical and token-based:
- Dark theme: `:root` values applied via `html[data-theme="dark"]` (or default when no explicit override).
- Light theme: `:root[data-theme="light"]` overrides in `tokens/design-tokens.css`.
- Theme preference storage key: `flag-theme-preference`.
- Default mode: `system` (`prefers-color-scheme`), with explicit user choice taking precedence when stored.

Rules:
- Do not define ad hoc per-component theme values in product styles.
- If a light/dark value is missing, add it to token files first.
- If a component needs a special light-theme override for contrast, document it in `COMPONENTS.md` and keep the value token-derived.
