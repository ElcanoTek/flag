# Typography & Font Licensing

Canonical policy for which typeface a product may ship, and why. This file is the
source of truth when `AGENT_GUIDE.md`, `TOKENS.md`, or any older document appears
to say otherwise.

## The two faces

Elcano ships **exactly two typefaces**, in every product, on every surface.

| Role | Face | Licence | Loads |
|---|---|---|---|
| UI · body · headings | **Nebula Sans** | SIL OFL 1.1 | `fonts/fonts.css` |
| Code · logs · tabular output | **Hack** | MIT (+ Bitstream Vera) | `fonts/fonts.css` |

One sheet declares both. There is no per-product choice to make, no tier to look
up, and no third face to reach for. If you are adding a typeface, you are doing
something this policy does not permit — see "Adding a face" below.

**Nebula Sans** — © 2024 Nebula Entertainment & Broadcasting LLC, with Reserved
Font Name "Nebula". Based on Source Sans, © 2010–2024 Adobe, with Reserved Font
Name "Source". Licensed under the SIL Open Font License 1.1
([`fonts/nebula-sans/OFL.txt`](fonts/nebula-sans/OFL.txt)). Six weights and true
italics upstream; Flag ships four weights and two italics (see below).
<https://www.nebulasans.com/>

**Hack** — © 2018 Source Foundry Authors under the MIT License, incorporating
Bitstream Vera Sans Mono (© 2003 Bitstream Inc., Bitstream Vera License, Reserved
Font Names "Bitstream" and "Vera") and public-domain DejaVu work
([`fonts/hack/LICENSE.md`](fonts/hack/LICENSE.md)). Designed for source code, with
hand-groomed glyphs and optical balancing at small sizes.
<https://sourcefoundry.org/hack/>

Both licences permit redistribution, bundling with software under any licence, and
embedding. Both require that the licence text travel with the binaries.

## Why there are no longer tiers

This file used to define a two-tier system: **Dubai** for internal-only tools and
**IBM Plex Sans** for anything public. That existed for exactly one reason — Dubai
is proprietary (© 2017 Dubai Executive Council, distributed by Monotype under an
end-user licence). Elcano held a right to *use* it and no right to *sublicense*
it, so shipping the binaries in a repo carrying an outbound licence (MIT in fleet,
BSL 1.1 in explorer) would have purported to grant rights Elcano does not hold.
The tier was a licensing firewall wearing the costume of a design decision.

Nebula Sans and Hack are both freely redistributable, so the firewall has nothing
left to separate. Every product — MIT, BSL 1.1, or internal-and-never-published —
loads the same sheet and renders in the same two faces. That is the point: the
tiering was the source of the inconsistency this policy now forbids.

Retired in the same pass, and **not** to be reintroduced:

| Face | Was | Why it is gone |
|---|---|---|
| Dubai | internal brand face | Proprietary. Cannot ship in a licensed repo. |
| IBM Plex Sans | public brand face | Superseded by Nebula Sans. |
| IBM Plex Mono | neutral mono | Superseded by Hack. |
| Share Tech Mono | MOC retro code face | Superseded by Hack. |
| VT323 | MOC retro chrome face | Superseded by Hack. |

The Share Tech Mono + VT323 pairing was a deliberate retro language for
MOC-heritage log and task-tracker components, not an accident. It is retired
anyway: two mono faces on one surface is the inconsistency, and Hack reads better
at the sizes those components actually use. `--font-code-ui` still exists as a
token so that product CSS keeps resolving, but it now points at Hack, same as
`--font-code`.

## How selection works

`tokens/design-tokens.css` never names a family. It resolves one through an
indirection:

```css
--font-heading: var(--font-brand, "Nebula Sans"), "Segoe UI", system-ui, -apple-system, sans-serif;
--font-body:    var(--font-brand, "Nebula Sans"), "Segoe UI", system-ui, -apple-system, sans-serif;
--font-code:    var(--font-code-brand, "Hack"), ui-monospace, "SF Mono", "Consolas", monospace;
--font-code-ui: var(--font-code-ui-brand, "Hack"), ui-monospace, "SF Mono", "Consolas", monospace;
```

`fonts/fonts.css` sets `--font-brand`, `--font-code-brand` and
`--font-code-ui-brand`. Two consequences worth knowing:

- **Import order does not matter.** The token sheet only ever *reads* those
  variables, so the font sheet wins whether it is linked before or after.
- **Forgetting the sheet degrades, it does not substitute.** The fallbacks name
  the same two faces, so an omission falls through to a system stack rather than
  silently rendering in some other brand face. The symptom is "this looks like
  Segoe UI", which is the bug you want — visible, and not a licence problem.

Product CSS uses `var(--font-heading)` / `var(--font-body)` / `var(--font-code)`
and **never** references a family name directly.

## Adding the font sheet to a product

```html
<link rel="stylesheet" href="/path/to/fonts/fonts.css" />
<link rel="stylesheet" href="/path/to/tokens/design-tokens.css" />
```

Copy the whole face directories, licence files included — `fonts/nebula-sans/`
carries `OFL.txt` and `fonts/hack/` carries `LICENSE.md`. Do not copy the
`.woff2` files without them; both licences require it.

### Numbers in columns need `tabular-nums`

**Nebula Sans has proportional figures by default.** This is the single most
likely way a product regresses after adopting it, so it is a rule, not a tip:

> Any number that is read down a column — a table cell, a KPI value, a
> right-aligned total, a duration, a timestamp, a phone number, a price — must
> set `font-variant-numeric: tabular-nums`.

The digit advances are not close to uniform. Measured from
`nebula-sans/NebulaSans-400.woff2` at `unitsPerEm` 1000:

| digit | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| advance | 610 | **407** | 611 | 605 | 608 | 600 | 621 | 600 | **625** | 619 |

`1` is 407 units against `8` at 625 — a **53% spread**. A column of figures
without `tnum` visibly wanders. IBM Plex Sans, which most products replaced, had
uniform digit widths by default, so **this is a regression introduced by the
swap, not a pre-existing condition** — the alignment worked before and stops
working after, which is exactly the kind of change that ships unnoticed.

Nebula Sans does ship the feature (`tnum`, alongside `pnum`, `lnum`, `onum` and
`frac`), so the fix is CSS only:

```css
/* Base layer: a new numeric column can never land ragged by omission. */
table { font-variant-numeric: tabular-nums; }

/* Plus every numeric readout that is not in a table. */
.kpi-value, .stat-number { font-variant-numeric: tabular-nums; }
```

Do **not** set it globally on `body`. Proportional figures are correct in running
prose — that is what they are for — and tabular figures there leave gappy holes
around `1`. Apply it where numbers are columnar and nowhere else.

Hack needs none of this: it is monospaced, every glyph at a uniform 0.602em, so
anything already rendering through `--font-code` is aligned by construction.

Verify by measuring, not by eye — render two equal-length strings of `1`s and
`8`s in the same element and compare their widths:

```js
const w = s => { const e = document.createElement('span');
  const cs = getComputedStyle(el);
  e.style.font = cs.font; e.style.fontVariantNumeric = cs.fontVariantNumeric;
  e.style.whiteSpace = 'pre'; e.textContent = s;
  document.body.append(e); const r = e.getBoundingClientRect().width;
  e.remove(); return r; };
console.log(w('111111'), w('888888'));   // near-equal once tnum is applied
```

**Assert near-equality, not equality.** Nebula Sans's tabular figures are *not*
one uniform width — the `.tf` glyphs measure 600–607 units, with `5` the outlier
at 600 and `4`/`8` at 607:

| digit | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| `tnum` advance | 605 | 606 | 606 | 605 | 607 | **600** | 605 | 606 | 607 | 606 |

That is a 1.17% spread — max deviation 0.007em, about **0.11px at 16px**, against
0.218em before. Invisible in practice and a ~31× improvement, but real: it is
bit-identical at 13/26/52/104px, so it is the font's own metrics and not
rasterizer rounding. A test asserting exact equality will fail. Allow a
sub-pixel tolerance (0.5px is comfortable) and describe the result as near-exact
rather than claiming the columns match perfectly.

**And the residual grows with weight**, so a bold numeric readout is the worst
case, not the 400-weight figure above:

| weight | narrowest | widest | spread | at 16px |
|---|---|---|---|---|
| 400 | 600 (`5`) | 607 (`4`) | 7 units | ~0.11px |
| 500 | 606 (`5`) | 615 (`4`) | 9 units | ~0.14px |
| 600 | 616 (`5`) | 629 (`4`) | 13 units | ~0.21px |
| 700 | 626 (`5`) | 643 (`0`) | 17 units | ~0.27px |

`five.tf` is the narrowest glyph at every weight. So a bold KPI value drifts about
2.4× as much as body-weight text — still sub-pixel at ordinary sizes, but it is
why a bold readout measures ~13× better than proportional where a regular one
measures ~32×. If a display-size bold figure ever needs to align exactly, the fix
is re-spacing the binary upstream, not more CSS.

### Weights

Flag ships the four weights that have real faces, plus true italics at 400 and
700:

| Token | Weight | Faces |
|---|---|---|
| `--font-weight-regular` | 400 | roman + italic |
| `--font-weight-medium` | 500 | roman |
| `--font-weight-semibold` | 600 | roman |
| `--font-weight-bold` | 700 | roman + italic |

Nebula Sans also has 300 and 900 upstream; Flag does not ship them, because
nothing in the system calls for them and every shipped face is a file every
product pays for. Asking for a weight with no face gets you a **synthetic**
one — the browser smears the nearest neighbour — which looks approximately right
in review and wrong on a retina display. Same for italics at 500/600. If you need
one, add the real face here rather than styling around it.

### Font files must be complete, not subset

The `.woff2` files here are complete builds: **950** codepoints for Nebula Sans
(Latin-1, Latin Extended-A, Greek, Cyrillic) and **1548** for Hack. Do not
replace them with a narrower subset to save bytes.

A subset that covers only Latin-1 fails silently: the glyph is missing, the
browser substitutes a system font for that character alone, and a name renders in
two typefaces mid-word. `Łódź`, `Erdős`, `Škoda`, and Turkish/Romanian/Czech brand
and publisher names all land in Latin Extended-A. Explorer shipped exactly this
subset and nobody noticed for months.

This is a live trap for Hack in particular: the upstream package ships
`hack-*-subset.woff2` alongside the full files, and the subset build drops to 386
codepoints with **no Greek or Cyrillic at all**. Flag vendors the full files. If
you re-vendor, verify coverage:

```sh
python3 -c "from fontTools.ttLib import TTFont; \
  print(len(set(TTFont('fonts/nebula-sans/NebulaSans-400.woff2').getBestCmap())))"  # expect 950
python3 -c "from fontTools.ttLib import TTFont; \
  print(len(set(TTFont('fonts/hack/hack-regular.woff2').getBestCmap())))"           # expect 1548
```

## HTML email is a deliberate exception

`email-safe.html` names its stack inline as
`'Nebula Sans','Segoe UI',Arial,sans-serif` rather than reading a token. That is
correct and intentional, not drift:

- Email clients do not reliably support `@font-face` — Outlook's Word renderer
  ignores it and Gmail strips it — so there is no way to *load* Nebula Sans in an
  email. Naming it first means recipients who happen to have it installed get it,
  and everyone else falls through to a system face.
- Email clients also strip `<style>` blocks and do not support CSS custom
  properties, so `var(--font-body)` would resolve to nothing at all.

`email-safe.html` is the source of truth; `preview/email-safe.html` is a synced
copy. Change the source, then run `sh design-system/sync-email-preview.sh` —
`check-email-template.sh` fails the build if the two drift.

## Adding a face

Don't. The system is two faces, and "we need a third" has been the first step of
every drift this policy has had to undo — Geist in manifest, JetBrains Mono and
General Sans and Manrope in home, Inter in half a dozen places, each individually
reasonable and collectively the reason nothing matched.

If a real need survives that: it goes here first, with a licence file and a
recorded reason, and it goes into `fonts/fonts.css` — never into a product's own
stylesheet, and never from a CDN.

## Rules

- **Never** name a font family in product CSS, in `tokens/design-tokens.css`, or
  in `tokens/design-tokens.json`. Families belong in exactly one place:
  `fonts/fonts.css`.
- **Never** load a font from Google Fonts or any other CDN. It leaks user IPs to
  a third party, breaks in the fleet sandbox (no egress), and puts the rendered
  brand outside our control. Self-host from `fonts/`.
- **Never** copy a `.woff2`/`.woff`/`.ttf` without its licence file.
- **Never** swap in a subset build — see the coverage note above.
- **Never** reintroduce Dubai, IBM Plex, Share Tech Mono, or VT323.
- Flag itself is MIT-licensed — see the root [`LICENSE`](../LICENSE) — so its
  tokens, icons, and logos may be vendored into any product, fleet and explorer
  included. The fonts keep their own licences above.
