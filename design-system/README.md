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
9. supporting docs: `BACKGROUNDS.md`, `LOGOS.md`, `ICONS.md`

## Source Files
- `tokens/design-tokens.css` - canonical runtime token source
- `tokens/design-tokens.json` - canonical machine-readable token source
- `logos/` - approved SVG/PNG logo assets
- `icons/core-icons.svg` - canonical SVG sprite

Source precedence (when docs and examples differ):
1. `tokens/design-tokens.css`
2. `tokens/design-tokens.json`
3. `AGENT_GUIDE.md`
4. component/pattern docs

## Visual Review
- `preview/index.html` - browsable style guide and component showcase

Preview includes:
- dark and light theme toggle
- section expand/collapse controls
- component state strips
- implementation examples for key patterns

Open locally:

```bash
cd /root/flag/design-system/preview
python3 -m http.server 8765
```

Then visit `http://localhost:8765`.
