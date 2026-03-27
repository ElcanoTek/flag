# Elcano Design System

This directory is the single documented source of truth for shared UI design decisions.

## Read Order
- `AGENT_GUIDE.md` - non-negotiable implementation contract
- `SYSTEM.md` - principles, architecture, approved patterns
- `TOKENS.md` - colors, typography, spacing, radii, elevation, layout
- `BACKGROUNDS.md` - gradient and background audit plus approved patterns
- `LOGOS.md` - approved logo assets and usage rules
- `ICONS.md` - canonical icon names, sizing, and usage
- `COMPONENTS.md` - component specs, variants, states, usage
- `INTERACTION_ACCESSIBILITY.md` - hover/focus/active/disabled/loading behavior
- `AUDIT.md` - cross-repo inconsistency audit and recommended deprecations
- `MIGRATION.md` - phased adoption plan per microservice

## Source Files
- `tokens/design-tokens.json` - machine-readable tokens
- `tokens/design-tokens.css` - CSS variable implementation
- `logos/` - approved SVG/PNG logo assets
- `icons/core-icons.svg` - canonical SVG sprite

## Visual Review
- `preview/index.html` - browsable style guide and component showcase

Open locally:

```bash
cd /root/flag/design-system/preview
python3 -m http.server 8765
```

Then visit `http://localhost:8765`.
