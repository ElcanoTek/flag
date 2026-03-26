# Agent Implementation Guide

Use this when a prompt says: "Follow the design system in the flag repo."

## Hard Rules
- Use tokens from `tokens/design-tokens.css` or `tokens/design-tokens.json`; do not invent one-off colors/spacing.
- Typography is fixed:
  - Headlines and subheadlines: `Dubai Bold`.
  - Body/UI text: `Dubai Regular`.
- Type scale is fixed:
  - Title: `28px`.
  - Subtitle: `18px`.
  - Body: `12px` to `14px`.
- Keep radius, border, and shadow values from token scales only.
- Focus style must be visible and consistent (`2px` ring with offset).
- Primary actions must use the primary button variant.
- Danger actions must use danger semantic tokens; never repurpose primary color for destructive actions.

## Quick Token Map
- Primary: `--color-primary`
- Secondary: `--color-secondary`
- Accent: `--color-accent`
- Background: `--color-bg`
- Surface: `--color-surface-1`, `--color-surface-2`
- Border: `--color-border`
- Text: `--color-text-primary`, `--color-text-secondary`, `--color-text-muted`
- Status: `--color-success`, `--color-warning`, `--color-danger`, `--color-info`

## Component Defaults
- Buttons: `primary`, `secondary`, `tertiary`, `danger`, `icon`.
- Inputs: 40px min height, `radius-md`, token border/focus styles.
- Tables: sticky headers optional, row hover subtle, status badges use semantic tokens.
- Modals: surface container, max-width tokens, explicit close button and escape key.
- Empty/Loading/Error: always include heading, explanatory body text, and next action.

## Disallowed Patterns
- External font/CDN dependencies for core UI styles.
- New ad hoc status colors.
- Mixed font systems within one screen.
- Invisible focus states.
- Gradient-heavy controls for every element (reserve gradients for hero/high-emphasis surfaces).
