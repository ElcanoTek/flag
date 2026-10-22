# Security Policy

## Reporting a vulnerability

Email **security@elcanotek.com**. Please do not open a public issue, pull
request or discussion for a security problem.

Helpful to include:

- What the issue is and where in the repository it lives.
- How to reproduce it.
- What an attacker gets out of it, and which Elcano product would be exposed
  once it vendors the affected file.
- The commit sha you tested.
- Whether you intend to disclose publicly, and on what timeline.

If you would rather encrypt, say so in a first message with no details and we
will arrange a key.

## What to expect

| Stage | Target |
|---|---|
| Acknowledgement that a human has read it | 3 business days |
| Initial assessment and severity | 10 business days |
| Fix or documented mitigation for a confirmed high-severity issue | 30 days |

We will keep you updated and tell you when a fix ships. Credit is offered
unless you prefer otherwise. We do not operate a paid bug-bounty programme.

## Scope

Flag is a design system: static CSS, JSON, SVG, fonts, one small theme script
and a preview site. There is no server, no authentication and no data
handling here, so the realistic issues are about what products copy:

**In scope:**

- `design-system/theme/theme-controller.js` and anything else under
  `design-system/` that products vendor and serve: script injection, unsafe
  DOM handling, anything that would weaken a product's Content-Security-Policy
  (products serve Flag files from their own origin with no `unsafe-inline`).
- SVG files (`icons/`, `logos/`) that could carry script or external
  references into a product.
- The preview site's own scripts (`design-system/preview/*.js`).
- The checks and CI workflow (`scripts/`, `.github/`): anything that would let
  a pull request run with more privilege than it should.
- Accidentally committed credentials or personal data.

**Out of scope:**

- Third-party code vendored for the preview (`design-system/preview/vendor/`,
  flatpickr) unless our use of it creates the problem; report upstream.
- How a product serves or configures Flag files; report that to the product.
- Reports from automated scanners with no demonstrated impact.

## Supported versions

Fixes land on `main`; there are no maintenance branches. Products pick a fix
up by re-syncing (`scripts/flag-sync.sh sync`), and each product's weekly
`flag-drift` job reports when they are behind.
