#!/usr/bin/env python3
"""Check that every reference in the repo points at something that exists.

1. Markdown links. Every relative link in every *.md resolves to a file, and
   every #anchor to a heading in the target (GitHub's slug rules).
2. The preview. Every href/src/data-logo-*/url() in design-system/preview/
   (vendor/ excepted) resolves to a file. A reference that leaves preview/
   must land in tokens/, fonts/, icons/ or logos/: the live preview
   (https://flag-71q.pages.dev/) is preview/ with exactly those four
   directories copied beside it, so anything else 404s in production while
   working locally. No <link>/<script>/url() may load from another host.
3. Icons. Every core-icons.svg#id used anywhere exists in the sprite; every
   sprite id is listed in ICONS.md and shown in the preview's icon gallery.
   (`<use>` with a missing id renders nothing and logs nothing; this is
   fleet's spriteCoverage idea.)
4. Logos. Every file in logos/ is documented in LOGOS.md and shown in the
   preview; every logos/<file> named in a doc exists.
5. Fonts. fonts/fonts.css declares only Nebula Sans and Hack, every url() in
   it exists, and each face directory keeps its licence file.

Usage: python3 scripts/check_refs.py
"""

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
DS = ROOT / "design-system"
PREVIEW = DS / "preview"
DEPLOYED_BESIDE_PREVIEW = ("tokens", "fonts", "icons", "logos")
SPRITE = DS / "icons" / "core-icons.svg"
SKIP_DIRS = {".git", "node_modules", "vendor"}
EXTERNAL = re.compile(r"^(https?:|mailto:|data:|javascript:|tel:|//)", re.I)

errors = []


def err(msg):
    errors.append(msg)


def rel(p):
    return str(p.relative_to(ROOT))


def files(suffixes, base=ROOT):
    for p in sorted(base.rglob("*")):
        if any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts):
            continue
        if p.is_file() and p.suffix in suffixes:
            yield p


# --- 1. Markdown ------------------------------------------------------------

def strip_code(text):
    text = re.sub(r"(?ms)^(```|~~~).*?^\1", "", text)
    return re.sub(r"`[^`\n]*`", "", text)


def slugs(md_path, cache={}):
    if md_path not in cache:
        out, counts = set(), {}
        for line in strip_code(md_path.read_text()).splitlines():
            m = re.match(r"^#{1,6}\s+(.*?)\s*#*\s*$", line)
            if not m:
                continue
            s = re.sub(r"[^\w\- ]", "", m.group(1).strip().lower()).replace(" ", "-")
            n = counts.get(s, 0)
            counts[s] = n + 1
            out.add(s if n == 0 else "%s-%d" % (s, n))
        for m in re.finditer(r'<a\s+(?:name|id)="([^"]+)"', md_path.read_text()):
            out.add(m.group(1))
        cache[md_path] = out
    return cache[md_path]


def check_markdown():
    count = 0
    for md in files({".md"}):
        text = strip_code(md.read_text())
        for m in re.finditer(r"!?\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)", text):
            target = m.group(1)
            if EXTERNAL.match(target):
                continue
            count += 1
            path, _, anchor = target.partition("#")
            dest = (md.parent / unquote(path)).resolve() if path else md
            if not dest.exists():
                err("%s: link to missing %s" % (rel(md), target))
                continue
            if anchor and dest.suffix == ".md" and anchor not in slugs(dest):
                err("%s: link to %s, but %s has no heading #%s" % (rel(md), target, rel(dest), anchor))
    return count


# --- 2. Preview -------------------------------------------------------------

def sprite_ids():
    return set(re.findall(r'<symbol\b[^>]*\bid="([^"]+)"', SPRITE.read_text()))


def check_preview(ids):
    count = 0
    for f in list(files({".html", ".css", ".js"}, PREVIEW)):
        text = f.read_text()
        refs = []
        if f.suffix == ".html":
            refs += re.findall(r'\b(?:href|src|data-logo-dark|data-logo-light)="([^"]+)"', text)
            for tag in re.findall(r"<(?:link|script)\b[^>]*>", text):
                for u in re.findall(r'\b(?:href|src)="([^"]+)"', tag):
                    if EXTERNAL.match(u):
                        err("%s: loads %s from another host; vendor it under preview/vendor/" % (rel(f), u))
        if f.suffix in (".css", ".html"):
            for u in re.findall(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", re.sub(r"/\*.*?\*/", "", text, flags=re.S)):
                if EXTERNAL.match(u) and not u.startswith("data:"):
                    err("%s: url(%s) loads from another host" % (rel(f), u))
                refs.append(u)
        for r in refs:
            if EXTERNAL.match(r) or r.startswith("#") or "{" in r or "${" in r:
                continue
            count += 1
            path, _, frag = r.partition("#")
            path = path.split("?")[0]
            dest = (f.parent / unquote(path)).resolve()
            if not dest.exists():
                err("%s: %s does not exist" % (rel(f), r))
                continue
            try:
                inside = dest.relative_to(PREVIEW)
            except ValueError:
                inside = None
            if inside is None:
                top = dest.relative_to(DS).parts[0] if DS in dest.parents else None
                if top not in DEPLOYED_BESIDE_PREVIEW:
                    err("%s: %s leaves preview/ for %s, which the live preview does not deploy "
                        "(only %s are copied beside it)" % (rel(f), r, rel(dest), ", ".join(DEPLOYED_BESIDE_PREVIEW)))
            if dest == SPRITE and frag and frag not in ids:
                err("%s: icon #%s is not in core-icons.svg" % (rel(f), frag))
    return count


# --- 3. Icons ---------------------------------------------------------------

def check_icons(ids):
    used = set()
    for f in files({".md", ".html", ".js", ".css", ".svg"}):
        for m in re.finditer(r"core-icons\.svg#([A-Za-z0-9_-]+)", f.read_text()):
            used.add(m.group(1))
            if m.group(1) not in ids:
                err("%s: core-icons.svg#%s is not in the sprite" % (rel(f), m.group(1)))
    icons_md = (DS / "ICONS.md").read_text()
    gallery = (PREVIEW / "index.html").read_text()
    for i in sorted(ids):
        if not re.search(r"^- `%s` - " % re.escape(i), icons_md, re.M):
            err("ICONS.md: sprite icon `%s` is not listed under Canonical Icon Names" % i)
        if not re.search(r'class="icon-item"><svg[^>]*><use href="\.\./icons/core-icons\.svg#%s"' % re.escape(i), gallery):
            err("preview/index.html: sprite icon `%s` is missing from the icon gallery" % i)
    for i in re.findall(r"^- `([a-z0-9-]+)` - ", icons_md, re.M):
        if i not in ids:
            err("ICONS.md lists `%s`, which the sprite does not define" % i)
    return len(ids)


# --- 4. Logos ---------------------------------------------------------------

def check_logos():
    logos = DS / "logos"
    logos_md = (DS / "LOGOS.md").read_text()
    gallery = (PREVIEW / "index.html").read_text()
    names = sorted(p.name for p in logos.iterdir() if p.is_file())
    for n in names:
        if "logos/%s" % n not in logos_md:
            err("LOGOS.md: logos/%s is not documented" % n)
        if "../logos/%s" % n not in gallery:
            err("preview/index.html: logos/%s is not shown" % n)
    for f in files({".md"}):
        for n in re.findall(r"logos/([A-Za-z0-9_.-]+\.(?:svg|png))", f.read_text()):
            if n not in names:
                err("%s: names logos/%s, which does not exist" % (rel(f), n))
    return len(names)


# --- 5. Fonts ---------------------------------------------------------------

def check_fonts():
    sheet = DS / "fonts" / "fonts.css"
    text = re.sub(r"/\*.*?\*/", "", sheet.read_text(), flags=re.S)
    families = set(re.findall(r'font-family:\s*"([^"]+)"', text))
    if families != {"Nebula Sans", "Hack"}:
        err("fonts/fonts.css declares %s; Flag ships exactly Nebula Sans and Hack" % sorted(families))
    urls = re.findall(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", text)
    for u in urls:
        if EXTERNAL.match(u):
            err("fonts/fonts.css: %s loads from another host" % u)
        elif not (sheet.parent / u).resolve().exists():
            err("fonts/fonts.css: %s does not exist" % u)
    for lic in ("nebula-sans/OFL.txt", "hack/LICENSE.md"):
        if not (DS / "fonts" / lic).exists():
            err("fonts/%s is missing; the licence must travel with the binaries" % lic)
    return len(urls)


def main():
    ids = sprite_ids()
    n_md = check_markdown()
    n_prev = check_preview(ids)
    n_icons = check_icons(ids)
    n_logos = check_logos()
    n_fonts = check_fonts()
    if errors:
        for e in errors:
            print("ERROR: " + e, file=sys.stderr)
        print("check-refs: %d broken reference(s)" % len(errors), file=sys.stderr)
        return 1
    print("check-refs: ok (%d markdown links, %d preview refs, %d icons, %d logos, %d font files)"
          % (n_md, n_prev, n_icons, n_logos, n_fonts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
