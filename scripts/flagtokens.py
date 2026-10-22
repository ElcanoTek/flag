"""Shared helpers for Flag's checks: read the token sheet, resolve CSS colors.

Standard library only. The evaluator understands exactly what the token sheet
uses — hex, rgb()/rgba(), `transparent`, `var(--x[, fallback])` and
`color-mix(in srgb, ...)` (nested, with CSS Color 5's premultiplied alpha
rule) — and raises on anything else, so a token written in a new syntax fails
a check loudly instead of being skipped. The idea comes from fleet's
cssContrast.ts.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DS = ROOT / "design-system"
TOKENS_CSS = DS / "tokens" / "design-tokens.css"
TOKENS_JSON = DS / "tokens" / "design-tokens.json"

LIGHT_SELECTOR = ':root[data-theme="light"]'


def _strip_comments(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def block(css, selector):
    """Custom properties declared directly in the top-level block `selector {`."""
    css = _strip_comments(css)
    m = re.search(r"(?m)^" + re.escape(selector) + r"\s*(,[^{]*)?\{", css)
    if not m:
        raise ValueError("no top-level %r block" % selector)
    body = css[m.end():css.index("\n}", m.end())]
    out = {}
    for d in re.finditer(r"(--[A-Za-z0-9-]+)\s*:\s*([^;]+);", body):
        out[d.group(1)] = " ".join(d.group(2).split())
    return out


def themes(css=None):
    """(dark, light, light_overrides): dark is :root, light overlays it."""
    if css is None:
        css = TOKENS_CSS.read_text()
    root = block(css, ":root")
    light = block(css, LIGHT_SELECTOR)
    return root, {**root, **light}, light


# --- colors ---------------------------------------------------------------

class ColorError(ValueError):
    pass


def _split_top(s):
    parts, depth, cur = [], 0, ""
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(cur.strip())
            cur = ""
        else:
            cur += ch
    parts.append(cur.strip())
    return parts


def _call(s):
    m = re.match(r"^([a-z-]+)\((.*)\)$", s.strip(), re.S | re.I)
    if not m:
        return None
    depth = 0
    body = s.strip()
    for i in range(len(m.group(1)), len(body)):
        if body[i] == "(":
            depth += 1
        elif body[i] == ")":
            depth -= 1
            if depth == 0 and i != len(body) - 1:
                return None
    return m.group(1).lower(), m.group(2)


def resolve(value, theme, depth=0):
    """Resolve a CSS color expression to (r, g, b, a), channels 0-255, a 0-1."""
    if depth > 32:
        raise ColorError("var() cycle resolving %r" % value)
    v = value.strip()
    low = v.lower()
    if low == "transparent":
        return (0.0, 0.0, 0.0, 0.0)
    if low == "white":
        return (255.0, 255.0, 255.0, 1.0)
    if low == "black":
        return (0.0, 0.0, 0.0, 1.0)
    if v.startswith("#"):
        h = v[1:]
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h)
        if len(h) not in (6, 8) or not re.fullmatch(r"[0-9a-fA-F]+", h):
            raise ColorError("bad hex %r" % v)
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
        a = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
        return (float(r), float(g), float(b), a)
    c = _call(v)
    if not c:
        raise ColorError("cannot evaluate %r" % v)
    name, args = c
    if name == "var":
        parts = _split_top(args)
        ref = parts[0]
        if ref in theme:
            return resolve(theme[ref], theme, depth + 1)
        if len(parts) > 1:
            return resolve(",".join(parts[1:]), theme, depth + 1)
        raise ColorError("undefined %s" % ref)
    if name in ("rgb", "rgba"):
        nums = re.split(r"[\s,/]+", args.strip())
        if len(nums) not in (3, 4):
            raise ColorError("bad %s()" % name)
        ch = [float(n) for n in nums[:3]]
        a = 1.0
        if len(nums) == 4:
            a = float(nums[3][:-1]) / 100 if nums[3].endswith("%") else float(nums[3])
        return (ch[0], ch[1], ch[2], a)
    if name == "color-mix":
        parts = _split_top(args)
        if len(parts) != 3 or parts[0].replace(" ", "") != "insrgb":
            raise ColorError("only color-mix(in srgb, a, b) is supported: %r" % v)

        def side(p):
            m = re.match(r"^(.*?)(?:\s+([\d.]+)%)?$", p.strip(), re.S)
            return resolve(m.group(1), theme, depth + 1), (float(m.group(2)) if m.group(2) else None)

        (c1, p1), (c2, p2) = side(parts[1]), side(parts[2])
        if p1 is None and p2 is None:
            p1 = p2 = 50.0
        elif p1 is None:
            p1 = 100 - p2
        elif p2 is None:
            p2 = 100 - p1
        total = p1 + p2
        if total <= 0:
            raise ColorError("color-mix percentages sum to 0")
        w1, w2 = p1 / total, p2 / total
        a = c1[3] * w1 + c2[3] * w2
        if a == 0:
            rgb = (0.0, 0.0, 0.0)
        else:
            rgb = tuple((c1[i] * c1[3] * w1 + c2[i] * c2[3] * w2) / a for i in range(3))
        if total < 100:
            a *= total / 100
        return (rgb[0], rgb[1], rgb[2], a)
    raise ColorError("unsupported function %s() in %r" % (name, v))


def over(top, bottom):
    """Composite `top` over an opaque `bottom`; returns an opaque color."""
    a = top[3]
    return tuple(top[i] * a + bottom[i] * (1 - a) for i in range(3)) + (1.0,)


def luminance(c):
    def lin(x):
        x /= 255
        return x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(c[0]) + 0.7152 * lin(c[1]) + 0.0722 * lin(c[2])


def contrast(fg, bg):
    """WCAG 2 contrast ratio; `fg` is composited over the opaque `bg`."""
    if bg[3] < 1:
        raise ColorError("backdrop must be opaque")
    fg = over(fg, bg)
    l1, l2 = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)
