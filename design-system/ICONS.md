# Core Icons

This is the shared icon vocabulary for all Elcano microservices.

## Source
- Sprite file: `icons/core-icons.svg`
- Style: stroke-based, rounded caps and joins.
- Stroke width: `1.75` to `2`.

## Sizing
- Inline in controls: `1rem`.
- Icon buttons and nav controls: `1.25rem`.
- Feature/empty-state icon: `1.5rem` to `2rem`.

## Canonical Icon Names
- `download` - export/report download actions
- `trash` - destructive remove/delete actions
- `logout` - sign out/session end
- `paperclip` - file attachment and upload affordance
- `calendar` - date picker and schedule fields
- `clock` - time picker and runtime metadata
- `search` - search controls
- `filter` - filter drawer/toggle
- `plus` - create/add action
- `close` - dismiss modal/toast
- `chevron-down` - dropdown disclosure
- `info` - helper and tooltip affordance
- `sun` - light mode indicator and theme toggle
- `moon` - dark mode indicator and theme toggle
- `tools` - tools/connections trigger (the chat composer wrench) and its library header
- `lock` - locked, always-on state (no switch)
- `maximize` - open the full view of a popover (e.g. the tool library)
- `alert-circle` - needs-setup state
- `alert-triangle` - unavailable state
- `external-link` - link that leaves the current surface (Settings, a vendor console)
- `chevron-right` - inline "go on" affordance ("Set up ›") and disclosure

## Accessibility Rules
- Decorative icons: `aria-hidden="true"`.
- Icon-only controls: include `aria-label`.
- Pair destructive icons with explicit text when space allows.

## Example Usage

```html
<button class="btn btn-danger" aria-label="Delete task">
  <svg class="icon" aria-hidden="true"><use href="../icons/core-icons.svg#trash"></use></svg>
  Delete
</button>
```
