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
10. Doc paths: every `flag-sync.sh add <flag> <src> <dest>` example names a
   <src> that exists under design-system/ (flag-sync's paths are relative to
   it), and every repo path in inline code exists (product-repo paths such
   as scripts/flag-sync.sh are listed in check_doc_paths).
11. Snippet accessibility: every classed element in a doc's ```html snippet
   has the role, tabindex and aria-* attributes of the preview's live
   element with the same classes, so copied markup keeps the preview's
   keyboard and screen-reader behavior.
12. Focus: every interactive control's focus-visible rules paint a visible
   indicator, and the flatpickr cascade simulation also proves each day state
   (plain, today, in range, selected, range ends; any month) ends keyboard
   focus in its measured ring, different from the day at rest.
13. Two-part indicators: every rule that paints part of one (a -fill, a knob
   or thumb, a spinner's recolored border side) has its paint pinned in
   MEASURED_PAINT, so check_tokens.py's TWO_PART pairs measure what renders.

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


# The vendorable component stylesheets: components.css, and the opt-in
# shadcn/ui parity layer that builds on it. Every components.css check below
# runs over both, as one stylesheet, and the preview carries a byte copy of
# each.
COMPONENT_SHEETS = ("components.css", "shadcn-parity.css")


def component_css():
    """The component stylesheets joined in load order, or None if components.css is missing."""
    if not (DS / "components" / "components.css").exists():
        return None
    return "\n".join((DS / "components" / n).read_text() for n in COMPONENT_SHEETS
                     if (DS / "components" / n).exists())


def check_preview_copy():
    for name in COMPONENT_SHEETS:
        canon = DS / "components" / name
        copy = PREVIEW / name
        if not canon.exists():
            err("design-system/components/%s is missing" % name)
        elif not copy.exists() or copy.read_bytes() != canon.read_bytes():
            err("design-system/preview/%s differs from design-system/components/%s; "
                "run sh design-system/sync-preview.sh" % (name, name))


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
    css = component_css()
    if css is None:
        return
    rules = css_rules(css)
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
    ".switch": ["hover", "focus-visible", "active", "disabled"],
    ".chip": ["hover", "active", "focus-visible"],
    ".chip-toggle": ["focus-visible"],
    ".chip-delete": ["hover", "focus-visible", "active"],
    ".link-tile": ["hover", "focus-visible", "active"],
    ".featured-link": ["hover", "focus-visible", "active", "disabled"],
    ".ds-accordion summary": ["hover", "focus-visible", "active"],
    ".ds-checkbox-input": ["checked", "focus-visible", "disabled"],
    ".input-file-select input": ["checked", "focus-visible", "disabled"],
    ".selectable-item": ["hover", "focus-visible", "disabled"],
    ".number-input": ["focus-visible", "disabled"],
    ".file-upload-dropzone": ["hover", "disabled"],
    # .theme-toggle is always also .btn or .icon-action, which carry its states.
    "input": ["focus-visible", "disabled"],
    "select": ["focus-visible", "disabled"],
    "textarea": ["focus-visible", "disabled"],
    # shadcn/ui parity controls (Tier A twins of the @flag registry items).
    'input[type="radio"].ds-radio': ["hover", "checked", "focus-visible", "disabled"],
    ".tab": ["hover", "focus-visible", "active", "disabled"],
    ".menu-item": ["hover", "focus-visible", "active", "disabled"],
    ".command__item": ["hover", "aria-disabled"],
    "tr.is-interactive": ["hover", "focus-visible", "active"],
    ".scroll-area": ["focus-visible"],
}
# A focus-visible rule must paint something a sighted keyboard user can see.
FOCUS_PAINT = re.compile(r"(?:^|;)\s*(outline(?:-color)?|box-shadow|border(?:-color)?|background(?:-color)?|"
                         r"text-decoration(?:-line)?)\s*:\s*(?!(?:none|0|transparent)\b)[^\s;][^;]*")
STATE_PATTERNS = {
    "hover": r":hover", "focus-visible": r":focus-visible|:focus-within", "active": r":active",
    "disabled": r":disabled|\[aria-disabled=\"true\"\]|\.is-disabled", "aria-disabled": r"\[aria-disabled=\"true\"\]",
    "checked": r":checked",
}

# The text-field shell's input selector: every input except the native
# controls Flag does not redraw (zero specificity via :where()).
TEXT_INPUT = ('input:where(:not([type="checkbox"], [type="radio"], [type="range"], [type="color"], [type="file"], '
              '[type="submit"], [type="button"], [type="reset"], [type="image"], [type="hidden"]))')

# States COMPONENTS.md lists for a component, with the selector that
# implements each (the doc names these selectors next to the state).
DOCUMENTED_STATES = [
    ".file-upload-dropzone:hover", ".file-upload-dropzone.is-dragover", ".file-item.uploading",
    ".file-item.uploaded", ".file-item.error", ".featured-link.is-selected", ".featured-link[aria-current=\"true\"]",
    ".featured-link.is-disabled", ".chip.selected", ".ds-accordion details[open] summary::after",
    TEXT_INPUT + "[aria-invalid=\"true\"]", TEXT_INPUT + ".is-warning", ".field-error", ".field-warning", ".field-hint",
    ".seg-option[aria-pressed=\"true\"]", ".seg-option[aria-checked=\"true\"]", ".seg-option[aria-selected=\"true\"]",
    ".switch[aria-checked=\"true\"]", ".picker-row--active", ".picker-row--dimmed .picker-row__name",
    ".state-panel--ok", ".state-panel--warn", ".state-panel--deny", ".kicker--ok", ".kicker--warn", ".kicker--deny",
    ".task-tracker-item.status-done .tt-title", ".task-tracker-item.status-inprogress .tt-title",
    ".badge-pending", ".badge-scheduled", ".badge-assigned", ".badge-leased", ".badge-running", ".badge-analyzing",
    ".badge-success", ".badge-warning", ".badge-danger", ".badge-cancelled",
    "[data-theme=\"light\"] .theme-toggle__icon--sun", "[data-theme=\"light\"] .theme-toggle__icon--moon",
    # shadcn/ui parity (COMPONENTS.md "shadcn/ui (Tier B) Mapping").
    ".alert--info", ".alert--success", ".alert--warning", ".alert--destructive",
    ".toast--success > svg", ".toast--warning > svg", ".toast--error > svg", ".toast--info > svg",
    ".tab[aria-selected=\"true\"]", ".menu-item--destructive", ".command__item[aria-selected=\"true\"]",
    ".table-wrap tr[aria-selected=\"true\"]", ".sheet--right", ".sheet--left", ".sheet--top", ".sheet--bottom",
    ".avatar--sm", ".avatar--lg", ".separator--vertical", ".select-wrap--sm select",
    ".badge-default", ".badge-secondary", ".badge-outline", ".badge-accent",
    "input[type=\"radio\"].ds-radio:checked", "input[type=\"radio\"].ds-radio:disabled:checked",
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


# Non-text indicators: the rule that paints each one must use exactly the
# token check_tokens.py measures for it (WCAG 1.4.11, 3:1), so measured and
# rendered cannot drift apart. (selector, property, required value)
MEASURED_PAINT = [
    (".spinner", "border-top-color", "var(--color-link)"),
    (".spinner", "border", "2px solid var(--color-overlay-soft)"),
    (".btn-primary .spinner", "border-top-color", "var(--color-on-primary-fill)"),
    (".btn-primary .spinner", "border-color", "var(--color-primary-fill-hover)"),
    (".file-item-progress-fill", "background", "var(--color-link)"),
    (".file-item-progress", "background", "var(--color-overlay-strong)"),
    (".switch__knob", "background", "var(--color-switch-knob)"),
    (".ds-checkbox__box", "border", "1.5px solid var(--color-control-border)"),
    (".ds-checkbox-input:checked + .ds-checkbox .ds-checkbox__box", "border-color", "var(--color-accent)"),
    (".input-file-select input", "border", "1.5px solid var(--color-control-border)"),
    (".switch", "background", "var(--color-switch-track-off)"),
    ('.switch[aria-checked="true"]', "background", "var(--color-switch-track-on)"),
    ('.seg-option[aria-pressed="true"]', "background", "var(--color-primary-fill)"),
    (".flatpickr-day.inRange", "background", "var(--color-accent-strong) !important"),
    (".flatpickr-day.today", "box-shadow", "inset 0 0 0 1px var(--color-accent) !important"),
    ('[data-theme="light"] .flatpickr-day.selected', "background", "var(--color-primary-fill) !important"),
    (".flatpickr-day.selected", "background", "var(--gradient-action-fill) !important"),
    (".flatpickr-day:focus-visible", "box-shadow", "var(--focus-ring-day) !important"),
    (".flatpickr-day.inRange:focus-visible", "box-shadow", "var(--focus-ring-day-on-range) !important"),
    (".flatpickr-day.selected:focus-visible", "box-shadow", "var(--focus-ring-day-on-fill) !important"),
    # shadcn/ui parity indicators and fills (components/shadcn-parity.css).
    ('input[type="radio"].ds-radio', "border", "1.5px solid var(--color-control-border)"),
    ('.tab[aria-selected="true"]', "border-bottom-color", "var(--color-accent)"),
    ('.command__item[aria-selected="true"]', "box-shadow", "inset 0 0 0 1px var(--color-row-active-border)"),
    (".badge-default", "background", "var(--color-primary-fill)"),
    (".badge-default", "color", "var(--color-on-primary-fill)"),
    (".badge-accent", "background", "var(--color-accent)"),
    (".badge-accent", "color", "var(--flag-on-accent)"),
]


# Hover and pressed styles never apply to a disabled control: every :hover /
# :active in components.css carries this zero-specificity gate (so adding it
# never changes the cascade). Vendor widget parts (flatpickr) are exempt:
# their disabled days have explicit reset rules.
HOVER_GATE = ':where(:not(:disabled, [aria-disabled="true"], .is-disabled))'


def check_hover_gates(sels):
    for s in sels:
        if not re.search(r":(hover|active)\b", s):
            continue
        if "flatpickr" in s or "numInputWrapper" in s or re.search(r":has\([^)]*:disabled", s):
            continue
        for compound in re.split(r"\s+(?![^()]*\))", s):
            m = re.search(r":is\(:hover|:(hover|active)\b", compound)
            if m and HOVER_GATE not in compound[:m.start()]:
                err("components.css: `%s` applies :hover/:active without the disabled gate %s" % (s, HOVER_GATE))
                break


# components.css is vendored into products that also render third-party
# markup, so a rule on a bare element (no Flag class on it or an ancestor)
# must be safe for ANY instance of that element. Allowed bare rules and the
# only properties they may set:
BARE_SAFE = {
    "*": {"box-sizing"},
    "a": {"color"},
    "button": {"font"},
    "table": {"font-variant-numeric"},
}
# Native controls the text-field shell must never reach.
NON_TEXT_TYPES = ["checkbox", "radio", "range", "color", "file", "submit", "button", "reset", "image", "hidden"]
TEXT_TYPES = ["text", "search", "email", "password", "tel", "url", "number"]


def check_bare_elements(css_text):
    for sel, body, _r in css_rules(css_text):
        props = {m.group(1) for m in re.finditer(r"(?:^|;)\s*([\w-]+)\s*:", body)}
        for s in split_selectors(sel):
            core = s.replace('[data-theme="light"] ', "").replace("body.theme-light ", "")
            compounds = re.split(r"\s+(?![^()]*\))", core)
            subject = compounds[-1]
            if re.match(r"^[.#\[:]", subject) or "." in re.sub(r":where\([^)]*\)|:not\([^)]*\)", "", subject):
                continue  # Flag class on the subject itself
            if any("." in c for c in compounds[:-1]):
                continue  # inside a Flag-classed ancestor
            tag = re.match(r"^([a-z]+|\*)", subject)
            if not tag:
                continue
            tag = tag.group(1)
            if "::" in subject and tag in ("input", "textarea"):
                continue  # ::placeholder and vendor pseudo-elements: text fields only
            appearance = "appearance" in props or "-webkit-appearance" in props
            if tag == "input":
                if appearance:
                    if not all('[type="%s"]' % ty in subject for ty in TEXT_TYPES) and '[type="' not in subject:
                        err("components.css: `%s` sets appearance: none on unqualified inputs" % s)
                    if any('[type="%s"]' % ty in subject and ":not(" not in subject for ty in NON_TEXT_TYPES):
                        err("components.css: `%s` removes native appearance from a non-text input type" % s)
                    continue
                if props <= {"font"}:
                    continue
                if not all('[type="%s"]' % ty in subject for ty in NON_TEXT_TYPES):
                    err("components.css: `%s` reaches non-text inputs (checkbox, radio, range, file, ...); "
                        "exclude them with :where(:not([type=...]))" % s)
                continue
            if tag == "select":
                if props & {"display", "width", "height", "min-height", "padding", "border", "background"} \
                        and ":not([multiple])" not in subject:
                    err("components.css: `%s` gives the field shell to multi-selects; exclude [multiple]" % s)
                continue
            if tag == "textarea":
                continue
            allowed = BARE_SAFE.get(tag)
            if allowed is None:
                err("components.css: bare `%s` rule is not safe for third-party markup; scope it to a Flag class" % s)
            elif not props <= allowed:
                err("components.css: bare `%s` sets %s; only %s is safe for any instance of <%s>"
                    % (s, ", ".join(sorted(props - allowed)), ", ".join(sorted(allowed)), tag))


def check_appearance_disabled(css_text, sels):
    """A control that drops its native appearance must draw its own disabled state."""
    for sel, body, _r in css_rules(css_text):
        if not re.search(r"appearance\s*:\s*none", body):
            continue
        for s in split_selectors(sel):
            if "::" in s:
                continue
            if "." not in s and '[type="' not in s:
                err("components.css: `%s` removes native appearance without a Flag class or a type qualifier" % s)
                continue
            last = re.split(r"\s+", s)[-1]
            tag = re.match(r"^[a-z]+", last)
            classes = set(re.findall(r"\.([\w-]+)", s))
            ok = False
            for d in sels:
                if not re.search(r":disabled|\[aria-disabled|\.is-disabled", d):
                    continue
                dl = re.split(r"\s+(?![^()]*\))", d)
                subj = next((c for c in reversed(dl) if re.search(r":disabled|\[aria-disabled|\.is-disabled", c)), dl[-1])
                dtag = re.match(r"^[a-z]+", subj)
                dclasses = set(re.findall(r"\.([\w-]+)", re.sub(r":not\([^)]*\)", "", d)))
                if (tag and dtag and dtag.group(0) == tag.group(0) or not tag) and dclasses <= classes | {"is-disabled"}:
                    ok = True
                    break
            if not ok:
                err("components.css: `%s` removes native appearance but has no disabled state" % s)


def check_flatpickr_cascade(css_text):
    """Simulate the cascade for every day-state x modifier combination.

    A selected / range-end day must keep --color-on-primary-fill on its fill,
    an in-range day --color-on-accent-strong on --color-accent-strong,
    whatever else it is (a neighbouring month's day, today), hovered,
    focused or not, in both themes.
    """
    import itertools
    rules = []
    for order, (sel, body, _r) in enumerate(css_rules(css_text)):
        decls = {}
        for m in re.finditer(r"([\w-]+)\s*:\s*([^;]+?)\s*!important", body):
            decls[m.group(1)] = " ".join(m.group(2).split())
        if not decls:
            continue
        for s in split_selectors(sel):
            if "flatpickr-day" not in s or " " in s.replace('[data-theme="light"] ', "") or "::" in s:
                continue
            light = s.startswith('[data-theme="light"] ')
            core = s.replace('[data-theme="light"] ', "")
            if re.search(r":(not|nth|is|where)\(", core):
                continue
            classes = set(re.findall(r"\.([\w-]+)", core))
            pseudos = set(re.findall(r":(hover|focus-visible|focus)(?![\w-])", core))
            spec = len(classes) + len(pseudos) + (1 if light else 0)
            rules.append((classes, pseudos, light, spec, order, decls))

    def winner(classes, pseudos, light, prop):
        best = None
        for rc, rp, rl, spec, order, decls in rules:
            if prop not in decls or not rc <= classes or not rp <= pseudos or (rl and not light):
                continue
            if best is None or (spec, order) >= (best[0], best[1]):
                best = (spec, order, decls[prop])
        return best[2] if best else None

    expect = {
        "selected": ("var(--color-on-primary-fill)", {False: "var(--gradient-action-fill)", True: "var(--color-primary-fill)"}),
        "startRange": ("var(--color-on-primary-fill)", {False: "var(--gradient-action-fill)", True: "var(--color-primary-fill)"}),
        "endRange": ("var(--color-on-primary-fill)", {False: "var(--gradient-action-fill)", True: "var(--color-primary-fill)"}),
        "inRange": ("var(--color-on-accent-strong)", {False: "var(--color-accent-strong)", True: "var(--color-accent-strong)"}),
    }
    mods = ["prevMonthDay", "nextMonthDay", "today"]
    # Keyboard focus matches :focus and :focus-visible together; it must end
    # in the ring measured for the day's fill, and differ from the day at rest.
    kbd = {"focus", "focus-visible"}
    rings = {"selected": "var(--focus-ring-day-on-fill)", "startRange": "var(--focus-ring-day-on-fill)",
             "endRange": "var(--focus-ring-day-on-fill)", "inRange": "var(--focus-ring-day-on-range)",
             None: "var(--focus-ring-day)"}
    for state, ring in rings.items():
        for n in range(len(mods) + 1):
            for combo in itertools.combinations(mods, n):
                if "prevMonthDay" in combo and "nextMonthDay" in combo:
                    continue
                for light in (False, True):
                    cls = {"flatpickr-day", *combo} | ({state} if state else set())
                    where = "%s (%s)" % ("".join("." + c for c in sorted(cls)), "light" if light else "dark")
                    rest = winner(cls, set(), light, "box-shadow")
                    for pseudo in (kbd, kbd | {"hover"}):
                        got = winner(cls, pseudo, light, "box-shadow")
                        if got != ring:
                            err("components.css: flatpickr day %s:%s ends up box-shadow %s, expected the "
                                "measured focus ring %s" % (where, ":".join(sorted(pseudo)), got, ring))
                        elif got == rest:
                            err("components.css: flatpickr day %s looks the same focused and at rest" % where)
    for state, (color, bgs) in expect.items():
        for n in range(len(mods) + 1):
            for combo in itertools.combinations(mods, n):
                if "prevMonthDay" in combo and "nextMonthDay" in combo:
                    continue
                for pseudo in (set(), {"hover"}, {"focus"}, kbd, kbd | {"hover"}):
                    for light in (False, True):
                        cls = {"flatpickr-day", state, *combo}
                        got_c = winner(cls, pseudo, light, "color")
                        got_b = winner(cls, pseudo, light, "background")
                        where = "%s.%s%s (%s)" % ("".join("." + c for c in sorted(cls - {state})), state,
                                                 "".join(":" + p for p in pseudo), "light" if light else "dark")
                        if got_c != color:
                            err("components.css: flatpickr day %s ends up color %s, expected %s" % (where, got_c, color))
                        if got_b != bgs[light]:
                            err("components.css: flatpickr day %s ends up background %s, expected %s"
                                % (where, got_b, bgs[light]))


def check_doc_paths():
    """Command and path examples in the docs must point at real files.

    - `flag-sync.sh add <flag-dir> <flag-path> <repo-path>`: flag-sync reads
      <flag-path> relative to Flag's design-system/, so it must exist there.
    - Inline-code paths into this repo (design-system/..., scripts/...,
      docs/..., .github/...) must exist; in design-system/*.md a path that
      starts with one of its subdirectories (tokens/, fonts/, ...) is
      relative to design-system/ and must exist there.
    """
    subdirs = sorted(p.name for p in DS.iterdir() if p.is_dir())
    # Paths that live in a *product* repo (flag-sync's installed copy, the
    # drift workflow, the lock file), not in Flag itself.
    product_paths = {"scripts/flag-sync.sh", "scripts/stack-check.sh",
                     ".github/workflows/flag-drift.yml", "flag.lock"}
    for md in files({".md"}):
        text = md.read_text()
        for m in re.finditer(r"flag-sync\.sh\s+add\s+(\S+)\s+(\S+)\s+(\S+)", text):
            src = m.group(2).strip("`")
            if src.startswith("<"):
                continue
            if not (DS / src).exists():
                err("%s: `flag-sync.sh add ... %s ...` names design-system/%s, which does not exist "
                    "(flag-sync paths are relative to design-system/)" % (rel(md), src, src))
        for m in re.finditer(r"`([^`\s]+)`", text):
            token = m.group(1).rstrip(".,;:")
            if "*" in token or "{" in token or "<" in token or token.startswith(("http", "/", "../", "./")):
                continue
            if token in product_paths:
                continue
            if re.match(r"^(design-system|scripts|docs|tools|\.github)/[\w./-]+$", token):
                if not (ROOT / token).exists():
                    err("%s: `%s` does not exist" % (rel(md), token))
            elif md.parent == DS and re.match(r"^(%s)/[\w./-]+\.\w+$" % "|".join(map(re.escape, subdirs)), token):
                if not (DS / token).exists():
                    err("%s: `%s` (relative to design-system/) does not exist" % (rel(md), token))


def check_snippet_a11y():
    """Each HTML snippet in the docs carries the same accessibility
    attributes as the preview's live element of the same classes.

    For every classed element in a snippet, some preview element with all of
    those classes must have the same role, the same tabindex and the same set
    of aria-* attributes (values of state attributes like aria-pressed may
    differ; their presence may not). A snippet that drops tabindex/role/
    aria-label from a scroll container, or a toggle's aria-pressed, fails.
    """
    from html.parser import HTMLParser

    class Collect(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.els = []

        def handle_starttag(self, tag, attrs):
            a = {k: (v or "") for k, v in attrs}
            if a.get("class"):
                self.els.append((tag, a))

        handle_startendtag = handle_starttag

    def sig(tag, a):
        return (tag, a.get("role"), a.get("tabindex"), tuple(sorted(k for k in a if k.startswith("aria-"))))

    live = Collect()
    live.feed((PREVIEW / "index.html").read_text())
    for path in sorted(set(files({".md"}))):
        check_snippets_in(path, live, Collect, sig)


def check_snippets_in(path, live, Collect, sig):
    md = path.read_text()
    for block in re.finditer(r"```html\n(.*?)```", md, re.S):
        doc = Collect()
        doc.feed(block.group(1))
        for tag, a in doc.els:
            classes = set(a["class"].split())
            peers = [(t, b) for t, b in live.els if classes <= set(b["class"].split())]
            label = "<%s class=\"%s\">" % (tag, a["class"])
            if not peers:
                err("%s: snippet element %s has no counterpart in preview/index.html" % (rel(path), label))
                continue
            if sig(tag, a) not in {sig(t, b) for t, b in peers}:
                t, b = peers[0]
                _, role, tabindex, aria = sig(t, b)
                err("%s: snippet element %s has role=%s tabindex=%s %s, but the preview's has "
                    "role=%s tabindex=%s %s" % (rel(path), label, a.get("role"), a.get("tabindex"),
                                                list(sig(tag, a)[3]), role, tabindex, list(aria)))


def check_dependabot():
    """Dependabot's commit messages follow the repo's gitmoji convention."""
    f = ROOT / ".github" / "dependabot.yml"
    if not f.exists():
        return
    for m in re.finditer(r'prefix:\s*"([^"]*)"', f.read_text()):
        if not m.group(1) or ord(m.group(1)[0]) < 0x2000:
            err('.github/dependabot.yml: commit-message prefix "%s" is not a gitmoji (AGENTS.md)' % m.group(1))


# Parts of two-part indicators (a fill on a track, a knob or thumb on a
# track, an arc on a ring): their paints must be pinned in MEASURED_PAINT so
# check_tokens.py measures part against track (TWO_PART), not just against
# the surface. Recognized by class name, or by the spinner pattern (a border
# with one side recolored).
TWO_PART_CLASS = re.compile(r"\.[\w-]*(-fill|__knob|__thumb|__arc|-track|__track)$")


def check_two_part(css_text):
    pinned = {sel for sel, _p, _v in MEASURED_PAINT}
    for sel, body, _r in css_rules(css_text):
        arc = re.search(r"(?:^|;)\s*border\s*:[^;]*solid", body) and \
            re.search(r"(?:^|;)\s*border-(top|right|bottom|left)-color\s*:", body)
        if not re.search(r"(?:^|;)\s*(background(-color)?|border(-[a-z]+)*|fill|stroke)\s*:", body):
            continue  # size or position only
        for one in split_selectors(sel):
            if one.startswith(('[data-theme="light"] ', "body.theme-light ")):
                continue
            subject = re.split(r"\s+", one)[-1]
            if (arc or TWO_PART_CLASS.search(subject)) and re.fullmatch(r"[.\w-]+", subject) \
                    and one not in pinned:
                err("components.css: `%s` paints part of a two-part indicator; pin its paint in MEASURED_PAINT and "
                    "measure it against its track in check_tokens.py TWO_PART" % one)


def check_measured_paint(css_text):
    rules = [(split_selectors(sel), body) for sel, body, _r in css_rules(css_text)]
    for sel, prop, value in MEASURED_PAINT:
        found = False
        for sels, body in rules:
            if sel in sels:
                for m in re.finditer(r"(?:^|;)\s*" + re.escape(prop) + r"\s*:\s*([^;]+)", body):
                    found = True
                    if " ".join(m.group(1).split()) != value:
                        err("components.css: `%s { %s: %s }` but check_tokens.py measures %s"
                            % (sel, prop, " ".join(m.group(1).split()), value))
        if not found:
            err("components.css: no `%s { %s }` rule (expected %s)" % (sel, prop, value))


def selector_list(css_text):
    sels = []
    for sel, _body, _reduced in css_rules(css_text):
        sels += split_selectors(sel)
    return sels


def check_component_coverage():
    css = component_css()
    if css is None:
        return
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

    # Interaction states (the hover gate itself says ":disabled"; ignore it).
    sels_nogate = [s.replace(HOVER_GATE, "") for s in sels]
    for base, states in INTERACTION_STATES.items():
        for state in states:
            pat = re.compile(r"(^|[\s,>+~(])" + re.escape(base) + r"(?![\w-])[^\s,]*?(" + STATE_PATTERNS[state] + ")")
            if not any(pat.search(re.sub(r":not\((?:[^()]|\([^()]*\))*\)", "", s)) for s in sels_nogate):
                err("components.css: `%s` has no %s state (INTERACTION_ACCESSIBILITY.md)" % (base, state))
            elif state == "focus-visible" and not any(
                    FOCUS_PAINT.search(body) for sel, body, _r in css_rules(css)
                    for one in split_selectors(sel)
                    if pat.search(re.sub(r":not\((?:[^()]|\([^()]*\))*\)", "", one.replace(HOVER_GATE, "")))):
                err("components.css: `%s`'s focus-visible rules paint no visible indicator (outline, box-shadow, "
                    "border-color, background or text-decoration other than none)" % base)

    # Light theme paints filled selections solid (TOKENS.md "Filled
    # controls"): every rule that paints --gradient-action-fill needs a
    # [data-theme="light"] twin painting --color-primary-fill.
    for sel, body, _r in css_rules(css):
        if re.search(r"background(-image)?\s*:\s*var\(--gradient-action-fill\)", body):
            for s in split_selectors(sel):
                twin = '[data-theme="light"] ' + s
                if twin not in sels:
                    err("components.css: `%s` paints --gradient-action-fill but has no `%s` rule with the solid "
                        "--color-primary-fill" % (s, twin))

    # Every light-theme rule also answers the legacy body.theme-light class,
    # which the token sheet honours (`:root[data-theme="light"],
    # body.theme-light`): otherwise a legacy page gets light tokens but the
    # dark component overrides (white-on-gradient primary, dark selected days).
    for s_ in sels:
        if s_.startswith('[data-theme="light"] '):
            twin = "body.theme-light " + s_[len('[data-theme="light"] '):]
            if twin not in sels:
                err("components.css: `%s` has no legacy twin `%s` in its selector list (the token sheet's light "
                    "theme also applies under body.theme-light)" % (s_, twin))
    if "body.theme-light" not in (DS / "tokens" / "design-tokens.css").read_text():
        err("design-tokens.css no longer honours body.theme-light; drop the legacy twins from components.css too")

    # Documented component states.
    for s in DOCUMENTED_STATES:
        if s not in sels_nogate:
            err("components.css: no `%s` rule for a state COMPONENTS.md documents" % s)

    check_measured_paint(css)
    check_two_part(css)
    check_hover_gates(sels)
    check_bare_elements(css)
    check_appearance_disabled(css, sels_nogate)
    check_flatpickr_cascade(css)

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
    check_dependabot()
    check_doc_paths()
    check_snippet_a11y()
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
