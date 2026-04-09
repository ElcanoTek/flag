# Elcano Design System

This directory is the single documented source of truth for shared UI design decisions.

## Read Order
1. `AGENT_GUIDE.md` - strict implementation contract (human + agent)
2. `TOKENS.md` - canonical foundations and token usage
3. `COMPONENTS.md` - component structures, states, and class mappings
4. `INTERACTION_ACCESSIBILITY.md` - required interaction and accessibility behavior
5. `SYSTEM.md` - system principles and architecture
6. `APPLY_TO_PRODUCT.md` - adoption guide for another product repo
7. `MIGRATION.md` - rollout strategy and sequencing
8. `AUDIT.md` - historical audit context and long-lived takeaways
9. supporting docs: `BACKGROUNDS.md`, `LOGOS.md`, `ICONS.md`, `EMAIL.md`, `email-safe.html`

## Source Files
- `tokens/design-tokens.css` - canonical runtime token source
- `tokens/design-tokens.json` - canonical machine-readable token source
- `fonts/code-fonts.css` + `fonts/*.ttf` - canonical self-hosted MOC code-component fonts
- `theme/theme-controller.js` - canonical light/dark theme controller for product adoption
- `logos/` - approved SVG/PNG logo assets
- `icons/core-icons.svg` - canonical SVG sprite
- `EMAIL.md` - approved email modules, plain-text guidance, and email-only color rules
- `email-safe.html` - canonical email-safe HTML reference aligned to the design system

Source precedence (when docs and examples differ):
1. `tokens/design-tokens.css`
2. `tokens/design-tokens.json`
3. `AGENT_GUIDE.md`
4. component/pattern docs

## Visual Review
- `preview/index.html` - browsable style guide and component showcase
- Live preview: `https://flag-71q.pages.dev/`
- Cloudflare Pages is connected to GitHub; changes go live automatically when they are pushed to `main`.
- `preview/email-safe.html` is a deployed preview copy of the canonical `email-safe.html`. After editing the canonical template, run `bash design-system/sync-email-preview.sh` before pushing so the Pages preview stays in sync.
Preview includes:
- canonical sun/moon light-dark theme toggle (system-default + persisted user preference)
- section expand/collapse controls
- component state strips
- launchpad/directory link-tile and app-icon usage patterns
- email template preview with light/dark inbox simulation and responsive viewport sizing
- implementation examples for key patterns

Open locally:

```bash
cd /root/flag/design-system/preview
python3 -m http.server 8765
```

Then visit `http://localhost:8765`.

Sync the deployed email preview copy:

```bash
bash design-system/sync-email-preview.sh
```

Run email guardrails:

```bash
bash design-system/check-email-template.sh
```

Email review checklist:
- desktop light preview
- desktop dark preview simulation
- mobile light preview
- mobile dark preview simulation
- default, long-content, and dense-table fixtures
- long table content and long CTA copy
- footer compliance content

## Example Implementation Prompt

Use the prompt below when assigning design-system adoption work in another Elcano repo:

```text
Pull the latest changes from both the `flag` repo and the `<target-repo>` repo.

Your task is to update the `<target-repo>` repo so that it strictly conforms to the design system defined in the `flag` repo.

Requirements:
- Treat the `flag` repo as the single source of truth for all design decisions.
- Read and follow the documented design system exactly, especially:
  - `design-system/README.md`
  - `design-system/TOKENS.md`
  - `design-system/COMPONENTS.md`
  - `design-system/APPLY_TO_PRODUCT.md`
- Also inspect the canonical implementation artifacts in `flag`, including:
  - `design-system/tokens/design-tokens.css`
  - `design-system/icons/core-icons.svg`
  - `design-system/logos/`
  - `design-system/preview/`
- Follow the documented design system exactly, including but not limited to:
  - color palette
  - typography
  - spacing
  - padding and margin
  - border radius
  - border treatments
  - buttons
  - links and email link styling
  - icons
  - layout patterns
  - header patterns
  - component styling
  - interaction states
  - light mode and dark mode behavior
  - mobile behavior
- Reuse or mirror established design tokens, component patterns, class naming, and behavior from `flag` wherever appropriate.
- Do not invent new styles or patterns unless absolutely necessary. If something is not clearly defined, infer from the existing `flag` repo system and stay consistent with it.
- Update existing UI in `<target-repo>` to align with the design system, but do not make unrelated product, backend, or architectural changes.
- Preserve existing functionality while improving the UI implementation to match the `flag` repo standards.
- Refactor inconsistent styling patterns in `<target-repo>` so the implementation is clean and maintainable.
- Prefer replacing local ad hoc UI patterns with canonical `flag` patterns rather than approximating them.

Implementation expectations:
- Import or vendor the canonical design-system assets from `flag` if needed instead of re-creating them.
- Use `flag`’s canonical theme contract:
  - `html[data-theme="light" | "dark"]`
  - `flag-theme-preference`
  - shared sun/moon theme toggle behavior
- Ensure shared header behavior follows `flag`, including mobile layout.
- Ensure icon-only actions match canonical sizing and accessibility requirements.
- Ensure checkboxes, date pickers, buttons, links, and selected states match the documented `flag` implementation exactly.
- If the target repo has login/auth pages, make them use the same shared header/app-shell patterns as defined in `flag` unless the repo has a documented exception.

Verification requirements:
- Verify the `<target-repo>` UI is visually consistent with the `flag` design system.
- Verify there are no obvious mismatches in typography, spacing, colors, links, checkbox styling, component styling, button states, date picker states, header layout, or mobile behavior.
- Verify the app still runs correctly.
- Verify all changes are scoped to bringing `<target-repo>` into compliance with the `flag` repo design system.

Git workflow requirements:
- Create a new feature branch in the `<target-repo>` repo for this work.
- Make all required UI updates in that branch.
- Commit the changes with a clear, professional commit message.
- Push the feature branch to the remote `<target-repo>` repo.

Output:
1. A short summary of what design system elements were updated in `<target-repo>`
2. Any areas where `<target-repo>` could not fully match `flag` and why
3. The branch name created
4. The commit hash / commit message used
5. The verification steps performed
```
