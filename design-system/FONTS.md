# Typography & Font Licensing

Canonical policy for which typeface a product may ship, and why. This file is the
source of truth when `AGENT_GUIDE.md`, `TOKENS.md`, or any older document appears
to say otherwise.

Flag ships two brand faces. They are **not interchangeable** — the choice is a
licensing decision, not a design preference.

## The tiers

| Product | Distribution | Licence | Brand face | Loads |
|---|---|---|---|---|
| **Manifest** | Internal only, never published | — (internal) | **Dubai** | `fonts/dubai-fonts.css` |
| **Fleet** | Open source, public | MIT | **IBM Plex Sans** | `fonts/ibm-plex-fonts.css` |
| **Explorer** | Source-available, public | BSL 1.1 | **IBM Plex Sans** | `fonts/ibm-plex-fonts.css` |
| Flag preview | Internal review surface | — (internal) | Dubai | `fonts/dubai-fonts.css` |
| Any new product | — | — | **IBM Plex Sans** unless it is internal-only | `fonts/ibm-plex-fonts.css` |

The default is IBM Plex Sans. Dubai is the exception, and it requires the product
to be internal-only.

## Why

**Dubai** is proprietary: © 2017 Dubai Executive Council, all rights reserved,
distributed by Monotype under an end-user licence. Elcano has a right to *use* it.
Elcano does **not** have a right to sublicense it. A repository that carries an
outbound licence — MIT in fleet, BSL 1.1 in explorer — and also ships the Dubai
binaries is, on its face, offering the world a licence to that font under those
terms. Elcano cannot grant that licence, so shipping the files there misstates
what the recipient is getting. See
[`fonts/dubai/LICENSE-NOTICE.md`](fonts/dubai/LICENSE-NOTICE.md).

**IBM Plex Sans** is © 2017 IBM Corp. under the SIL Open Font License 1.1. The OFL
explicitly permits redistribution, bundling with software under any licence, and
embedding — so it is safe in MIT, BSL, and internal products alike. Its one hard
requirement is that the licence text travels with the files:
[`fonts/ibm-plex-sans/OFL.txt`](fonts/ibm-plex-sans/OFL.txt) must be copied
wherever the `.woff2` files are copied.

**The code faces** are all SIL OFL 1.1 and carry no tier restriction — any product
may use any of them. Their notices are `fonts/OFL-ShareTechMono.txt`,
`fonts/OFL-VT323.txt` and `fonts/ibm-plex-mono/OFL.txt`, and the same
travel-with-the-files rule applies. There are two sanctioned options:

| Code language | Faces | Sheet | Used by |
|---|---|---|---|
| MOC retro baseline (default) | Share Tech Mono + VT323 | `fonts/code-fonts.css` | MOC-heritage log/task-tracker components |
| Neutral mono | IBM Plex Mono | `fonts/ibm-plex-mono-fonts.css` | fleet — developer-facing output, pairs with IBM Plex Sans |

The retro language is deliberate, not accidental, but it is not universal. A product
whose primary surface is dense developer output may load
`ibm-plex-mono-fonts.css`, which sets `--font-code-brand` /
`--font-code-ui-brand`. Loading a design-system sheet is the sanctioned way to make
that swap — self-hosting a repo-local copy is how explorer's IBM Plex ended up a
stale Latin-1 subset.

## How selection works

`tokens/design-tokens.css` does not name a brand face. It resolves one through an
indirection:

```css
--font-heading: var(--font-brand, "IBM Plex Sans"), "Segoe UI", system-ui, -apple-system, sans-serif;
--font-body:    var(--font-brand, "IBM Plex Sans"), "Segoe UI", system-ui, -apple-system, sans-serif;
```

Each font sheet sets `--font-brand` for itself: `ibm-plex-fonts.css` sets
`"IBM Plex Sans"`, `dubai-fonts.css` sets `"Dubai"`. Two consequences worth
knowing:

- **Import order does not matter.** The token sheet never assigns `--font-brand`,
  so whichever font sheet a product loads wins regardless of whether it is linked
  before or after `design-tokens.css`.
- **Forgetting to load a font sheet fails safe.** The fallback is the OFL face, so
  the failure mode of an omission is a licence-clean render, not a proprietary
  font reference in a public repo.

Product CSS keeps using `var(--font-heading)` / `var(--font-body)` and never
references a family name directly.

## Adding a font sheet to a product

```html
<!-- open source / source-available -->
<link rel="stylesheet" href="/path/to/fonts/ibm-plex-fonts.css" />
<link rel="stylesheet" href="/path/to/tokens/design-tokens.css" />
```

```html
<!-- internal only -->
<link rel="stylesheet" href="/path/to/fonts/dubai-fonts.css" />
<link rel="stylesheet" href="/path/to/tokens/design-tokens.css" />
```

Copy the whole face directory, licence file included: `fonts/ibm-plex-sans/` and
`fonts/ibm-plex-mono/` each carry `OFL.txt`; do not copy the `.woff2` files
without it.

### Font files must be complete, not subset

The `.woff2` files here are IBM's **complete** builds — 895 codepoints for Sans,
983 for Mono, covering Latin-1, Latin Extended-A/B, Greek and Cyrillic. Do not
replace them with a narrower subset to save bytes.

A subset that covers only Latin-1 fails silently: the glyph is missing, the browser
substitutes a system font for that character alone, and a name renders in two
typefaces mid-word. `Łódź`, `Erdős`, `Škoda`, and Turkish/Romanian/Czech brand and
publisher names all land in Latin Extended-A. Explorer shipped exactly this subset
and nobody noticed. If you regenerate these files, verify coverage:

```sh
python3 -c "from fontTools.ttLib import TTFont; \
  print(len(set(TTFont('IBMPlexSans-400.woff2').getBestCmap())))"   # expect ~895
```

## Rules

- **Never** hardcode `"Dubai"` in `tokens/design-tokens.css`, in
  `tokens/design-tokens.json`, or in any product stylesheet. It belongs in exactly
  one place: `fonts/dubai-fonts.css`.
- **Never** copy `fonts/dubai/*` into fleet, explorer, or any other public or
  source-available repository.
- **Never** copy an OFL `.woff2`/`.ttf` without its `OFL.txt` / `OFL-*.txt`.
- **Never** swap in a Latin-1 subset of a brand face — see the coverage note above.
- A new product defaults to IBM Plex Sans. Dubai requires confirming the product
  is internal-only and never published.
- Note that this repo itself is internal and proprietary — see the root
  [`LICENSE`](../LICENSE). Flag's tokens, icons, and logos are **not** licensed for
  redistribution in fleet or explorer either; that is tracked separately from the
  font question.
