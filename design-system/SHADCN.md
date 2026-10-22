# shadcn/ui Registry (Tier B)

Flag publishes a [shadcn/ui](https://ui.shadcn.com) registry: the base UI for
Elcano's React apps (Tier B in the frontend standard: Vite + React +
TypeScript, built to a static bundle that the Go server embeds). Tier A
(server-rendered) pages use Flag's CSS component classes instead; every
registry item has a Tier A equivalent with the same name, variants and states.
The mapping is in [COMPONENTS.md](COMPONENTS.md#shadcnui-tier-b-mapping).

- Registry index: `https://flag.elcanotek.com/r/registry.json`
- Item URLs: `https://flag.elcanotek.com/r/{name}.json` (for example
  `https://flag.elcanotek.com/r/button.json`)
- Namespace used below: `@flag`
- Preview: `https://flag.elcanotek.com/shadcn.html` (kitchen sink in both themes)

The items are upstream shadcn/ui components (Radix via the `radix-ui`
package, `class-variance-authority`, `lucide-react`) restyled to Flag's
[COMPONENTS.md](COMPONENTS.md) specs: Flag's focus ring token, radii, motion
tokens, hover, active and disabled states, the popover and modal surfaces, and
reduced motion. Their colours come from Flag tokens through
[`shadcn/theme.css`](shadcn/theme.css), never from copied hex values.

## Adopt in a Tier B app

The app needs Tailwind CSS v4 (`@tailwindcss/vite`) and the `@/*` import
alias in `tsconfig.json` and `vite.config.ts`.

1. **Vendor Flag's stylesheets** with the shared vendoring script, like every
   other Flag file (see [APPLY_TO_PRODUCT.md](APPLY_TO_PRODUCT.md#vendoring-and-drift)).
   Flag paths are relative to Flag's `design-system/`:

   ```sh
   scripts/flag-sync.sh add ../flag fonts web/src/flag/fonts
   scripts/flag-sync.sh add ../flag tokens/design-tokens.css web/src/flag/tokens/design-tokens.css
   scripts/flag-sync.sh add ../flag shadcn/theme.css web/src/flag/shadcn/theme.css
   scripts/flag-sync.sh add ../flag theme/theme-controller.js web/src/flag/theme/theme-controller.js
   scripts/flag-sync.sh add ../flag LICENSE web/src/flag/LICENSE
   ```

2. **Import them** in the app stylesheet, in this order. Keep the tokens
   unlayered (no `layer(...)` on the import):

   ```css
   @import "tailwindcss";
   @import "tw-animate-css";
   @import "./flag/fonts/fonts.css";
   @import "./flag/tokens/design-tokens.css";
   @import "./flag/shadcn/theme.css";
   ```

   Fonts are Nebula Sans and Hack from Flag's `fonts.css` only. Do not add
   `@fontsource` packages or font CDNs; `theme.css` points `font-sans`,
   `font-heading` and `font-mono` at Flag's font tokens.

3. **Load the theme controller before first paint** (`import
   "./flag/theme/theme-controller.js"` at the top of `main.tsx`, or a
   `<script>` in `index.html`). The theme follows Flag's contract:
   `html[data-theme="light"|"dark"]`, system preference by default, an explicit
   choice stored as `flag-theme-preference`. Tailwind's `dark:` variant is
   remapped to the same contract, but Flag components never need it: the
   tokens switch on their own.

4. **Write `components.json` by hand** (do not run `shadcn init`; it would
   apply one of shadcn's own presets and its CSS variables):

   ```json
   {
     "$schema": "https://ui.shadcn.com/schema.json",
     "style": "new-york",
     "rsc": false,
     "tsx": true,
     "tailwind": { "config": "", "css": "src/index.css", "baseColor": "neutral", "cssVariables": true, "prefix": "" },
     "iconLibrary": "lucide",
     "aliases": {
       "components": "@/components",
       "utils": "@/lib/utils",
       "ui": "@/components/ui",
       "lib": "@/lib",
       "hooks": "@/hooks"
     },
     "registries": { "@flag": "https://flag.elcanotek.com/r/{name}.json" }
   }
   ```

   Keep these aliases: items import `@/lib/utils`, `@/components/ui/*` and
   `@/hooks/*`, and the CLI rewrites them to whatever the aliases say.

5. **Add items** with the pinned CLI:

   ```sh
   npx shadcn@4.21.4 add @flag/flag-theme
   npx shadcn@4.21.4 add @flag/button @flag/input @flag/dialog
   ```

   `@flag/flag-theme` installs the shared runtime dependencies
   (`radix-ui`, `class-variance-authority`, `clsx`, `tailwind-merge`,
   `lucide-react`, `tw-animate-css`) and `@flag/utils` (`cn`). Each component
   pulls its own `@flag/*` dependencies. The files land in
   `src/components/ui/` and are the app's own code from then on: reviewed,
   tested and committed like anything else. List the runtime dependencies in
   the app's AGENTS.md as the standard asks.

Add items from Flag's registry, not from upstream (`npx shadcn add button`
without `@flag/` installs the unthemed upstream version).

## What the theme maps

`theme.css` defines shadcn's variables from Flag tokens:

| shadcn variable | Flag token | Notes |
|---|---|---|
| `--background` / `--foreground` | `--color-bg` / `--color-text-primary` | |
| `--card` | `--color-surface-1` | cards, modals, sheets |
| `--popover` | `--color-surface-2` | popovers, menus, select lists, toasts |
| `--primary` / `--primary-foreground` | `--color-primary-fill` / `--color-on-primary-fill` | the measured fill pair (4.5:1), not the raw primary |
| `--secondary`, `--muted` | `--color-surface-2` | |
| `--muted-foreground` | `--color-text-muted` | placeholders, low-emphasis text |
| `--accent` / `--accent-foreground` | `--color-selected-bg` / `--color-text-primary` | the highlighted menu item or row ("accent tone") |
| `--accent-solid` / `--accent-solid-foreground` (Flag addition) | `--color-accent` / `#1A0B1E` dark, `#FFFFFF` light | Flag's accent used as a fill (`bg-accent-solid text-accent-solid-foreground`, the badge `accent` variant); shadcn's `--accent` is the hover wash, so the fill gets its own pair. The label is set in `theme.css` per theme (the token sheet has no accent label) and measured by `check_tokens.py` |
| `--destructive` | `--color-danger` | destructive controls use the status-error triplet |
| `--border` | `--color-border` | |
| `--input` | `--color-control-border` | 3:1 field edge (input, textarea, select trigger); Tier A fields keep `--color-border` |
| `--ring` | `--color-accent` | controls draw `--focus-ring` itself |
| `--radius` | `--radius-md` | `rounded-sm/md/lg/xl` are Flag's radius scale |
| `--chart-1..5` | primary, accent, secondary, info, warning | provisional until Flag has a chart palette |
| `--sidebar-*` | surface-1, primary fill, selected-bg, border, accent | |

It also adds Flag-only utilities: `text-title`, `text-subtitle`, `text-body`,
`text-body-md`, `text-caption`, `text-overline`; `bg-surface-1`,
`bg-surface-2`, `bg-surface-inset`, `border-border-strong`, `text-subtle`
(secondary text), `text-link`, `text-success`, `text-warning`, `text-info`,
`bg-accent-solid` / `text-accent-solid-foreground`. Anything else reads a token directly, for
example `bg-(--color-status-running-bg)`.

## Flag additions to the upstream API

| Item | Addition |
|---|---|
| `badge` | variants `pending`, `scheduled`, `assigned`, `leased`, `running`, `analyzing`, `success`, `warning`, `error`, `cancelled` (the task status set), and `accent` (`--accent-solid-foreground` on `--color-accent`) |
| `alert` | variants `info`, `success`, `warning` beside `default` and `destructive` |
| `tabs` | `TabsList variant="default"` is Flag's segmented control; `variant="line"` is page tabs |
| `switch` | sizes `default` (30x18) and `lg` (38x22), from the connection picker |
| `table` | `TableRow interactive` turns on row hover and pointer (Flag: hover only on clickable rows); the container scrolls from the keyboard |
| `sonner` | follows `html[data-theme]` through `useFlagTheme` (`@flag/use-flag-theme`) instead of `next-themes` |
| `utils` | `cn` knows Flag's `text-*` sizes, so `cn("text-caption", "text-subtle")` keeps both |

## Accessibility

- Disabled controls never show hover or pressed styles: the registry uses
  `enabled:hover:` on Radix buttons and `disabled:pointer-events-none`
  elsewhere, matching the disabled gate in `components.css`.
- Every control shows `--focus-ring` (switches `--focus-ring-picker`, tabs a
  2px accent outline, as Flag's segmented control) on `:focus-visible` only.
- Icon-only buttons need `aria-label`; pair them with a `Tooltip`.
- Give `PopoverContent` an accessible name (`aria-labelledby` pointing at its
  `PopoverTitle`, or `aria-label`): it is a dialog.
- The kitchen sink passes axe with no page-level violations in both themes at
  1440 and 390 px. While a Radix *modal* menu or select is open, axe also
  reports `aria-hidden-focus`, `landmark-one-main` and `page-has-heading-one`
  (Radix hides the rest of the page from assistive technology and traps focus
  in the menu), and `region` for the portalled popup. These come from Radix's
  modal behaviour, which is correct; pass `modal={false}` to a
  `DropdownMenu` if a page needs the rest of the UI reachable while it is open.

## Propose a new item or change one

1. Start from the current upstream source (`https://ui.shadcn.com/r/styles/new-york-v4/<name>.json`).
2. Put it in `design-system/shadcn/registry/flag/ui/<name>.tsx`. Import
   `cn` from `@/lib/utils` and other items from `@/registry/flag/ui/<item>`.
   Swap shadcn's colours and `ring-*` focus for Flag tokens and states
   (copy the patterns of the existing items). No `dark:` utilities and no
   literal colours.
3. Add the item to `design-system/shadcn/registry.json` (`registryDependencies`
   use `@flag/<item>`; `dependencies` name the npm packages with a caret range).
4. Add or update its Tier A class in `components/shadcn-parity.css` (or the
   spec in `components/components.css` it already maps to) and its row
   in the [mapping table](COMPONENTS.md#shadcnui-tier-b-mapping), so both tiers
   stay alike.
5. `make registry` (rebuilds `preview/r/`), then
   `sh design-system/shadcn/kitchen-sink/verify.sh /tmp/ks --preview` after
   adding the item to `kitchen-sink/App.tsx`. Commit the source, the built
   JSON and the refreshed renders together.

CI's `shadcn-registry` job validates `registry.json` against the shadcn
schemas (vendored in `shadcn/schema/`) and fails if `preview/r/` is not what
a fresh build produces. `make registry-check` runs the same locally.

## Versioning

- The registry is served from Flag's `main`; item URLs are not versioned.
  Merging to `main` updates what `shadcn add` installs from then on.
- Apps own their copies. Nothing changes in an app until someone runs
  `npx shadcn@4.21.4 add @flag/<item> --diff` (to review) or `--overwrite`
  (to take the new version) in that app's own PR, the same deliberate re-sync
  as `flag-sync.sh sync`. Local edits to a copied component are allowed but
  should be upstreamed here.
- `theme.css` is vendored and locked by `flag.lock`; re-sync it with the
  tokens, since its variables name Flag tokens.
- Renaming or removing an item, a variant or a theme variable is a breaking
  change for every Tier B app: say so in the PR and list the apps (fleet,
  manifest).
- The CLI is pinned (`shadcn@4.21.4` in `shadcn/package.json` and in these
  docs). Bump it deliberately, rebuild, and run `verify.sh`.
