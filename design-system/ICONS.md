# Core Icons

This is the shared icon vocabulary for all Elcano microservices.

## Source
- Sprite file: `icons/core-icons.svg` (72 symbols; every one is shown in the
  preview's Core Icons section).
- Style: stroke-based on a 24px grid, `currentColor`, rounded caps and joins.
- Stroke width: `1.75` to `2` (new glyphs use `1.9`). Two glyphs are filled
  on purpose because a stroke reads poorly at their size: `dots` (overflow
  menu) and `stop` (stop a running operation).
- Some glyphs are drawn after [Lucide](https://lucide.dev) (ISC); the notice
  lives in a comment at the top of the sprite, so it travels with every copy.

## Adding, renaming or removing an icon
- Adding a glyph is safe: add the `<symbol>` to the sprite, list it below with
  what it means, and add it to the preview's Core Icons grid.
  `scripts/check_refs.py` (run by `make check` and CI) fails when any of the
  three is missing, and when anything references an id the sprite lacks:
  `<use>` with a missing id renders an empty box and logs nothing.
- Pick a name for what the glyph *depicts or does* (`plug`, `refresh`), not
  for one product's screen.
- Do not add a second glyph for a meaning an existing one covers (there is one
  warning triangle, `alert-triangle`, and one wrench, `tools`).
- Renaming, removing or redrawing an existing id is a breaking change for
  every product that vendors the sprite: see `CONTRIBUTING.md`.

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
- `file` - generic file or document
- `folder` - folders, collections and file groups
- `book` - documentation, guides and help
- `menu` - open a navigation menu (hamburger)
- `copy` - copy to clipboard
- `activity` - activity feed, health and monitoring
- `arrow-right` - go forward, next step, continue
- `arrow-up` - send, submit or move up (e.g. a composer send button)
- `bar-chart` - reports, analytics and metrics
- `brain` - memory and learned knowledge
- `briefcase` - projects and bodies of work
- `bug` - bugs, issues and debugging
- `check` - done, confirmed or a selected option
- `check-square` - tasks and checklists
- `cloud` - cloud services and sync
- `compress` - collapse to a compact view (pairs with `expand`)
- `database` - data stores and datasets
- `dollar-sign` - cost, spend and billing
- `dots` - more actions (overflow menu); filled glyph
- `edit` - edit or rewrite
- `expand` - expand to a full view (pairs with `compress`)
- `file-text` - text documents and summaries of a document
- `globe` - web, sites and public reach
- `grid` - dashboards and grid views
- `headphones` - audio, calls and voice
- `image` - images and media
- `keyboard` - keyboard shortcuts
- `layers` - stacks, layers and grouped items
- `mail` - email and mailboxes
- `map-pin` - locations
- `megaphone` - announcements and campaigns
- `message` - messages and conversations
- `model` - an AI model or compute (chip)
- `panel-left` - toggle a side panel
- `persona` - a person, agent or persona
- `pin` - pin or keep in place
- `plug` - connections and integrations
- `puzzle` - skills, plug-ins and modular capabilities
- `refresh` - reload, retry or regenerate
- `return-key` - press Enter / submit hint
- `settings` - settings and preferences
- `shield` - admin, security and protected areas
- `shopping-cart` - commerce, purchases and orders
- `sparkles` - generated or polished output
- `stop` - stop a running operation; filled glyph
- `summarize` - summarize or fold ranges into a summary
- `tag` - tags and labels
- `target` - goals and targeting
- `zap` - automation, triggers and quick actions
- `selector` - up/down caret on a picker or select trigger (smaller than `expand`)
- `archive` - archive an item (move out of the active list without deleting)

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
