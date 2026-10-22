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
6. Docs do not prescribe pairs the contrast check rejects: no CSS example
   puts a label on raw --color-primary / --gradient-action-primary or uses
   --color-secondary as a link color, and no prose asks for white text on the
   raw primary. (Lines that say "never"/"not"/"decorative" are warnings and
   are allowed.)
8. components.css: every infinite animation has a prefers-reduced-motion
   override that stops it, and the code well (.tool-call-code) paints only
   var(--color-surface-inset), the background the syntax contrast is
   measured on.
9. Component coverage, so components.css implements what COMPONENTS.md
   documents: every class the doc names (backticked `.class` or a class in
   an example's markup) has a selector; every interactive control has its
   hover, focus-visible, active and disabled states (INTERACTION_STATES);
   every documented component state has its selector (DOCUMENTED_STATES);
   and every vendored flatpickr rule that hard-codes a color is overridden
   by a token rule that applies wherever it does, so no vendor color shows
   through in either theme.
7. The preview's components.css is a byte copy of
   design-system/components/components.css (refresh with
   design-system/sync-preview.sh).

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


REJECTED_IN_DOCS = [
    (re.compile(r"background(-color)?:\s*var\(--gradient-action-primary\)"),
     "a label on --gradient-action-primary (4.46:1); use --gradient-action-fill + --color-on-primary-fill"),
    (re.compile(r"background(-color)?:\s*var\(--color-primary\)"),
     "a fill of raw --color-primary; use --color-primary-fill + --color-on-primary-fill"),
    (re.compile(r"(?<![-\w])color:\s*var\(--color-secondary\)"),
     "--color-secondary as a text/link color (2.7-3.6:1 in dark); use --color-link"),
    (re.compile(r"solid\s+`?(var\()?(--color-primary|color\.primary)\)?`?(?!-)[^\n]{0,40}white", re.I),
     "white text on raw primary (4.46:1); use --color-primary-fill + --color-on-primary-fill"),
    (re.compile(r"links?[^\n]{0,40}default to `?(color\.secondary|--color-secondary)", re.I),
     "--color-secondary as the default link color; use --color-link"),
]
WARNING_WORDS = re.compile(r"\b(never|not|no label|decorative|don't|do not|instead of|was|were)\b", re.I)


def check_docs_pairs():
    for md in files({".md"}):
        for n, line in enumerate(md.read_text().splitlines(), 1):
            if WARNING_WORDS.search(line):
                continue
            for pattern, why in REJECTED_IN_DOCS:
                if pattern.search(line):
                    err("%s:%d prescribes %s" % (rel(md), n, why))


def check_preview_copy():
    canon = DS / "components" / "components.css"
    copy = PREVIEW / "components.css"
    if not canon.exists():
        err("design-system/components/components.css is missing")
    elif not copy.exists() or copy.read_bytes() != canon.read_bytes():
        err("design-system/preview/components.css differs from design-system/components/components.css; "
            "run sh design-system/sync-preview.sh")


def css_rules(text):
    """(selector, body, inside_reduced_motion) for every leaf rule."""
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    out = []

    def walk(s, reduced):
        i = 0
        while True:
            j = s.find("{", i)
            if j < 0:
                return
            sel = s[i:j].strip()
            depth, k = 1, j + 1
            while depth:
                depth += {"{": 1, "}": -1}.get(s[k], 0)
                k += 1
            body = s[j + 1:k - 1]
            if sel.startswith("@media") or sel.startswith("@supports"):
                walk(body, reduced or "prefers-reduced-motion: reduce" in sel)
            elif not sel.startswith("@keyframes"):
                out.append((" ".join(sel.split()), body, reduced))
            i = k
    walk(text, False)
    return out


def check_components():
    comp = DS / "components" / "components.css"
    if not comp.exists():
        return
    rules = css_rules(comp.read_text())
    stopped = set()
    for sel, body, reduced in rules:
        if reduced and re.search(r"animation(-name)?\s*:\s*none", body):
            stopped.update(s.strip() for s in sel.split(","))
    for sel, body, reduced in rules:
        if reduced:
            continue
        if re.search(r"animation\s*:[^;]*\binfinite\b|animation-iteration-count\s*:\s*infinite", body):
            for s in sel.split(","):
                if s.strip() not in stopped:
                    err("components.css: `%s` animates forever with no prefers-reduced-motion "
                        "override setting `animation: none`" % s.strip())
        if ".tool-call-code" in sel:
            for m in re.finditer(r"background(-color)?\s*:\s*([^;]+)", body):
                if m.group(2).strip() != "var(--color-surface-inset)":
                    err("components.css: `%s` paints the code well with %s; use var(--color-surface-inset), "
                        "the background check_tokens.py measures syntax colors on" % (sel, m.group(2).strip()))


# Classes COMPONENTS.md names that are hooks, not styles.
DOC_CLASS_HOOKS = {"language-python", "featured"}

# Interactive controls and the states INTERACTION_ACCESSIBILITY.md requires
# ("Every interactive control must define all of hover, focus-visible,
# active, disabled where applicable"). A state may be met by a selector on a
# wrapper that styles the control (e.g. .ds-checkbox-input:focus-visible).
INTERACTION_STATES = {
    ".btn": ["hover", "focus-visible", "active", "disabled"],
    ".icon-action": ["hover", "focus-visible", "active", "disabled"],
    ".number-input__btn": ["hover", "focus-visible", "active", "disabled"],
    ".dropzone-browse-btn": ["hover", "focus-visible", "active", "disabled"],
    ".seg-option": ["hover", "focus-visible", "active", "disabled"],
    ".pill-btn": ["hover", "focus-visible", "active", "aria-disabled"],
    ".picker-icon-btn": ["hover", "focus-visible", "active"],
    ".switch": ["hover", "focus-visible", "active"],
    ".chip": ["hover", "active", "focus-visible"],
    ".chip-toggle": ["focus-visible"],
    ".chip-delete": ["hover", "focus-visible", "active"],
    ".link-tile": ["hover", "focus-visible", "active"],
    ".featured-link": ["hover", "focus-visible", "active", "disabled"],
    ".ds-accordion summary": ["hover", "focus-visible", "active"],
    ".ds-checkbox-input": ["checked", "focus-visible", "disabled"],
    # .theme-toggle is always also .btn or .icon-action, which carry its states.
    "input": ["focus-visible", "disabled"],
    "select": ["focus-visible", "disabled"],
    "textarea": ["focus-visible", "disabled"],
}
STATE_PATTERNS = {
    "hover": r":hover", "focus-visible": r":focus-visible|:focus-within", "active": r":active",
    "disabled": r":disabled|\[aria-disabled=\"true\"\]|\.is-disabled", "aria-disabled": r"\[aria-disabled=\"true\"\]",
    "checked": r":checked",
}

# States COMPONENTS.md lists for a component, with the selector that
# implements each (the doc names these selectors next to the state).
DOCUMENTED_STATES = [
    ".file-upload-dropzone:hover", ".file-upload-dropzone.is-dragover", ".file-item.uploading",
    ".file-item.uploaded", ".file-item.error", ".featured-link.is-selected", ".featured-link[aria-current=\"true\"]",
    ".featured-link.is-disabled", ".chip.selected", ".ds-accordion details[open] summary::after",
    "input[aria-invalid=\"true\"]", "input.is-warning", ".field-error", ".field-warning", ".field-hint",
    ".seg-option[aria-pressed=\"true\"]", ".seg-option[aria-checked=\"true\"]", ".seg-option[aria-selected=\"true\"]",
    ".switch[aria-checked=\"true\"]", ".picker-row--active", ".picker-row--dimmed .picker-row__name",
    ".state-panel--ok", ".state-panel--warn", ".state-panel--deny", ".kicker--ok", ".kicker--warn", ".kicker--deny",
    ".task-tracker-item.status-done .tt-title", ".task-tracker-item.status-inprogress .tt-title",
    ".badge-pending", ".badge-scheduled", ".badge-assigned", ".badge-leased", ".badge-running", ".badge-analyzing",
    ".badge-success", ".badge-warning", ".badge-danger", ".badge-cancelled",
    "[data-theme=\"light\"] .theme-toggle__icon--sun", "[data-theme=\"light\"] .theme-toggle__icon--moon",
]


def split_selectors(sel):
    parts, depth, cur = [], 0, ""
    for ch in sel:
        depth += {"(": 1, ")": -1, "[": 1, "]": -1}.get(ch, 0)
        if ch == "," and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    return [" ".join(p.split()) for p in parts + [cur] if p.strip()]


def selector_list(css_text):
    sels = []
    for sel, _body, _reduced in css_rules(css_text):
        sels += split_selectors(sel)
    return sels


def check_component_coverage():
    comp = DS / "components" / "components.css"
    if not comp.exists():
        return
    css = comp.read_text()
    sels = selector_list(css)
    joined = "\n".join(sels)
    classes = set(re.findall(r"\.([A-Za-z][\w-]*)", joined))

    # Documented classes.
    md = strip_code((DS / "COMPONENTS.md").read_text())
    raw_md = (DS / "COMPONENTS.md").read_text()
    documented = set(re.findall(r"`\.([A-Za-z][\w-]*)", raw_md))
    for m in re.finditer(r'class="([^"]+)"', raw_md):
        documented.update(m.group(1).split())
    for c in sorted(documented - classes - DOC_CLASS_HOOKS):
        err("COMPONENTS.md documents `.%s`, but components.css has no selector for it" % c)

    # Interaction states.
    for base, states in INTERACTION_STATES.items():
        for state in states:
            pat = re.compile(r"(^|[\s,>+~(])" + re.escape(base) + r"(?![\w-])[^\s,]*?(" + STATE_PATTERNS[state] + ")")
            if not any(pat.search(re.sub(r":not\((?:[^()]|\([^()]*\))*\)", "", s)) for s in sels):
                err("components.css: `%s` has no %s state (INTERACTION_ACCESSIBILITY.md)" % (base, state))

    # Documented component states.
    for s in DOCUMENTED_STATES:
        if s not in sels:
            err("components.css: no `%s` rule for a state COMPONENTS.md documents" % s)

    # Vendored flatpickr colors are overridden.
    vendor = PREVIEW / "vendor" / "flatpickr" / "flatpickr.min.css"
    if vendor.exists():
        check_vendor_overrides(vendor.read_text(), css)


FAMILY = [("color", r"^color$"), ("background", r"^background(-color|-image)?$"),
          ("border", r"^border(-(top|right|bottom|left))?(-color)?$"), ("fill", r"^fill$"), ("box-shadow", r"^box-shadow$")]


def family(prop):
    for name, pat in FAMILY:
        if re.match(pat, prop):
            return name
    return None


def subject(sel):
    """(all classes, subject tag, subject pseudo-classes, pseudo-element) of a selector."""
    plain = re.sub(r":(not|nth-child|nth-of-type|is|where)\([^)]*\)", "", sel)
    parts = re.split(r"\s*[\s>+~]\s*", plain.strip())
    last = parts[-1]
    tag = re.match(r"^([a-z]+)", last)
    pe = re.search(r"::?(before|after)\b", last)
    pcs = set(re.findall(r":(hover|focus|active|focus-visible|focus-within)\b", last))
    return set(re.findall(r"\.([\w-]+)", plain)), tag.group(1) if tag else None, pcs, pe.group(1) if pe else None


def check_vendor_overrides(vendor_css, comp_css):
    vendor_css = re.sub(r"/\*.*?\*/", "", vendor_css, flags=re.S)
    vendor_css = re.sub(r"@(-webkit-)?keyframes[^{]*\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}", "", vendor_css)
    ours = []
    for sel, body, _r in css_rules(comp_css):
        fams = {family(m.group(1)) for m in re.finditer(r"([\w-]+)\s*:[^;]*!important", body)}
        for s in split_selectors(sel):
            ours.append((subject(s), fams))
    for sel, body in re.findall(r"([^{}@]+)\{([^{}]*)\}", vendor_css):
        need = set()
        for m in re.finditer(r"([\w-]+)\s*:\s*([^;]+)", body):
            if re.search(r"#[0-9a-fA-F]{3,8}\b|rgba?\(", m.group(2)) and family(m.group(1)):
                need.add(family(m.group(1)))
        if not need:
            continue
        for s in split_selectors(sel):
            vc, vt, vp, ve = subject(s)
            for fam in need:
                covered = any(rc <= vc and (rt is None or rt == vt) and rp <= vp and re_ == ve and fam in fams
                              for (rc, rt, rp, re_), fams in ours)
                if not covered:
                    err("components.css: no !important token override of `%s` for vendored flatpickr `%s`" % (fam, s))


def main():
    check_component_coverage()
    check_components()
    check_docs_pairs()
    check_preview_copy()
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
