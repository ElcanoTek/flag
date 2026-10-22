# Flag Design System

This repository is the canonical source of truth for Elcano product design across services.

## Repo Purpose
- Define a single shared design language (tokens, components, interaction rules).
- Provide implementation-ready CSS/JSON tokens for product repos.
- Provide agent-readable guidance for deterministic UI implementation.
- Provide a visual preview surface for review and QA.

## Quick Start
Run preview locally:

```bash
cd design-system/preview
python3 -m http.server 8765
```

Then open `http://localhost:8765`.

## File Map
- `design-system/README.md` - design-system navigation and usage order
- `design-system/AGENT_GUIDE.md` - strict implementation contract for coding agents
- `design-system/TOKENS.md` - token model and usage rules
- `design-system/COMPONENTS.md` - component specs and class/state contracts
- `design-system/INTERACTION_ACCESSIBILITY.md` - required interaction and a11y behavior
- `design-system/APPLY_TO_PRODUCT.md` - how to adopt this system in another repo
- `design-system/FONTS.md` - typography and font licensing policy (which face each product may ship)
- `design-system/tokens/design-tokens.css` - canonical runtime token source
- `design-system/tokens/design-tokens.json` - canonical machine-readable token source
- `design-system/icons/core-icons.svg` - icon sprite
- `design-system/logos/` - approved logo assets
- `design-system/email-safe.html` - canonical email-safe HTML reference
- `design-system/check-vendorable.sh` - CI check that vendored files stay safe to copy verbatim (see `APPLY_TO_PRODUCT.md` "Vendoring and drift")
- `design-system/preview/index.html` - live visual reference

## Licensing and Fonts

Flag is released under the **MIT License** — see [`LICENSE`](LICENSE). Products
under any licence (MIT, BSL 1.1, internal-only) may vendor its tokens, icons,
logos, theme controller and stylesheets; keep the copyright notice with them
(each product lists Flag in its `NOTICE` or licensing doc). The bundled fonts
keep their own licences, listed in `LICENSE`.

Flag ships two typefaces, and every product uses both — there is no tier to choose
between:

| Role | Face | Licence | Font sheet |
|---|---|---|---|
| Text — headings, body, UI | **Nebula Sans** | SIL OFL 1.1 | `design-system/fonts/fonts.css` |
| Code — logs, tabular output | **Hack** | MIT (+ Bitstream Vera) | `design-system/fonts/fonts.css` |

One sheet declares both. Both faces are freely redistributable, so the same sheet
is correct for MIT, BSL 1.1, and internal-only products alike — which is why the
old two-tier split (Dubai for internal tools, IBM Plex for public repos) is gone.
`design-tokens.css` names no face directly; it resolves `--font-brand` and the two
code variables, falling back to a system stack so a product that forgets the sheet
looks visibly wrong rather than quietly rendering in a different brand face.

Read [`design-system/FONTS.md`](design-system/FONTS.md) before adding or changing a
typeface in any product.

## Source of Truth Order
Use this precedence when there is ambiguity:
1. `design-system/tokens/design-tokens.css`
2. `design-system/tokens/design-tokens.json`
3. `design-system/AGENT_GUIDE.md`
4. component and pattern docs (`COMPONENTS.md`, `SYSTEM.md`, `INTERACTION_ACCESSIBILITY.md`)

## Implementation Workflow
1. Import `design-system/fonts/fonts.css`, then `design-system/tokens/design-tokens.css`.
2. Implement UI using semantic tokens only (`var(--color-primary)`, `var(--radius-md)`, etc.).
3. Apply canonical component structure/classes from `COMPONENTS.md`.
4. Implement required states (`hover`, `focus-visible`, `active`, `disabled`).
5. Verify behavior in preview and against `INTERACTION_ACCESSIBILITY.md`.

## Agent Workflow
For coding agents working in product repos:
1. Read `design-system/AGENT_GUIDE.md` first.
2. Follow `design-system/APPLY_TO_PRODUCT.md` for adoption steps.
3. Use token variables; do not hardcode colors, radii, spacing, or transition values.
4. Support light/dark via the canonical root theme contract (`html[data-theme]`) and shared theme controller behavior.

## Canonical Theme Behavior
- This repo is the source-of-truth implementation for light/dark mode across all Elcano products.
- Default behavior is system-driven: preview resolves theme from `prefers-color-scheme` when there is no stored user preference.
- Explicit user choice is persisted in `localStorage` using `flag-theme-preference`.
- Stored user choice wins over system changes; system changes only auto-apply when preference is `system`/unset.
- The canonical root selector is `html[data-theme="light"]` or `html[data-theme="dark"]`.

Implementation lives in:
- `design-system/preview/index.html` (theme toggle UI with shared sun/moon icons)
- `design-system/preview/preview.js` (theme controller + persistence + system sync)
- `design-system/preview/styles.css` (theme toggle visuals + transition polish)
- `design-system/tokens/design-tokens.css` and `design-system/tokens/design-tokens.json` (theme token contract)
