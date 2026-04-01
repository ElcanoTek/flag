# Logos

This document defines approved logo assets, usage contexts, and implementation rules.

## Approved Logo Assets

- `logos/elcano-mark-primary.svg`
  - Primary Elcano brand mark.
- `logos/elcano-mark-favicon.svg`
  - Compact Elcano mark for favicon/touch icon contexts.
- `logos/victoria-ship-white.svg`
  - Victoria product mark for dark theme surfaces.
- `logos/victoria-ship-dark.svg`
  - Victoria product mark for light theme surfaces.
- `logos/lens-favicon.svg`
  - Lens app mark for dark theme surfaces.
- `logos/lens-favicon-light.svg`
  - Lens app mark for light theme surfaces.
- `logos/explorer-favicon.svg`
  - Explorer app mark for dark theme surfaces.
- `logos/explorer-favicon-light.svg`
  - Explorer app mark for light theme surfaces.
- `logos/moc-icon-192.png`
  - MOC app icon for dark theme surfaces.
- `logos/moc-icon-192-light.png`
  - MOC app icon for light theme surfaces.

## Which Logo to Use

- Global/suite shell, company-level surfaces -> `elcano-mark-primary.svg`
- Browser tab/favicon/app-icon source -> `elcano-mark-favicon.svg` or app-specific icon
- Product-specific shell:
  - Lens -> `lens-favicon.svg` (dark), `lens-favicon-light.svg` (light)
  - Explorer -> `explorer-favicon.svg` (dark), `explorer-favicon-light.svg` (light)
  - MOC -> `moc-icon-192.png` (dark), `moc-icon-192-light.png` (light)
  - Victoria surfaces -> `victoria-ship-white.svg` (dark), `victoria-ship-dark.svg` (light)
- Internal launchpad/directory tiles:
  - suite/internal workspaces without a product-specific mark -> `elcano-mark-primary.svg`
  - first-party product tiles -> use the product's approved light/dark mark pair when available
  - external tools and vendor links -> use approved service icons/favicons, not product marks

## Rules

- Do not create new logo variants outside this directory.
- Do not recolor, stretch, rotate, skew, or add effects to logo files.
- Maintain minimum clear space of `0.5rem` around all marks.
- Minimum display size:
  - small UI contexts: `1.5rem`
  - header/brand lockup: `2rem`
  - hero/marketing: `2.75rem`+
- For dark backgrounds, use provided white/purple approved versions only.
- For light backgrounds, use the dedicated light-mode asset variant; do not recolor dark-mode files in product code.
- If a product mark has theme-specific variants, switch the asset by theme instead of applying CSS recoloring.
- Directory/link-tile icon wrappers may add tokenized border, radius, padding, and background treatment around approved assets, but must not visually modify the asset itself.

## Pairing Rules

- Use only one primary brand mark per header region.
- Product marks can appear with product name text, but should not visually override Elcano global branding in suite-level shells.
- In launchpads/directories, product marks may be shown in cards/tiles with consistent container sizing.
- Do not substitute a first-party Elcano product mark for an external vendor/service logo just because the host lacks a shared asset.
- If no approved external icon exists, fall back to `elcano-mark-primary.svg` until the correct asset is added.

## Implementation Notes

- Prefer SVG assets where available.
- Preserve aspect ratio: `width: auto; height: auto; object-fit: contain`.
- Keep logo wrappers tokenized for spacing, border, and background surfaces.
- Approved external app/service icons may live outside `design-system/logos/` when they are product-local launchpad assets, but naming should remain deterministic (for example, host-derived filenames) and products should document exceptions.
