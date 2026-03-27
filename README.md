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
- `design-system/tokens/design-tokens.css` - canonical runtime token source
- `design-system/tokens/design-tokens.json` - canonical machine-readable token source
- `design-system/icons/core-icons.svg` - icon sprite
- `design-system/logos/` - approved logo assets
- `design-system/preview/index.html` - live visual reference

## Source of Truth Order
Use this precedence when there is ambiguity:
1. `design-system/tokens/design-tokens.css`
2. `design-system/tokens/design-tokens.json`
3. `design-system/AGENT_GUIDE.md`
4. component and pattern docs (`COMPONENTS.md`, `SYSTEM.md`, `INTERACTION_ACCESSIBILITY.md`)

## Implementation Workflow
1. Import `design-system/tokens/design-tokens.css` first.
2. Implement UI using semantic tokens only (`var(--color-primary)`, `var(--radius-md)`, etc.).
3. Apply canonical component structure/classes from `COMPONENTS.md`.
4. Implement required states (`hover`, `focus-visible`, `active`, `disabled`).
5. Verify behavior in preview and against `INTERACTION_ACCESSIBILITY.md`.

## Agent Workflow
For coding agents working in product repos:
1. Read `design-system/AGENT_GUIDE.md` first.
2. Follow `design-system/APPLY_TO_PRODUCT.md` for adoption steps.
3. Use token variables; do not hardcode colors, radii, spacing, or transition values.
4. Support light/dark via canonical theme tokens (`body.theme-light` override model).
