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

Products **vendor** Flag files (copy them into the product repo and serve them
from the product's own binary — no CDN, no runtime dependency on this repo).
Every copy is recorded in a lock file so it cannot drift silently; see
[Vendoring and drift](#vendoring-and-drift) below. Never copy by hand.

Copy these sources before product component work:
- `tokens/design-tokens.css`
- `tokens/design-tokens.json`
- `icons/core-icons.svg`
- `theme/theme-controller.js`
- `components/components.css`: the component layer (buttons, fields, chips,
  cards, badges, tables, segmented control, ...) for server-rendered (Tier A)
  products. Load it after the tokens and keep product styling in a separate
  sheet that loads after it. Tier B (React) products may skip it and build
  the same specs as components.
- the font sheet and both face directories (see [`FONTS.md`](FONTS.md)):
  `fonts/fonts.css` + `fonts/nebula-sans/` + `fonts/hack/`. Copy `nebula-sans/OFL.txt`
  and `hack/LICENSE.md` along with the font binaries — both licences require it.
  The same sheet is correct for every product; there is no licence tier to pick.

Import the font stylesheet alongside `design-tokens.css`:

```html
<link rel="stylesheet" href="/path/to/fonts/fonts.css" />
<link rel="stylesheet" href="/path/to/design-tokens.css" />
<link rel="stylesheet" href="/path/to/components.css" />
```

Order between the first two does not matter — the font sheet sets `--font-brand` and the
two code variables, which the token sheet only reads. A product that loads neither
falls back to a system stack, which looks visibly wrong rather than quietly
substituting some other brand face.

> Flag is MIT-licensed (see the root `LICENSE`), so any product may vendor it;
> list Flag (MIT, ElcanoTek) in the product's `NOTICE` or licensing doc, and
> copy the font licence files with the fonts.

## 2) Wire Theme in App Shell

Preferred option: copy or import `theme/theme-controller.js` and use the canonical toggle marker:

```html
<script src="/path/to/theme-controller.js"></script>
<button data-flag-theme-toggle class="icon-action theme-toggle" type="button" aria-label="Switch to dark mode" aria-pressed="false">...</button>
```

If a product cannot import the shared controller directly, preserve the same behavior and storage contract. Apply theme on initial load before main UI render when possible:

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
<button data-flag-theme-toggle class="icon-action theme-toggle" type="button" aria-label="Switch to light mode" aria-pressed="true">
  <span class="theme-toggle__icon-wrap" aria-hidden="true">
    <svg class="icon-inline theme-toggle__icon theme-toggle__icon--sun" aria-hidden="true"><use href="../icons/core-icons.svg#sun"></use></svg>
    <svg class="icon-inline theme-toggle__icon theme-toggle__icon--moon" aria-hidden="true"><use href="../icons/core-icons.svg#moon"></use></svg>
  </span>
</button>
```

Required behavior:
- click toggles between `light` and `dark`
- updates `aria-label` to describe next action
- updates `aria-pressed` to reflect dark mode state
- updates visible icon state
- if the product header already uses icon-only actions, keep the toggle icon-only and match the same button size
- on mobile, keep the theme toggle and sibling header actions in one non-wrapping top-right row

Recommended header adoption:
- Reuse the shared `.page-header` and `.ds-app-header` in login and authenticated pages unless the product has a documented exception.
- Header support copy is optional; omit it rather than inventing page-specific intro text when the screen is already self-explanatory.

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

a {
  color: var(--color-link);
}

.btn-primary {
  background: var(--gradient-action-fill);
  color: var(--color-on-primary-fill);
}
```

Additional implementation requirements:
- Filled controls paint their label on a measured fill: primary buttons use
  `--gradient-action-fill` (dark) or solid `--color-primary-fill` (light)
  with `--color-on-primary-fill`; selected calendar days likewise. Never put
  a label on raw `--color-primary` or `--gradient-action-primary` (white on
  `#7272AB` is 4.46:1). See COMPONENTS.md "Foreground on a saturated fill".
- Links use `--color-link` (4.5:1+ on every surface in both themes).
- When porting the shared checkbox pattern, copy the full structure and verify the checkmark asset actually exists.

## 5) Keep Accessibility + Persistence Intact

- Icon-only controls require `aria-label`.
- Decorative SVGs remain `aria-hidden="true"`.
- Keep keyboard behavior and `:focus-visible` (`var(--focus-ring)`) on custom controls.
- If using a live region, announce theme changes when users toggle manually.
- Persist only explicit user choice; do not persist inferred system value as explicit choice.

## 6) What to Configure

- Path aliases/import paths for tokens and icons in your app.
- Optional local wrapper around `theme/theme-controller.js` if your bundler or app shell requires it.
- Placement of the theme toggle in app shell/header.
- Optional wiring into app state/store (the root `data-theme` value remains the source of applied theme).

## 7) Launchpads and Resource Directories

When implementing an internal home/launchpad screen:
- Use the shared `.page-header` and standard shell first.
- Prefer featured cards for top-priority workflows.
- Use `details/summary` groups with `.link-tile` entries for secondary resource directories.
- Include the live Flag design-system site (<https://flag-71q.pages.dev/>) in docs/resources sections when the product exposes internal reference links.
- If directory links need app/service icons, use the shared iconography rules from `COMPONENTS.md` and `LOGOS.md` rather than inventing custom badge treatments.

## 8) What Not to Change

- Do not replace `html[data-theme]` with ad hoc selectors.
- Do not rename `flag-theme-preference` per product unless there is a hard requirement.
- Do not swap in custom sun/moon artwork when the shared icon sprite is available.
- Do not add per-component local light/dark overrides when token overrides already exist.

## 9) Recommended Migration Order

1. Import tokens/icons and apply root `data-theme` selector contract.
2. Add theme controller (system default + persisted preference + system-change sync).
3. Add shared theme toggle and verify accessibility attributes.
4. Migrate component styles to semantic tokens only.
5. Validate visual parity and interaction/accessibility behavior in both themes.

## Vendoring and drift

Every Elcano product vendors Flag the same way, with two scripts shared
verbatim across the product repos (`scripts/flag-sync.sh` and
`scripts/stack-check.sh`; the canonical copies live in each product repo and
are identical everywhere — change them in all repos at once):

- `flag.lock` at the product repo root records the Flag commit and the sha256
  of every vendored file (`file <sha256> <flag-path> <repo-path>`), plus `dir`
  lines for directories that must contain only locked Flag files.
- **Paths:** a `<flag-path>` is always relative to Flag's `design-system/`
  directory (`tokens/design-tokens.css` is
  `design-system/tokens/design-tokens.css` in this repo); a `<repo-path>` is
  relative to the product repo root. flag-sync reads the files from the Flag
  checkout's committed `HEAD` (never its working tree) and refuses a checkout
  with uncommitted changes under `design-system/`.
- `scripts/flag-sync.sh check` runs offline in the product's CI and fails on
  any hand edit, missing file, or unlocked file inside a vendored directory.
  It is the PR gate (run through `scripts/stack-check.sh`).
- `scripts/flag-sync.sh add ../flag <flag-path> <repo-path>` vendors a new file
  or directory, for example
  `scripts/flag-sync.sh add ../flag components/components.css static/flag/components/components.css`;
  `scripts/flag-sync.sh sync ../flag` re-copies everything at a newer Flag
  commit (a locked `dir` mirrors its Flag directory: new upstream files are
  added and removed ones deleted);
  `scripts/flag-sync.sh status ../flag` lists what is stale, including files
  Flag added to a locked `dir` (exit 3 when stale). All three take a local
  checkout of this repo (a sibling `../flag` by default).
- `.github/workflows/flag-drift.yml` (shared verbatim, like the scripts) runs
  weekly: it checks out this repo's `main` and runs `flag-sync.sh status`, so
  a product learns that Flag moved on without anyone remembering to look. The
  PR gate catches hand edits; the weekly job reports upstream staleness.
- Every product vendors Flag's `design-system/LICENSE` (the MIT text, kept
  identical to the repo-root `LICENSE` by this repo's CI) next to its vendored
  files, so the notice travels with them. Because `<flag-path>` is relative to
  `design-system/`, the command names it as just `LICENSE`:
  `scripts/flag-sync.sh add ../flag LICENSE static/flag/LICENSE` copies
  `design-system/LICENSE`, never the repo-root file. The font licence files
  travel inside `fonts/`, and the sprite carries its Lucide ISC notice inline.

Rules for product repos:

1. **Vendored files are byte-identical to Flag.** Product styling lives outside
   the vendored directories and reads tokens. A product that needs a new icon,
   logo, token or a fix asks for it here (a PR to this repo) and re-syncs; it
   never patches its copy.
2. **Vendor only what the product uses.** Lock individual icons/logos rather
   than whole directories when a product uses a few of them.
3. **Re-sync deliberately.** After a Flag change lands, each product re-syncs
   in its own PR, renders its pages in both themes, and fixes anything the
   change breaks.

Rules for this repo, so that files stay safe to vendor verbatim:

- Files under `tokens/`, `fonts/`, `theme/`, `icons/` and `logos/` must not
  depend on where they sit relative to this repo's docs: name docs as
  "Flag's design-system/FONTS.md", never with a relative path like
  `../FONTS.md` that is wrong once copied. `check-vendorable.sh` enforces this.
- Renaming or removing an icon id, logo file, or token is a breaking change
  for every product that vendors it: say so in the PR and list the products.
  So is changing an existing token value or redrawing an icon (every product
  changes look on its next sync): do it only as a deliberate fix, with
  before/after renders. See `CONTRIBUTING.md` at the repo root.

