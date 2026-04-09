# Email System

This document defines the reusable email-specific patterns that sit on top of the core design system.

## Source Of Truth
- Canonical authored template: `design-system/email-safe.html`
- Deployed preview artifact: `design-system/preview/email-safe.html`
- Preview tooling: `design-system/preview/email-preview.html`

## Approved Modules
- Header block
  Use the dark branded header with kicker, send date, one primary heading, and one metadata line.
- Status strip
  Use a compact table-based badge + status row immediately under the header.
- Summary block
  Use one section heading and one or two short paragraphs for the main takeaway.
- Metric card
  Use a bordered off-white card for compact topline KPIs.
- Risk callout
  Use the warm callout treatment with left accent border for negative attention.
- Opportunity callout
  Use the green callout treatment with left accent border for positive attention.
- Data table
  Use the semantic desktop table and stacked mobile card pattern defined in `email-safe.html`.
- CTA block
  Use one bulletproof primary CTA per email.
- Compliance footer
  Keep the locked footer with mailing address, unsubscribe, and recipient reason.

## Content Constraints
- Subject target: 35-60 characters.
- Preheader target: 40-100 characters.
- Heading target: one line on desktop when possible.
- CTA target: 25 characters or fewer.
- Summary target: two short paragraphs maximum before cards/callouts.
- Campaign names should be concise, but stacked mobile cards must still survive longer names without layout breakage.

## Desktop Table Pattern
- Keep `<table>`, `<thead>`, `<tbody>`, and `scope="col"`.
- Zebra striping may be used by row, never by a single column.
- Header row uses `#EEF3FF`.
- Neutral row uses `#FAFAFA`.
- Zebra row uses `#F4F6FB`.
- Borders use `#D7DEEE` and inner separators use `#E6EBF5`.

## Mobile Stacked Table Pattern
- Hide the desktop table header.
- Stack each row into a card.
- The first cell becomes the card header and uses the highlighted header background.
- Remaining cells use one neutral body fill so the card reads as a single object.
- Apply borders to cells, not the `tr`, to avoid overflow and right-edge bleed.
- Keep compact inline labels for each stacked value.

## Email-Only Color Guidance
- Preferred large-surface light backgrounds: `#F4F6FB`, `#FAFAFA`
- Preferred dark text: `#141824`, `#33415F`, `#586F7C`
- Preferred table/card border: `#D7DEEE`
- Preferred table/card inner separator: `#E6EBF5`
- Preferred dark preview border: `#3A3A50`
- Preferred dark preview body card: `#2A2A3C`
- Preferred dark preview header card: `#252538`

Use these colors for email-specific patterns when a component needs stronger dark-mode resilience than the product UI.

## Plain-Text Companion
- Every production HTML email should have a plain-text companion when the sending system supports it.
- Plain-text order should match the HTML order:
  1. subject
  2. preheader summary
  3. status
  4. executive summary
  5. topline metrics
  6. risk
  7. opportunity
  8. campaign data table in text form
  9. CTA URL
  10. footer compliance content

Example table fallback:

```text
Campaign Performance

- Amazon US OLV | Current: $311,402 | Prior: $405,928 | WoW: -23.3%
- Amazon CA Display | Current: $72,119 | Prior: $68,004 | WoW: +6.1%
- Pepsi Display | Current: $54,882 | Prior: $58,131 | WoW: -5.6%
```

## Review Fixtures
- Default fixture: balanced content and three table rows.
- Long-content fixture: long subject, long campaign names, and longer summary copy.
- Dense-table fixture: more rows to test rhythm and border consistency.

These fixtures should be reviewable from the preview page before shipping visual changes.

## Guardrails
- Run `bash design-system/sync-email-preview.sh` after changing the canonical template.
- Run `bash design-system/check-email-template.sh` before pushing email-template changes.
- Keep raw HTML under 100KB to avoid Gmail clipping.
- Keep embedded style blocks under 8,192 characters.
