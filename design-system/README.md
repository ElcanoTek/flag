# Elcano Design System

This directory is the single documented source of truth for shared UI design decisions.

## Read Order
- `AGENT_GUIDE.md` - non-negotiable implementation contract
- `SYSTEM.md` - principles, architecture, approved patterns
- `TOKENS.md` - colors, typography, spacing, radii, elevation, layout
- `COMPONENTS.md` - component specs, variants, states, usage
- `INTERACTION_ACCESSIBILITY.md` - hover/focus/active/disabled/loading behavior
- `AUDIT.md` - cross-repo inconsistency audit and recommended deprecations
- `MIGRATION.md` - phased adoption plan per microservice

## Source Files
- `tokens/design-tokens.json` - machine-readable tokens
- `tokens/design-tokens.css` - CSS variable implementation

## Visual Review
- `preview/index.html` - browsable style guide and component showcase

Open locally:

```bash
cd /root/flag/design-system/preview
python3 -m http.server 8765
```

Then visit `http://localhost:8765`.
