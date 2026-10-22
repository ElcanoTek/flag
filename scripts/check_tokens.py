#!/usr/bin/env python3
"""Check tokens/design-tokens.json against tokens/design-tokens.css, and the
palette's contrast.

1. Consistency. Every token in one file exists in the other with the same
   value, for the dark (:root) set and the light overrides. JSON paths map to
   CSS names by rule (color.text.primary -> --color-text-primary) plus the
   short alias table below for the names that predate the rule. Values are
   compared after normalising case and spacing and, when they still differ,
   after resolving var() references, so `"onSuccess": "#000000"` matches
   `--color-on-success: var(--color-black)`.

2. Contrast. The pairs in CONTRAST are measured in both themes (WCAG 2;
   translucent colors composited over the surface they sit on). A pair below
   its floor fails; there are no exceptions. Gradients that carry a label are
   measured at every point of the blend.

Usage: python3 scripts/check_tokens.py
"""

import json
import re
import sys

from flagtokens import TOKENS_CSS, TOKENS_JSON, ColorError, contrast, over, resolve, themes

# JSON path -> CSS name, for names that predate the mapping rule.
ALIASES = {
    "color.background": "--color-bg",
    "color.surface.default": "--color-surface-1",
    "color.surface.elevated": "--color-surface-2",
    "color.border.default": "--color-border",
    "font.size.bodyLarge": "--font-size-body-lg",
    "font.size.bodyMedium": "--font-size-body-md",
    "font.lineHeight.bodyLarge": "--line-height-body-lg",
    "shadow.focusRingPicker": "--focus-ring-picker",
    "themes.contract.storageKey": "--theme-preference-storage-key",
    "color.border.control": "--color-control-border",
}
PREFIXES = [  # (json prefix, css prefix); longest first
    ("font.lineHeight.", "--line-height-"),
    ("font.weight.", "--font-weight-"),
    ("font.size.", "--font-size-"),
    ("color.picker.", "--color-"),
    ("gradient.background.", "--gradient-bg-"),
    ("layout.container.", "--container-"),
    ("layout.breakpoint.", "--breakpoint-"),
]
# JSON paths that describe something other than a CSS custom property.
JSON_ONLY = re.compile(r"^(themes\.contract\.(?!storageKey$)|themes\.(dark|light)\.selector$|themes\.dark\.)")
# Font families: the JSON names the face; the CSS names it as the var() fallback.
FAMILY_PATHS = {
    "font.heading": "--font-heading",
    "font.body": "--font-body",
    "font.code": "--font-code",
    "font.codeUi": "--font-code-ui",
}
FAMILY_ONLY = {"font.brand", "font.codeBrand"}  # set by fonts/fonts.css
CSS_ONLY = {"--theme-selector-attribute"}  # the JSON says it as themes.contract.rootSelector


def kebab(s):
    return re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", s).lower()


def css_name(path):
    if path in ALIASES:
        return ALIASES[path]
    for jp, cp in PREFIXES:
        if path.startswith(jp):
            return cp + kebab(path[len(jp):]).replace(".", "-")
    return "--" + kebab(path).replace(".", "-")


def flatten(obj, prefix=""):
    out = {}
    for k, v in obj.items():
        p = prefix + k
        if isinstance(v, dict):
            out.update(flatten(v, p + "."))
        else:
            out[p] = v
    return out


def norm(v):
    v = " ".join(str(v).split()).lower()
    v = re.sub(r"\s*,\s*", ", ", v)
    v = re.sub(r"\(\s+", "(", v)
    return re.sub(r"\s+\)", ")", v)


def expand(v, theme, depth=0):
    """Textually substitute var(--x) with its value, recursively."""
    if depth > 16:
        return v

    def sub(m):
        name = m.group(1)
        return theme[name] if name in theme else m.group(0)

    out = re.sub(r"var\((--[A-Za-z0-9-]+)\)", sub, v)
    return out if out == v else expand(out, theme, depth + 1)


def same(json_v, css_v, theme):
    a, b = norm(json_v), norm(css_v)
    if a == b:
        return True
    if norm(expand(str(json_v), theme)) == norm(expand(css_v, theme)):
        return True
    try:  # last resort for colors written two ways (#fff vs rgb(255,255,255))
        return resolve(str(json_v), theme) == resolve(css_v, theme)
    except (ColorError, ValueError, IndexError):
        return False


def check_consistency(errors):
    dark, light, light_over = themes()
    data = json.loads(TOKENS_JSON.read_text())
    flat = flatten(data)
    root_json, light_json = {}, {}
    for path, value in flat.items():
        if JSON_ONLY.match(path) or path in FAMILY_ONLY:
            continue
        if path.startswith("themes.light."):
            light_json[path[len("themes.light."):]] = value
        else:
            root_json[path] = value

    # Families.
    for path, name in FAMILY_PATHS.items():
        face = root_json.pop(path, None)
        stack = dark.get(name, "")
        if face is None or not re.search(r'var\(--[a-z-]+,\s*"%s"\)' % re.escape(str(face)), stack):
            errors.append("%s (%r) is not the fallback face of %s: %s" % (path, face, name, stack))

    seen = set(CSS_ONLY) | set(FAMILY_PATHS.values())
    for path, value in root_json.items():
        name = css_name(path)
        seen.add(name)
        if name not in dark:
            errors.append("JSON %s -> %s: not declared in design-tokens.css :root" % (path, name))
        elif not same(value, dark[name], dark):
            errors.append("JSON %s = %r but CSS %s = %r" % (path, value, name, dark[name]))
    for name in dark:
        if name not in seen:
            errors.append("CSS %s (:root) has no entry in design-tokens.json" % name)

    seen_light = set()
    for path, value in light_json.items():
        name = css_name(path)
        seen_light.add(name)
        if name not in light_over:
            errors.append("JSON themes.light.%s -> %s: not overridden in the CSS light block" % (path, name))
        elif not same(value, light_over[name], light):
            errors.append("JSON themes.light.%s = %r but CSS light %s = %r" % (path, value, name, light_over[name]))
    for name, value in light_over.items():
        if name in seen_light:
            continue
        if name in dark and same(value, dark[name], light):
            continue  # restates the dark value; nothing for the JSON to say
        errors.append("CSS light %s has no entry in design-tokens.json themes.light" % name)


# --- contrast ---------------------------------------------------------------

SURFACES = ("--color-bg", "--color-surface-1", "--color-surface-2")
TEXT = 4.5
NON_TEXT = 3.0

# (label, foreground, background, floor). A background may be a list of
# layers, painted bottom-up over each surface named in `on`.
CONTRAST = []


def pair(fg, layers, floor, on=SURFACES, label=None, only=None):
    CONTRAST.append((label or fg, fg, layers, floor, on, only))


for t in ("--color-text-primary", "--color-text-secondary", "--color-text-muted",
          "--color-text-subtle", "--color-link", "--color-success", "--color-warning",
          "--color-danger", "--color-info", "--color-state-ok", "--color-state-warn",
          "--color-state-deny"):
    pair(t, [], TEXT)
for s in ("pending", "scheduled", "assigned", "leased", "running", "analyzing",
          "success", "warning", "error", "cancelled"):
    pair("--color-status-%s-fg" % s, ["--color-status-%s-bg" % s], TEXT, label="status-%s badge" % s)
for s in ("keyword", "string", "number", "comment", "function", "builtin", "operator", "punctuation"):
    pair("--color-syntax-%s" % s, ["--color-surface-inset"], TEXT, label="syntax-%s in a well" % s)
for t in ("--color-text-primary", "--color-text-secondary"):
    pair(t, ["--color-surface-inset"], TEXT, label="%s in a well" % t)
# Labels on fills (the fill is opaque, so the surface does not matter).
pair("--color-on-primary-fill", ["--color-primary-fill"], TEXT, on=("--color-bg",))
pair("--color-on-primary", ["--color-primary-fill"], TEXT, on=("--color-bg",))
pair("--color-on-primary-fill", ["--color-primary-fill-hover"], TEXT, on=("--color-bg",))
pair("--color-on-accent-strong", ["--color-accent-strong"], TEXT, on=("--color-bg",))
pair("--color-on-success", ["--color-success"], TEXT, on=("--color-bg",))
# Non-text: the switch (WCAG 1.4.11) and the active-row ring on the popover.
pair("--color-switch-track-off", [], NON_TEXT, on=("--color-surface-1", "--color-surface-2"))
pair("--color-switch-knob", ["--color-switch-track-off"], NON_TEXT, on=("--color-bg",))
pair("--color-switch-knob", ["--color-switch-track-on"], NON_TEXT, on=("--color-bg",))
pair("--color-row-active-border", [], NON_TEXT, on=("--color-surface-2",))
# Accent marks focus rings, input focus borders and hover borders.
pair("--color-accent", [], NON_TEXT, label="--color-accent as a state border")

# Every state-bearing, non-text indicator against what it is painted on
# (WCAG 1.4.11, 3:1), overlays composited. A layer named --gradient-* is
# measured at each of its stops.
POPOVER = ("--color-surface-1", "--color-surface-2")
CALENDAR = ["--gradient-surface-elevated"]
pair("--color-link", [], NON_TEXT, label="spinner arc (.spinner) on the surface")
pair("--color-on-primary-fill", ["--color-primary-fill"], NON_TEXT, on=("--color-bg",),
     label="spinner arc on a primary button (.btn-primary .spinner)")
pair("--color-on-primary-fill", ["--gradient-action-fill"], NON_TEXT, on=("--color-bg",),
     label="spinner arc on the primary gradient")

# Indicators made of two painted parts are measured part against part: the
# moving or filled part against its own track, the track composited over each
# surface (or fill) it can sit on, as painted. Each row is (label, part,
# track layers, surfaces); check_refs.py pins both paints (MEASURED_PAINT).
# Flag leaves <input type="range"> native, so it has no row here.
TWO_PART = [
    ("spinner arc on its track", "--color-link", ["--color-overlay-soft"], SURFACES),
    ("primary-button spinner arc on its track", "--color-on-primary-fill", ["--color-primary-fill-hover"],
     ("--color-bg",)),
    ("upload progress fill on its track", "--color-link", ["--color-overlay-strong"], SURFACES),
    ("switch knob on its track (off)", "--color-switch-knob", ["--color-switch-track-off"], POPOVER),
    ("switch knob on its track (on)", "--color-switch-knob", ["--color-switch-track-on"], POPOVER),
]
for label, part, track, on in TWO_PART:
    pair(part, track, NON_TEXT, on=on, label=label)
pair("--color-control-border", [], NON_TEXT, label="checkbox/radio edge on the surface")
pair("--color-control-border", ["--color-overlay-soft"], NON_TEXT, label="checkbox edge on its box")
pair("--color-accent", ["--color-status-running-bg"], NON_TEXT, label="checked checkbox edge on its box")
pair("--color-text-secondary", ["--color-status-running-bg"], NON_TEXT, label="checkbox checkmark")
pair("--color-secondary", [], NON_TEXT, on=("--color-surface-1",), label="radio dot on the radio (surface-1)")
pair("--color-switch-track-on", [], NON_TEXT, on=POPOVER, label="switch track (on)")
pair("--color-switch-track-on", ["--color-selected-bg"], NON_TEXT, on=("--color-surface-2",),
     label="switch track (on) on the popover's active row")
pair("--color-switch-track-off", ["--color-selected-bg"], NON_TEXT, on=("--color-surface-2",),
     label="switch track (off) on the popover's active row")
pair("--color-primary-fill", [], NON_TEXT, label="selected segmented option / filled selection")
pair("--color-accent-strong", CALENDAR, NON_TEXT, on=("--color-bg",), label="date-range fill on the calendar")
pair("--color-on-accent-strong", ["--color-accent-strong"], TEXT, on=("--color-bg",), label="date-range day label")
pair("--color-primary-fill", CALENDAR, NON_TEXT, on=("--color-bg",), label="selected day on the calendar")
pair("--color-accent", CALENDAR, NON_TEXT, on=("--color-bg",), label="today ring on the calendar")
# Keyboard focus on a day: an inset ring on the fill that day has.
pair("focus-ring-day", CALENDAR, NON_TEXT, on=("--color-bg",), label="day focus ring on the calendar")
pair("focus-ring-day", CALENDAR + ["--color-status-running-bg"], NON_TEXT, on=("--color-bg",),
     label="day focus ring on a hovered/focused day")
pair("focus-ring-day-on-range", ["--color-accent-strong"], NON_TEXT, on=("--color-bg",),
     label="day focus ring on an in-range day")
pair("focus-ring-day-on-fill", ["--gradient-action-fill"], NON_TEXT, on=("--color-bg",),
     label="day focus ring on a selected day (gradient)")
pair("focus-ring-day-on-fill", ["--color-primary-fill"], NON_TEXT, on=("--color-bg",),
     label="day focus ring on a selected day (solid, light)")
# The focus ring's outer color against whatever it surrounds (WCAG 1.4.11).
pair("focus-ring", [], NON_TEXT, label="--focus-ring outer color")
pair("focus-ring-picker", [], NON_TEXT, label="--focus-ring-picker outer color")
# Links: --color-link everywhere; light also allows --color-secondary, with
# --color-primary-hover as its hover color (TOKENS.md "Links").
pair("--color-secondary", [], TEXT, label="--color-secondary as link text", only="light")
pair("--color-primary-hover", [], TEXT, label="--color-primary-hover as link hover", only="light")

# The README's shadcn mapping: every Flag token it names must exist, and the
# pairs shadcn paints with it are measured (a "-foreground" on its base, over
# each surface where the base is translucent; --destructive as text and
# --input / --ring as indicators on every surface).
def shadcn_mapping():
    from flagtokens import ROOT as REPO
    readme = (REPO / "README.md").read_text()
    sec = re.search(r"^## shadcn registry\n(.*?)(?=^## )", readme, re.S | re.M)
    if not sec:
        return None, ["README.md has no '## shadcn registry' section"]
    rows = dict(re.findall(r"^\|\s*`(--[a-z-]+)`\s*\|\s*`(--[a-z0-9-]+)`", sec.group(1), re.M))
    return rows, []


SHADCN, SHADCN_ERRORS = shadcn_mapping()
if SHADCN:
    base_of = {"--foreground": "--background", "--primary-foreground": "--primary",
               "--secondary-foreground": "--secondary", "--muted-foreground": "--muted",
               "--accent-foreground": "--accent"}
    for fgv, bgv in base_of.items():
        if fgv in SHADCN and bgv in SHADCN:
            pair(SHADCN[fgv], [SHADCN[bgv]], TEXT, label="shadcn %s on %s" % (fgv, bgv))
    for v in ("--card", "--popover"):
        if v in SHADCN and "--foreground" in SHADCN:
            pair(SHADCN["--foreground"], [SHADCN[v]], TEXT, label="shadcn %s-foreground on %s" % (v, v))
    if "--destructive" in SHADCN:
        pair(SHADCN["--destructive"], [], TEXT, label="shadcn --destructive as text")
    for v in ("--input", "--ring"):
        if v in SHADCN:
            pair(SHADCN[v], [], NON_TEXT, label="shadcn %s" % v)

# Foregrounds defined outside the token sheet, in the opt-in shadcn layers
# (not core tokens, so products that do not use those layers vendor nothing
# new). Each is read from its own file, where it must be set for both themes,
# and measured like a token.
SCOPED = [
    ("components/shadcn-parity.css", "--flag-on-accent"),
    ("shadcn/theme.css", "--accent-solid-foreground"),
]
pair("--flag-on-accent", ["--color-accent"], TEXT, on=("--color-bg",),
     label="--flag-on-accent on --color-accent (.badge-accent, shadcn-parity.css)")
pair("--accent-solid-foreground", ["--color-accent"], TEXT, on=("--color-bg",),
     label="--accent-solid-foreground on --color-accent (shadcn/theme.css)")


def check_shadcn_theme(errors):
    """shadcn/theme.css sets every variable the README table maps, to that token."""
    from flagtokens import DS, block
    if not SHADCN:
        return
    theme = block((DS / "shadcn" / "theme.css").read_text(), ":root")
    for var, token in sorted(SHADCN.items()):
        got = theme.get(var)
        if got != "var(%s)" % token:
            errors.append("design-system/shadcn/theme.css: %s is %s, but README.md's shadcn table maps it to %s"
                          % (var, got or "unset", token))


def scoped_values(errors):
    from flagtokens import DS, LIGHT_SELECTOR, block
    dark, light = {}, {}
    for rel_path, prop in SCOPED:
        css = (DS / rel_path).read_text()
        for name, sel, out in (("dark", ":root", dark), ("light", LIGHT_SELECTOR, light)):
            try:
                decls = block(css, sel)
            except ValueError:
                decls = {}
            if prop in decls:
                out[prop] = decls[prop]
            else:
                errors.append("design-system/%s: no %s in its %s block (%s theme)" % (rel_path, prop, sel, name))
    return dark, light


# Gradients under a label: every point of the blend is measured.
GRADIENT_LABELS = [
    ("--color-on-primary-fill", "--gradient-action-fill", TEXT),
    ("focus-ring-day-on-fill", "--gradient-action-fill", NON_TEXT),
    ("--color-on-primary-fill", "--gradient-action-fill-hover", TEXT),
]



def gradient_stops(value, theme):
    m = re.match(r"^linear-gradient\((.*)\)$", " ".join(expand(value, theme).split()), re.S)
    if not m:
        raise ColorError("not a linear-gradient: %r" % value)
    from flagtokens import _split_top
    parts = _split_top(m.group(1))
    if parts and re.match(r"^[\d.]+deg$|^to ", parts[0]):
        parts = parts[1:]
    return [re.sub(r"\s+[\d.]+%$", "", p) for p in parts]


def fg_color(fg, theme):
    if fg.startswith("focus-ring"):
        # "0 0 0 2px <inner>, 0 0 0 4px <outer>": the outer ring is what
        # meets the surrounding surface. An inset ring ("inset 0 0 0 2px
        # <color>") has one layer, painted on the element's own fill.
        from flagtokens import _split_top
        layers = _split_top(expand(theme["--" + fg], theme))
        return resolve(re.sub(r"^(inset\s+)?(-?[\d.]+(px)?\s+){3,4}", "", layers[-1].strip()), theme)
    return resolve("var(%s)" % fg, theme)


def check_contrast(errors, report):
    dark, light, _ = themes()
    sdark, slight = scoped_values(errors)
    dark, light = {**dark, **sdark}, {**light, **slight}
    for tname, theme in (("dark", dark), ("light", light)):
        for label, fg, layers, floor, on, only in CONTRAST:
            if only and only != tname:
                continue
            for surface in on:
                try:
                    backs = [resolve("var(%s)" % surface, theme)]
                    for layer in layers:
                        if layer.startswith("--gradient"):
                            stops = [resolve(s, theme) for s in gradient_stops(theme[layer], theme)]
                            backs = [over(s, b) for b in backs for s in stops]
                        else:
                            backs = [over(resolve("var(%s)" % layer, theme), b) for b in backs]
                    color = fg_color(fg, theme)
                    ratio = min(contrast(color, b) for b in backs)
                except ColorError as e:
                    errors.append("%s %s on %s: %s" % (tname, label, surface, e))
                    continue
                where = "%s: %s on %s" % (tname, label, " + ".join([surface] + layers))
                if ratio < floor:
                    errors.append("%s is %.2f:1, needs %.1f:1" % (where, ratio, floor))
        for fg, grad, floor in GRADIENT_LABELS:
            try:
                stops = [resolve(s, theme) for s in gradient_stops(theme[grad], theme)]
                label = fg_color(fg, theme)
            except (ColorError, KeyError) as e:
                errors.append("%s %s: %s" % (tname, grad, e))
                continue
            worst = None
            for a, b in zip(stops, stops[1:]):
                for i in range(101):
                    w = i / 100
                    c = tuple(a[k] * (1 - w) + b[k] * w for k in range(4))
                    r = contrast(label, over(c, (0.0, 0.0, 0.0, 1.0)))
                    worst = r if worst is None else min(worst, r)
            if worst < floor:
                errors.append("%s: %s on %s dips to %.2f:1, needs %.1f:1" % (tname, fg, grad, worst, floor))


# --- static values -----------------------------------------------------------

MODERN_COLOR = re.compile(r"\b(color-mix|oklch|oklab|lch|lab|color|light-dark|relative)\(", re.I)


def check_static(errors):
    """Newer color functions must never be the only value.

    A browser that does not understand color-mix() (older Safari, some
    webviews) treats a custom property that uses it as invalid at
    computed-value time, so every rule reading that token falls back to its
    initial value: a transparent button under a white label. Tokens must
    therefore be static values (precompute the mix). In components.css a
    modern function is allowed only right after a declaration of the same
    property with a static value, which old browsers keep.
    """
    from flagtokens import DS
    css = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), TOKENS_CSS.read_text(), flags=re.S)
    for lineno, code in enumerate(css.splitlines(), 1):
        if MODERN_COLOR.search(code):
            errors.append("tokens/design-tokens.css:%d uses %s; precompute it to a static hex/rgba value"
                          % (lineno, MODERN_COLOR.search(code).group(1)))
    for path, value in flatten(json.loads(TOKENS_JSON.read_text())).items():
        if isinstance(value, str) and MODERN_COLOR.search(value):
            errors.append("design-tokens.json %s uses %s; precompute it" % (path, MODERN_COLOR.search(value).group(1)))
    comp = DS / "components" / "components.css"
    if not comp.exists():
        return
    text = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), comp.read_text(), flags=re.S)
    for m in re.finditer(r"\{([^{}]*)\}", text):
        decls = [d.strip() for d in m.group(1).split(";") if d.strip()]
        for i, d in enumerate(decls):
            if not MODERN_COLOR.search(d):
                continue
            prop = d.split(":", 1)[0].strip()
            prev = decls[i - 1] if i else ""
            if not (prev.split(":", 1)[0].strip() == prop and not MODERN_COLOR.search(prev)):
                line = text.count("\n", 0, m.start()) + 1
                errors.append("components/components.css (rule at line %d): `%s` needs a static `%s:` "
                              "fallback declared right before it" % (line, d[:70], prop))


def main():
    errors, report = [], []
    check_static(errors)
    for name, fn in (("consistency", check_consistency),):
        try:
            fn(errors)
        except (ValueError, json.JSONDecodeError) as e:
            errors.append("%s: %s" % (name, e))
    errors.extend(SHADCN_ERRORS)
    check_shadcn_theme(errors)
    dark, light, _ = themes()
    for var, token in sorted((SHADCN or {}).items()):
        for tname, theme in (("dark", dark), ("light", light)):
            if token not in theme:
                errors.append("README.md shadcn registry: %s maps to %s, which %s does not define (%s)"
                              % (var, token, TOKENS_CSS.name, tname))
    try:
        check_contrast(errors, report)
    except ValueError as e:
        errors.append("contrast: %s" % e)
    for line in report:
        print("check-tokens: " + line)
    if errors:
        for e in errors:
            print("ERROR: " + e, file=sys.stderr)
        print("check-tokens: %d problem(s) in %s / %s" % (len(errors), TOKENS_JSON.name, TOKENS_CSS.name), file=sys.stderr)
        return 1
    print("check-tokens: ok (%d contrast measurements over both themes, JSON and CSS agree)"
          % sum(len(p[4]) * (1 if p[5] else 2) for p in CONTRAST))
    return 0


if __name__ == "__main__":
    sys.exit(main())
