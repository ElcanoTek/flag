# Foundations and Tokens

All values below are canonical for Elcano products.

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

## 2) Typography

Required family:
- Headlines/Subheadlines: `Dubai Bold`, weight `700`
- Body/UI: `Dubai Regular`, weight `400`

Type scale:
- Title: `28px`, line-height `34px`, weight `700`
- Subtitle: `18px`, line-height `24px`, weight `700`
- Body Large: `14px`, line-height `20px`, weight `400`
- Body Base: `13px`, line-height `18px`, weight `400`
- Body Small: `12px`, line-height `16px`, weight `400`

Hierarchy usage:
- One Title per page region.
- Subtitles for section starts and modal titles.
- Body 13px default for controls, tables, and cards.
- Body 12px only for helper, caption, and metadata.

## 3) Spacing, Radius, Borders, Shadows

Spacing scale (px): `4, 8, 12, 16, 20, 24, 32, 40, 48`.

Usage:
- Control vertical rhythm: `8` to `12`.
- Card internal padding: `16` or `24`.
- Section spacing: `24` to `32`.

Radius scale:
- `radius.sm = 8`
- `radius.md = 10`
- `radius.lg = 14`
- `radius.xl = 18`
- `radius.pill = 999`

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
- Default page max width: `1160px`
- Data-dense workspace max width: `1400px`

Control sizing:
- Inputs/selects/buttons min height: `40px`
- Icon button: `32px` to `36px`

Responsive breakpoints:
- `sm`: `640px`
- `md`: `768px`
- `lg`: `1024px`
- `xl`: `1280px`

App shell:
- Header + main content + optional right panel/modal overlay.
- Keep one-column base below `md`; introduce side-by-side layouts at `lg`.
