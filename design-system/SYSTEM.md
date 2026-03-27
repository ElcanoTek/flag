# Unified Design System Definition

## Purpose
Establish a durable, implementation-ready, cross-service design language for Elcano products.

## Design Principles
- Consistency over novelty in shared app flows.
- Strong visual hierarchy with restrained palette usage.
- Data readability first for operations-heavy interfaces.
- Accessibility as baseline behavior, not optional enhancement.
- Token-first implementation for scalability across services.

## System Architecture
- Foundations: tokens, typography, spacing, radii, shadows.
- Primitives: buttons, inputs, badges, cards, table rows.
- Complex components: upload zones, filters, scheduling controls, modals.
- Patterns: app shell, empty/loading/error feedback, detail panel flows.

## Approved Patterns

### App Shell
- Topbar with product identity and account/action controls.
- Main region with section cards and optional side/detail panel.

### Data Workflows
- Search/filter toolbar above result list/table.
- Status badges for lifecycle visibility.
- Inline action icons with text labels in dense contexts when space permits.

### File Workflows
- Drag-and-drop zone plus browse fallback.
- Explicit constraints and validation messaging near field.

### Scheduling Workflows
- Presets for common recurrences and timeout ranges.
- Advanced/collapsible custom expression mode.

## Implementation Guidance
- New surfaces must import `tokens/design-tokens.css` first.
- Components should follow specs in `COMPONENTS.md`.
- Interactions must satisfy `INTERACTION_ACCESSIBILITY.md`.
- Background and gradient choices must follow `BACKGROUNDS.md`.
- Any deviation requires explicit documentation in the owning repo.
