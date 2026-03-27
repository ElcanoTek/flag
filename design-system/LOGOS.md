# Logos

This document defines approved logo assets, usage contexts, and implementation rules.

## Approved Logo Assets

- `logos/elcano-mark-primary.svg`
  - Primary Elcano brand mark.
- `logos/elcano-mark-favicon.svg`
  - Compact Elcano mark for favicon/touch icon contexts.
- `logos/victoria-ship-white.svg`
  - Victoria product mark.
- `logos/lens-favicon.svg`
  - Lens app mark.
- `logos/explorer-favicon.svg`
  - Explorer app mark.
- `logos/moc-icon-192.png`
  - MOC app icon.

## Which Logo to Use

- Global/suite shell, company-level surfaces -> `elcano-mark-primary.svg`
- Browser tab/favicon/app-icon source -> `elcano-mark-favicon.svg` or app-specific icon
- Product-specific shell:
  - Lens -> `lens-favicon.svg`
  - Explorer -> `explorer-favicon.svg`
  - MOC -> `moc-icon-192.png`
  - Victoria surfaces -> `victoria-ship-white.svg`

## Rules

- Do not create new logo variants outside this directory.
- Do not recolor, stretch, rotate, skew, or add effects to logo files.
- Maintain minimum clear space of `0.5rem` around all marks.
- Minimum display size:
  - small UI contexts: `1.5rem`
  - header/brand lockup: `2rem`
  - hero/marketing: `2.75rem`+
- For dark backgrounds, use provided white/purple approved versions only.

## Pairing Rules

- Use only one primary brand mark per header region.
- Product marks can appear with product name text, but should not visually override Elcano global branding in suite-level shells.
- In launchpads/directories, product marks may be shown in cards/tiles with consistent container sizing.

## Implementation Notes

- Prefer SVG assets where available.
- Preserve aspect ratio: `width: auto; height: auto; object-fit: contain`.
- Keep logo wrappers tokenized for spacing, border, and background surfaces.
