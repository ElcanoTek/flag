# AGENTS.md

Guidance for coding agents working **in this repository**. If you are
building or changing a product's UI to follow Flag, read
[`design-system/AGENT_GUIDE.md`](design-system/AGENT_GUIDE.md) instead.

## What this repo is

Flag, the Elcano design system: tokens (`design-system/tokens/`), fonts,
the icon sprite, logos, the theme controller, component specs (Markdown) and a
static preview site (`design-system/preview/`, live at
<https://flag-71q.pages.dev/>). Every Elcano product vendors these files byte
for byte, locked by hash in its `flag.lock`. There is no build step and no
package manager.

## Commands

```bash
make check     # everything CI runs; must pass before you push
make audit     # render + axe + computed contrast (needs Node; run for UI changes)
make preview   # serve design-system/ at http://localhost:8765/preview/
make sync      # after editing components/components.css or email-safe.html
```

## Rules

- **Additive by default.** Renaming or removing a token, icon id or logo file,
  or changing an existing value, changes every product. Only do it as a
  deliberate fix, and say so in the PR (see `CONTRIBUTING.md` "Breaking
  changes").
- **Components live in `design-system/components/components.css`** (vendored
  by Tier A products); the preview loads a synced copy, so run `make sync`
  after editing it. `preview/styles.css` is preview page layout only.
- **Tokens are static values** (no `color-mix()`; precompute), and a newer
  color function in `components.css` needs a static fallback right before it.
- **CSS and JSON tokens move together.** Every token in
  `design-tokens.css` exists in `design-tokens.json` with the same value, dark
  and light; `scripts/check_tokens.py` enforces it and measures contrast.
- **A new icon or logo is three edits**: the asset, its line in `ICONS.md` /
  `LOGOS.md`, and its entry in the preview gallery (`check_refs.py`).
- **Vendorable files stay location-independent.** Nothing under `tokens/`,
  `fonts/`, `theme/`, `icons/` or `logos/` may point at a doc by relative path;
  write "Flag's design-system/FONTS.md" (`check-vendorable.sh`).
- **The preview only reaches `tokens/`, `fonts/`, `icons/` and `logos/`**
  outside `preview/`; that is what the Cloudflare deploy copies beside it.
  No remote scripts, styles or fonts.
- **Measure, do not eyeball.** New colors get a contrast pair in
  `scripts/check_tokens.py`; render the preview in light and dark at 1440 and
  390 wide before and after a visual change.
- **Public repo hygiene**: example addresses use `example.com`, fixture
  advertisers are fictional, no internal hostnames or real people's data.
- `design-system/LICENSE` must keep the root `LICENSE`'s MIT text
  (`check_license.sh`).
- Commits start with a gitmoji, as in the history.
