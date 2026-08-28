# Dubai font — licence notice (READ BEFORE COPYING)

**These files are proprietary. They are not open source and not OFL-licensed.**

| | |
|---|---|
| Family | Dubai (`Dubai W23`) |
| Files | `DubaiW23-Regular.{ttf,woff2}`, `DubaiW23-Bold.{ttf,woff2}` |
| Copyright | © 2017 Dubai Executive Council. All rights reserved. |
| Foundry | Monotype |
| Licence | Proprietary EULA from the Dubai Font programme. Elcano holds a use right, **not** a right to sublicense or relicense. |

## What this means in practice

Elcano may **use** the Dubai font in its own internal products. Elcano may **not**
grant anyone else a licence to it. Any repository that ships an outbound licence
(MIT, Apache, BSL 1.1, or any other) and also ships these files is, on its face,
purporting to license the font under those terms. Elcano cannot do that.

## Rules

- **DO** load `../dubai-fonts.css` in internal-only tools (Manifest) and in this
  repo's preview surface.
- **DO NOT** copy any file in this directory into `fleet` (MIT), `explorer`
  (BSL 1.1), or any other repository that is published, open-sourced, or made
  source-available.
- **DO NOT** reference `"Dubai"` from a token file, stylesheet, or `font-family`
  declaration that ships in one of those repositories, even without the binaries —
  a bare name reference is harmless legally but it is a false statement about what
  the product renders, and it is how the binaries get copied in later.
- Open-source and source-available products use IBM Plex Sans
  (`../ibm-plex-fonts.css`, SIL OFL 1.1). See [`../../FONTS.md`](../../FONTS.md).

If you need the font for a new surface, confirm the surface's licence tier in
`FONTS.md` first. If it is not internal-only, the answer is IBM Plex Sans.
