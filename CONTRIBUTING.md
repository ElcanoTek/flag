# Contributing to Flag

Thanks for looking. Flag is the design system every Elcano product vendors, so
a change here reaches every product on its next sync. That makes most changes
easy and a few of them expensive; this page says which is which.

Read [`design-system/README.md`](design-system/README.md) for the doc map and
[`design-system/AGENT_GUIDE.md`](design-system/AGENT_GUIDE.md) for the rules
products follow.

## Licensing of contributions

Flag is released under the [MIT License](LICENSE) with ElcanoTek, Inc. as
copyright holder. Opening a pull request means you have the right to
contribute the change and agree to it being released under MIT. There is no
CLA. Third-party material (a font, an icon set, a vendored library) needs a
licence that permits redistribution, and its notice must travel with the files
(see how `fonts/` and the icon sprite do it).

## Setup

You need `make`, `sh`, `perl` and Python 3. There is no package manager and
nothing to install.

```bash
git clone https://github.com/ElcanoTek/flag.git
cd flag
make preview      # http://localhost:8765/preview/
make check        # everything CI runs
```

`make preview` serves `design-system/`, not `design-system/preview/`: the
preview reads `../tokens/`, `../fonts/`, `../icons/` and `../logos/`, exactly
like the live site at <https://flag-71q.pages.dev/> (Cloudflare Pages, which
publishes `preview/` with those four directories beside it on every push to
`main`).

## The checks

`make check` runs `scripts/check-all.sh`, which CI runs on every pull request:

| Check | What it guards |
|---|---|
| `design-system/check-vendorable.sh` | Vendored files never reference Flag docs by relative path; the token JSON parses; icon ids are unique |
| `design-system/check-email-template.sh` | `email-safe.html` stays under Gmail's 100 KB and 8,192-character style limits, and the preview copy is in sync |
| `scripts/check_tokens.py` | `design-tokens.json` and `design-tokens.css` declare the same tokens with the same values, in both themes; tokens are static values and `components.css` gives every newer color function a static fallback; every text, badge, fill, gradient, switch and focus-ring pair meets WCAG AA in both themes |
| `scripts/check_refs.py` | Markdown links and anchors resolve; docs never prescribe a token pair the contrast check rejects; `components.css` has a selector for every class COMPONENTS.md documents, every interaction state (hover, focus-visible, active, disabled) of every control, every documented component state, a visible focus-visible indicator for every control and a measured focus ring on every calendar day state, a reduced-motion override for every infinite animation, and a token override for every vendored flatpickr color; the preview references only files that exist and that the live site deploys; `preview/components.css` is in sync; every icon is in the sprite, `ICONS.md` and the preview; every logo is documented and shown; the font sheet is complete; every `flag-sync.sh add` example and repo path in the docs exists; every doc HTML snippet carries the preview's role, tabindex and aria-* attributes |
| `scripts/check_license.sh` | `design-system/LICENSE` carries the same MIT text as the root `LICENSE` |
| `scripts/check_product_tools.sh` | `tools/product/flag-sync.sh` and `stack-check.sh` (and Flag's own shell scripts) are shellcheck-clean and executable; their `FLAG_SYNC_VERSION` / `STACK_CHECK_VERSION` match what `tools/product/README.md` and `APPLY_TO_PRODUCT.md` name; the shipped standard block hashes to the `STANDARD_SHA` that `stack-check.sh` pins |

All checks are standard-library Python or POSIX sh and run offline.

`make audit` renders the preview in Chromium (light and dark, 1440 and 390
wide, with the date and date-time pickers open) and fails on any axe
WCAG 2 A/AA violation, any text below its contrast floor as actually painted
(including over gradients, which axe skips), any focusable control with
no visible focus, or a calendar day (range start and end, in range, today,
plain) that, reached with the arrow keys, lacks a 2px inset ring at 3:1
against its fill. It needs Node and installs Playwright and axe-core into
`.audit/` on first use, so CI runs only `make check`; run `make audit` before
a PR that changes `components.css`, the tokens or the preview.

## Proposing a change

### A new token

1. Add it to `design-system/tokens/design-tokens.css`, in `:root` (dark) and,
   if the light value differs, in `:root[data-theme="light"]`. A token with no
   light value must read well in light too.
2. Add the same token to `design-tokens.json`, with the same value, under the
   matching path (`color.text.primary` is `--color-text-primary`;
   `scripts/check_tokens.py` lists the few older aliases).
3. If it is a color something reads or a state indicator, add its pair to
   `CONTRAST` in `scripts/check_tokens.py` so the floor is enforced.
4. Document it in `design-system/TOKENS.md` and show it in the preview when
   it is visible.

Name tokens for their role (`--color-on-primary-fill`), not their value or
one product's screen.

### A new icon

1. Add a `<symbol>` to `design-system/icons/core-icons.svg`: 24×24 viewBox,
   `stroke="currentColor"`, round caps and joins, stroke width 1.9. Check it
   is not a duplicate of an existing glyph.
2. List it in `design-system/ICONS.md` under "Canonical Icon Names" with what
   it means.
3. Add it to the Core Icons grid in `design-system/preview/index.html`.

`make check` fails until all three are done. If the glyph is drawn after
another set, its licence must allow it and the notice goes in the sprite.

### A new logo

Add the file under `design-system/logos/`, document it in
`design-system/LOGOS.md` (which context, which theme) and show it in the
preview's logo gallery. Ship light and dark variants when one file cannot
reach 3:1 on both themes' surfaces.

### A component or pattern

Spec it in `design-system/COMPONENTS.md` (structure, classes, every state,
keyboard and screen-reader behavior) and implement it in
`design-system/components/components.css` with tokens only: products vendor
that file. Then run `make sync` (the preview loads a byte copy, because the
live site only publishes `preview/` plus tokens, fonts, icons and logos), show
it in the preview, and make it pass the contrast and accessibility rules in
`INTERACTION_ACCESSIBILITY.md`. Preview-only layout goes in
`preview/styles.css`. A newer color function (`color-mix()`, `oklch()`, ...)
needs a static fallback declaration right before it; tokens must be static
values.

## Breaking changes

Products vendor Flag's files byte for byte and reference icon ids, logo file
names and token names directly. So:

- **Renaming or removing** a token, an icon id or a logo file is a breaking
  change for every product that uses it. Prefer adding the new name and
  keeping the old one. When removal is truly needed, say "breaking" in the PR
  title, list the affected products (search their repos for the name), and
  give the replacement.
- **Changing an existing value** (a token's color, an icon's drawing, a logo)
  changes every product's look on its next sync. Do it only as a deliberate
  fix (a contrast failure, a broken glyph), state the old and new value and
  why in the PR, and attach before/after screenshots.
- **Adding** is not breaking. Products pick additions up when they want them.

## Preview your change in both themes

Every visual change is checked in light and dark, at desktop and phone width.
The preview's toggle (top right) switches theme and remembers the choice; or
set your OS appearance and clear the `flag-theme-preference` key. Attach
light and dark screenshots of what changed to the PR.

## Pull requests

- Work on a branch off `main`; `main` is protected and CI runs on every PR.
- Commit subjects in this repo start with a gitmoji and describe the effect
  ("✨ Segmented control spec and preview", "🐛 Theme toggle gets its aria
  state on load").
- One concern per PR. Update the docs a change invalidates in the same PR.
- `make check` passes.
- No secrets, internal hostnames, real people's addresses or real customer
  data. Examples use `example.com` addresses and fictional names.

The PR template asks for exactly this.

## Reporting bugs and requesting assets

Open an issue: the bug template for something that renders or behaves wrong,
the request template for a missing token, icon, logo or component. Security
problems go to the address in [`SECURITY.md`](SECURITY.md), not an issue.
