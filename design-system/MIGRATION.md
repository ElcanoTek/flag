# Migration Guidance

> **Note:** This is a historical document from the initial creation of the design system. It is preserved for context only. Do not use this file as a reference for current component patterns. The single source of truth is COMPONENTS.md.

## Adoption Strategy

### Phase 1 - Foundations First
- Import `tokens/design-tokens.css` into each microservice UI.
- Replace local color variables with canonical semantic tokens.
- Switch typography to Dubai Bold/Regular and tokenized scale.
- Add theme toggle support using the canonical `body.theme-light` override model.

### Phase 2 - Shared Primitives
- Standardize button variants, input fields, badges, cards, and empty states.
- Normalize focus/hover/disabled/loading behavior.
- Replace hardcoded radii/shadows/transitions with token variables.

### Phase 3 - Complex Components
- Align modals, table/list rows, filters, pagination, date pickers, and file upload.
- Replace divergent scheduling and chips implementation styling with tokenized variants.
- Ensure keyboard and screen-reader behavior for custom controls (chips, icon-only actions, disclosures).

### Phase 4 - Cleanup and Enforcement
- Remove deprecated component classes.
- Add lint/check rules to block forbidden colors/fonts.
- Update contribution templates to require design-system compliance.

## Repo-by-Repo Priority

## Explorer
- Remove CDN dependency for datepicker styles/scripts.
- Replace remaining ad hoc sizes with tokenized spacing/radius.

## Lens
- Migrate typography from IBM Plex to Dubai.
- Keep existing component structure; mostly token refactor.

## Home
- Convert Avenir-based typography and bespoke spacing to system tokens.
- Keep launchpad pattern but align controls, badges, and states.

## MOC
- Keep IA and feature model; replace visual language (fonts, glow-heavy effects, status palette mapping).
- Prioritize consistency of buttons/forms/tables/modals with system primitives.

## Victoria Voice (`victoria-phone`)
- Extract inline CSS into tokenized stylesheet.
- Align typography, button/input/table styles, and status badges.

## Victoria
- No active frontend surface identified in current repo.

## Definition of Done for Each Repo
- Uses canonical tokens for color, spacing, radius, typography.
- Ships required button/input/modal/table/status variants only.
- Passes interaction/accessibility baseline in `INTERACTION_ACCESSIBILITY.md`.
- Supports canonical dark/light theming without per-component ad hoc theme values.

## Fast Path Checklist
Use this for small repos or new UIs:
1. Import `tokens/design-tokens.css`.
2. Map existing UI colors/radius/spacing to tokens.
3. Implement buttons + inputs + badges + cards using `COMPONENTS.md` contracts.
4. Add required interactive states and accessibility attributes.
5. Add theme toggle (`body.theme-light`) and verify parity.
