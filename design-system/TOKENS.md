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

Use `rem` as the canonical unit (not hard-coded `px`) for type sizing.

Core scale:

| Role | Token | Size | Line Height | Weight | Approx px at 16px root |
|---|---|---|---|---|---|
| Display | `font.size.display` | `clamp(2rem, 1.75rem + 0.8vw, 2.5rem)` | `1.15` | `700` | `32-40px` |
| Title | `font.size.title` | `1.75rem` | `1.2143` | `700` | `28px` |
| Subtitle | `font.size.subtitle` | `1.125rem` | `1.3334` | `700` | `18px` |
| Body Large | `font.size.bodyLarge` | `0.875rem` | `1.4286` | `400` | `14px` |
| Body Base | `font.size.body` | `0.8125rem` | `1.3847` | `400` | `13px` |
| Caption | `font.size.caption` | `0.75rem` | `1.3334` | `400` | `12px` |
| Overline | `font.size.overline` | `0.6875rem` | `1.2728` | `700` | `11px` |

PowerPoint baseline mapping (for compatibility with existing slide conventions):
- `Title 28px` -> `1.75rem`
- `Subtitle 18px` -> `1.125rem`
- `Body 12-14px` -> `0.75rem` to `0.875rem`

Hierarchy usage:
- One Title per page region.
- Subtitles for section starts and modal titles.
- Body Base (`0.8125rem`) default for controls, tables, and cards.
- Caption (`0.75rem`) only for helper, caption, and metadata.

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
- Dark theme: default `:root` values.
- Light theme: `body.theme-light` overrides in `tokens/design-tokens.css`.

Rules:
- Do not define ad hoc per-component theme values in product styles.
- If a light/dark value is missing, add it to token files first.
