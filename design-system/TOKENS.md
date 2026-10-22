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

| Token | Dark | Light | Purpose | Rules |
|---|---|---|---|---|
| `--color-primary` | `#7272AB` | `#7272AB` | Primary emphasis, active states | Never put a label on it; filled controls use `--color-primary-fill` |
| `--color-secondary` | `#586F7C` | `#586F7C` | Secondary controls and supportive accents | Never used as danger/success; light-theme link color |
| `--color-accent` | `#9DA7EF` | `#5A64B8` | Highlights, focus, selected states | Use sparingly; light value deepened from `#9DA7EF` (2.1:1) so focus rings and focus/hover borders reach 3:1 |
| `--color-bg` | `#1A0B1E` | `#F4F6FB` | App background base | Default shell background |
| `--color-surface-1` | `#241B31` | `#FFFFFF` | Primary panel/card surface | Main content containers |
| `--color-surface-2` | `#2F2741` | `#E9EEFC` | Elevated/interactive surface | Hovered cards, popovers, modal nesting |
| `--color-border` | `rgba(114, 114, 171, 0.35)` | `rgba(38, 55, 92, 0.2)` | Standard border | Default border token |
| `--color-text-primary` | `#FFFFFF` | `#141824` | High-emphasis text | Headings, key labels |
| `--color-text-secondary` | `#D2D9DE` | `#33415F` | Secondary text | Metadata, support copy |
| `--color-text-muted` | `#BEB6CD` | `#5C6A87` | Tertiary text | Placeholders and low-emphasis labels |
| `--color-link` | `#9DA7EF` | `#5F5F97` | Link text | Default link color; 4.5:1+ on every surface |
| `--color-success` | `#50FA7B` | `#1E7A3F` | Positive state | Status/success messages only |
| `--color-warning` | `#FF8847` | `#8F3E10` | Warning state | Caution messages only |
| `--color-danger` | `#FF5757` | `#B3261E` | Error/destructive | Error and destructive actions only |
| `--color-info` | `#8E8EC2` | `#4F5496` | Informational state | Neutral/informational badges |

Connection picker tokens (switch, compact search, pills, kickers, group
headers, match highlight, state panels, scrim; see COMPONENTS.md
"Connection Picker"). Dark values shown; light values in the token files.

| Token | Dark | Purpose |
|---|---|---|
| `color.picker.accentStrong` | `#5956D5` | Switch track (on), count badge fill |
| `color.picker.onAccentStrong` | `#EEF0FF` | Count badge digits (4.99:1 on the fill; the design's `#B9C0F2` is 3.2:1) |
| `color.picker.link` | `#9DA7EF` (light `#5F5F97`) | Links inside the picker |
| `color.picker.textSubtle` | `#9C96AE` | Row descriptions, group headers, counts (below `text.muted`) |
| `color.picker.divider` | `#3A3147` | Lines inside popovers and modals |
| `color.picker.selectedBg` / `selectedBorder` | `rgba(89,86,213,0.2)` / `rgba(157,167,239,0.4)` | Active row and selected filter fill; popover/modal border |
| `color.picker.rowActiveBorder` | `#9DA7EF` (light `#6262A0`) | Active row and selected filter ring (6.2:1 / 4.8:1 on the popover) |
| `color.picker.pillBorder` / `pillHoverBg` | `rgba(255,255,255,0.14)` / `rgba(255,255,255,0.06)` | Small pill button |
| `color.picker.switchTrackOff` / `switchKnob` | `#7A7392` / `#F4F5F9` (light `#80829E` / `#FFFFFF`); each off track is at least 3:1 on the popover and under the knob | Switch |
| `color.picker.matchBg` | `rgba(157,167,239,0.22)` | Search match highlight |
| `color.picker.stateOk` / `stateWarn` / `stateDeny` | `#4ECB8F` / `#E0A94A` / `#E08AA3` (light `#1B7950` / `#8E611E` / `#9C546A`, each ≥ 4.5:1) | Status kickers, dots and icons |
| `color.picker.panel{Ok,Warn,Deny}{Bg,Border}` | 12% fill / 30-32% border of the state color | State panels |
| `color.picker.iconTile` | `rgba(157,167,239,0.14)` | Modal header icon square |
| `color.picker.railBg` | `rgba(0,0,0,0.16)` | Modal filter rail |
| `color.picker.scrim` | `rgba(26,11,30,0.55)` | Modal backdrop (with a 3px blur) |
| `shadow.switchKnob` | `none` (light: `0 1px 2px rgba(26,11,30,0.28)`) | Switch knob lift in light mode |
| `shadow.focusRingPicker` | `--focus-ring` in both themes | Focus ring on picker fields, pills, switches and icon buttons. Light used a separate `#6262A0` ring while the base light ring was under 3:1; with the light accent deepened it inherits `--focus-ring`, and stays a token so product CSS keeps resolving |
| `shadow.popover` | `0 24px 60px -22px rgba(0,0,0,0.55)` | Popover and modal elevation |

Neutral utility tokens:
- `color.white` = `#FFFFFF`
- `color.black` = `#000000`

Default semantic usage clarifications:
- Links and email-address affordances use `--color-link`. Light-theme
  products may keep the long-standing `--color-secondary` (4.5:1+ there) with
  `--color-primary-hover` on hover; `--color-secondary` is not a dark-theme
  link color (2.7-3.6:1). A link inside running text is underlined, not told
  apart by color alone.
- Primary buttons and selected calendar days in light theme use a solid
  `--color-primary-fill` with `--color-on-primary-fill` text (see "Filled
  controls" below).

### Filled controls

White on `--color-primary` (`#7272AB`) is 4.46:1, just under WCAG AA. Every
filled control therefore paints its label on a measured fill:

| Token | Value | Use |
|---|---|---|
| `--color-primary-fill` | primary mixed 1% toward black (4.53:1 under white) | Filled buttons, selected chips/options, selected calendar day, segmented selection |
| `--color-primary-fill-hover` | primary mixed 11% toward black (5.4:1) | Hover of the above: hover only ever raises contrast |
| `--color-on-primary` / `--color-on-primary-fill` | `#FFFFFF` | The label on either fill (`--color-on-primary-fill` reads `--color-on-primary`) |
| `--color-secondary-fill` / `-hover` | secondary / 10% toward black | Far stop of the action gradient |
| `--gradient-action-fill` / `-hover` | primary-fill to secondary-fill (light: the hover stops) | Primary buttons in dark; the label holds 4.5:1 at every point of the blend |

`--color-primary` stays for things with nothing painted on them (an active
bar, a checkbox accent, tints, borders); `--gradient-action-primary` stays for
decoration. Neither carries a label. Upstreamed from fleet's measured fill
pair.

### Wells, syntax and focus

- `--color-surface-inset`: a recessed in-flow surface (code and output wells,
  preview toolbars, tool-result panels). Dark: the same black wash as
  `--color-overlay-strong`; light: a 4.5% slate tint, so a well inside a card
  stays near-white. `--color-overlay-strong` is the modal scrim only.
- `--color-syntax-{keyword,string,number,comment,function,builtin,operator,punctuation}`:
  code highlighting. Each holds 4.5:1 in an inset well over `--color-bg`,
  `--color-surface-1` and `--color-surface-2`, in both themes.
- `--focus-ring`: 2px of the page color, then 2px of `--color-accent`. The
  outer color reaches 3:1 against every surface in both themes (WCAG 1.4.11);
  in light that needed the deeper light accent (`#5A64B8`; it was `#9DA7EF`,
  2.1:1).

### Contrast is measured, not asserted

`scripts/check_tokens.py` (run by `make check` and CI) resolves the token
sheet the way a browser does, including `var()` and `color-mix()`, and
measures every text, badge, fill, gradient, switch and focus-ring pair above
in both themes. A token change that drops a pair below 4.5:1 (text) or 3:1
(non-text) fails the build.

Status mapping for task/node badges:

| Status | Foreground (dark / light) | Background (dark / light) | Border (dark / light) |
|---|---|---|---|
| `pending` | `#D3DDE6` / `#33415F` | `rgba(124, 140, 152, 0.2)` / `rgba(124, 140, 152, 0.18)` | `rgba(124, 140, 152, 0.6)` / `rgba(124, 140, 152, 0.42)` |
| `scheduled` | `#FFE4B8` / `#7A4A12` | `rgba(224, 171, 74, 0.18)` / `rgba(224, 171, 74, 0.24)` | `rgba(224, 171, 74, 0.62)` / `rgba(224, 171, 74, 0.54)` |
| `assigned` | `#CFE3FF` / `#1F3F87` | `rgba(90, 132, 255, 0.2)` / `rgba(90, 132, 255, 0.2)` | `rgba(90, 132, 255, 0.58)` / `rgba(90, 132, 255, 0.44)` |
| `leased` | `#E5D6FF` / `#5A2F8F` | `rgba(168, 119, 255, 0.2)` / `rgba(168, 119, 255, 0.18)` | `rgba(168, 119, 255, 0.58)` / `rgba(168, 119, 255, 0.42)` |
| `running` | `#C9F0FF` / `#0F5E78` | `rgba(47, 183, 220, 0.22)` / `rgba(47, 183, 220, 0.22)` | `rgba(47, 183, 220, 0.62)` / `rgba(47, 183, 220, 0.46)` |
| `analyzing` | `#D6DDFF` / `#3B3391` | `rgba(124, 107, 255, 0.22)` / `rgba(124, 107, 255, 0.2)` | `rgba(124, 107, 255, 0.62)` / `rgba(124, 107, 255, 0.44)` |
| `success` | `#CBFDD8` / `#1C5A33` | `rgba(80, 250, 123, 0.14)` / `rgba(80, 250, 123, 0.16)` | `rgba(80, 250, 123, 0.6)` / `rgba(80, 250, 123, 0.42)` |
| `warning` | `#FFD2A1` / `#8F3E10` | `rgba(255, 136, 71, 0.2)` / `rgba(255, 136, 71, 0.24)` | `rgba(255, 136, 71, 0.62)` / `rgba(255, 136, 71, 0.48)` |
| `error` | `#FFD2D2` / `#7C1F1F` | `rgba(255, 85, 85, 0.14)` / `rgba(255, 85, 85, 0.18)` | `rgba(255, 85, 85, 0.6)` / `rgba(255, 85, 85, 0.44)` |
| `cancelled` | `#C7CED4` / `#556074` | `rgba(108, 118, 130, 0.16)` / `rgba(108, 118, 130, 0.16)` | `rgba(108, 118, 130, 0.48)` / `rgba(108, 118, 130, 0.34)` |

Each `--color-status-<state>-{fg,bg,border}` triple is a badge: the
foreground holds 4.5:1 on its own tint over every surface, in both themes
(`scripts/check_tokens.py`).

## 2) Typography

Required roles:
- Headlines/Subheadlines: `--font-heading`, weight `700`
- Body/UI: `--font-body`, weight `400`

Both resolve through `--font-brand`, which `fonts/fonts.css` sets. There is
exactly one sheet and one pair of faces across every Elcano product — see
[`FONTS.md`](FONTS.md) for the full policy. Summary:

| Role | Face | Licence |
|---|---|---|
| Text — headings, body, UI | **Nebula Sans** | SIL OFL 1.1 |
| Code — logs, tabular output | **Hack** | MIT (+ Bitstream Vera) |

Both are freely redistributable, so the same sheet is correct for every product
regardless of its outbound licence. There is no tier to look up.

`design-tokens.css` names no face of its own. Its fallbacks name these same two
faces, so a product that forgets the sheet degrades to a system stack rather than
silently rendering in some other brand face. Import order between the font sheet
and `design-tokens.css` does not matter.

```html
<link rel="stylesheet" href="/path/to/design-system/fonts/fonts.css" />
<link rel="stylesheet" href="/path/to/design-system/tokens/design-tokens.css" />
```

Font files provided (copy the licence files with them — both licences require it):
- Nebula Sans — `fonts/nebula-sans/NebulaSans-{400,500,600,700}.woff2` plus true
  italics at `NebulaSans-{400,700}-italic.woff2` (+ `OFL.txt`).
- Hack — `fonts/hack/hack-{regular,bold,italic,bolditalic}.{woff2,woff}` (+ `LICENSE.md`).

Weights with a real face: `400` regular, `500` medium, `600` semibold, `700` bold.
Anything else is a synthetic smear — see [`FONTS.md`](FONTS.md) before asking for one.

Code typography:
- `font.code` / `--font-code`: `Hack`
- `font.codeUi` / `--font-code-ui`: `Hack`
- Both resolve to the same face. They stay distinct as tokens so product CSS reading
  `--font-code-ui` keeps working; the old two-face MOC retro language (Share Tech
  Mono for code, VT323 for task-tracker chrome) is retired.

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
