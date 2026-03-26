# Cross-Repo Audit Summary

Scope audited:
- `lens`
- `explorer`
- `home`
- `moc`
- `victoria` (no frontend UI surface present)
- `victoria-phone` (treated as Victoria Voice UI)

## Major Inconsistencies

## 1) Typography is fragmented
- `lens` uses IBM Plex Sans (`/root/lens/templates/index.html`).
- `home` uses Avenir Next (`/root/home/public/styles.css`).
- `moc` uses Share Tech Mono + VT323 (`/root/moc/cmd/moc/assets/css/dashboard.css`).
- `victoria-phone` uses Sora/Manrope (`/root/victoria-phone/app/dashboard.py`).
- `explorer` partially aligns with Dubai (`/root/explorer/app/static/styles.css`) but still deviates in scale.

## 2) Color system is close but not standardized
- Most products use deep purple/glaucous/payne's gray roots.
- Token names and opacity usage vary significantly by repo.
- Status colors vary by implementation, especially warning/error surfaces.

## 3) Button patterns diverge
- Rounded size and padding differ materially (8px to 20px radii).
- `moc` uses highly stylized retro mono buttons; `home` uses glossy app-launch buttons; `explorer` and `lens` are closer to each other.

## 4) Input and form behavior is inconsistent
- Field sizes, helper text style, and validation presentation vary.
- Focus states are present but not tokenized consistently.

## 5) Icon systems are inconsistent
- Stroke icon style appears in `lens` and `explorer`.
- `home` mixes logo marks and icon treatments per section.
- `moc` includes mixed icon densities and heavy glow usage.

## 6) Radius, spacing, and surface depth are inconsistent
- Cards range from subtle to highly stylized/glow-heavy.
- Spacing scales differ and are not token-backed.

## 7) Layout model mismatch
- `home` is marketing/launchpad style.
- `explorer` and `lens` are productivity UIs.
- `moc` is dense ops console with retro visual language.
- `victoria-phone` is a custom one-page dashboard with inline CSS.

## 8) Third-party style dependencies are not normalized
- `explorer` references Flatpickr CDN CSS/JS in templates (`/root/explorer/app/templates/inbox.html`).

## Reusable Patterns Identified
- Strongest upload dropzone: `lens` and `moc`.
- Strongest searchable results table + detail panel: `explorer`.
- Strongest card-grid launchpad pattern: `home`.
- Strongest task creation + scheduling form model: `moc`.
- Strongest lightweight status badge semantics: `lens` and `explorer`.

## Recommended Standard Component Sources
- Buttons/inputs baseline: `explorer` + `lens`.
- Upload/dropzone: `lens`.
- Tables/list rows and side detail panel: `explorer`.
- Scheduling presets/chips: `moc` (visual restyle required).
- Empty states: `explorer`.
- Toast and process feedback: `lens` (less visual noise than `moc`).

## Deprecation Targets
- Deprecate repo-specific ad hoc fonts across all services.
- Deprecate un-tokenized hardcoded status colors.
- Deprecate retro-only visual language in `moc` as shared default.
- Deprecate inline-only stylesheet approach for Victoria Voice dashboard.
- Deprecate external CDN dependency for core datepicker presentation in Explorer.
