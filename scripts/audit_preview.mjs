#!/usr/bin/env node
// audit_preview.mjs — render the preview in Chromium and audit what is
// actually painted: axe-core (WCAG 2 A/AA, including computed text contrast)
// in light and dark at 1440 and 390 wide, with the interactive states that
// only exist after interaction: the date picker open in range mode, the
// date-time picker open with its time controls, and keyboard focus moved
// through every focusable element.
//
// Needs Node, Playwright with Chromium, and axe-core; nothing else in Flag
// does, so CI runs the static checks (make check) and this runs locally:
//
//   npm install --no-save --prefix /tmp/flag-audit playwright axe-core
//   NODE_PATH=/tmp/flag-audit/node_modules node scripts/audit_preview.mjs
//
// (or `make audit`, which does the same). Exits 1 on any violation.

import { createServer } from "node:http";
import { createRequire } from "node:module";
import { readFile } from "node:fs/promises";
import { existsSync, readFileSync } from "node:fs";
import { extname, join, normalize, resolve, dirname } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..", "design-system");

function load(name) {
  const bases = [import.meta.url, ...(process.env.NODE_PATH || "").split(":").filter(Boolean).map((p) => join(p, "noop.js"))];
  for (const base of bases) {
    try {
      return createRequire(base).resolve(name);
    } catch {}
  }
  throw new Error(`cannot find ${name}; install it and set NODE_PATH (see the header of this file)`);
}

const pw = await import(pathToFileURL(load("playwright")).href);
const chromium = pw.chromium || pw.default.chromium;
const AXE = readFileSync(load("axe-core/axe.min.js"), "utf8");

const TYPES = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".svg": "image/svg+xml",
  ".png": "image/png", ".woff2": "font/woff2", ".woff": "font/woff", ".json": "application/json" };
const server = createServer(async (req, res) => {
  const path = normalize(decodeURIComponent(new URL(req.url, "http://x").pathname)).replace(/^(\.\.[/\\])+/, "");
  const file = join(ROOT, path);
  if (!file.startsWith(ROOT) || !existsSync(file)) { res.writeHead(404); res.end(); return; }
  res.writeHead(200, { "content-type": TYPES[extname(file)] || "application/octet-stream" });
  res.end(await readFile(file));
}).listen(0, "127.0.0.1");
await new Promise((r) => server.on("listening", r));
const base = `http://127.0.0.1:${server.address().port}`;

const PAGES = ["/preview/index.html", "/preview/email-preview.html", "/email-safe.html"];
const browser = await chromium.launch();
let failures = 0;

// Computed text contrast, including what axe reports as "incomplete": text
// over gradients is measured against every color stop of every gradient
// beneath it (the worst stop counts), translucent layers are composited, and
// ancestor opacity fades the text. Disabled controls are exempt (WCAG 1.4.3).
const CONTRAST_JS = `(() => {
  const parse = (s) => {
    const out = [];
    for (const m of s.matchAll(/rgba?\\(([^)]+)\\)|color\\(srgb ([^)]+)\\)|transparent/g)) {
      if (m[0] === "transparent") { out.push([0, 0, 0, 0]); continue; }
      if (m[1]) { const v = m[1].split(/[ ,/]+/).filter(Boolean).map(Number); out.push([v[0], v[1], v[2], v.length > 3 ? v[3] : 1]); }
      else { const v = m[2].split(/[ /]+/).filter(Boolean).map(Number); out.push([v[0] * 255, v[1] * 255, v[2] * 255, v.length > 3 ? v[3] : 1]); }
    }
    return out;
  };
  const over = (t, b) => [0, 1, 2].map((i) => t[i] * t[3] + b[i] * (1 - t[3])).concat(1);
  const lum = (c) => { const f = (x) => { x /= 255; return x <= 0.04045 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4; };
    return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]); };
  const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };
  const visible = (el) => { const r = el.getBoundingClientRect(); if (r.width < 2 || r.height < 2) return false;
    const cs = getComputedStyle(el); if (cs.visibility === "hidden" || cs.clipPath.includes("inset(50%") || cs.clip === "rect(0px, 0px, 0px, 0px)") return false;
    for (let n = el; n; n = n.parentElement) { const c = getComputedStyle(n); if (c.display === "none" || parseFloat(c.opacity) === 0) return false; }
    return true; };
  const disabled = (el) => {
    if (el.closest(":disabled, [aria-disabled='true'], .is-disabled, .flatpickr-disabled, .notAllowed")) return true;
    const label = el.closest("label");
    return !!(label && label.control && label.control.disabled);
  };
  const fails = [];
  const els = [...document.querySelectorAll("body *")].filter((el) =>
    ([...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim()) || (el.matches("input:not([type=checkbox]):not([type=radio]):not([type=file]), textarea") && el.value)) && !el.closest("svg, style, script, iframe"));
  for (const el of els) {
    if (!visible(el) || disabled(el)) continue;
    const cs = getComputedStyle(el);
    let fg = parse(cs.color)[0]; if (!fg) continue;
    let opacity = 1; const layers = [];
    for (let n = el; n; n = n.parentElement) {
      const c = getComputedStyle(n); opacity *= parseFloat(c.opacity);
      // background-image layers, top first; each gradient layer's stops are candidates.
      let img = null;
      if (c.backgroundImage.includes("gradient")) {
        const parts = []; let depth = 0, cur = "";
        for (const ch of c.backgroundImage) { if (ch === "(") depth++; if (ch === ")") depth--; if (ch === "," && depth === 0) { parts.push(cur); cur = ""; } else cur += ch; }
        parts.push(cur);
        img = parts.map((s) => parse(s)).filter((l) => l.length);
      }
      const col = parse(c.backgroundColor)[0];
      layers.push({ col, img });
      const opaqueImg = img && img.length && img[img.length - 1].every((s) => s[3] === 1);
      if ((col && col[3] === 1) || opaqueImg) break;
    }
    let backs = [[255, 255, 255, 1]];
    for (const L of layers.reverse()) {
      if (L.col && L.col[3] > 0) backs = backs.map((b) => over(L.col, b));
      if (L.img) for (const stops of [...L.img].reverse()) {
        const nb = []; for (const b of backs) for (const s of stops) nb.push(over(s, b));
        backs = [...new Map(nb.map((c) => [c.map(Math.round).join(), c])).values()].slice(0, 96);
      }
    }
    fg = [fg[0], fg[1], fg[2], fg[3] * opacity];
    const size = parseFloat(cs.fontSize); const bold = parseInt(cs.fontWeight, 10) >= 700;
    const floor = size >= 24 || (bold && size >= 18.66) ? 3 : 4.5;
    let worst = 99, at = null; for (const b of backs) { const r = ratio(over(fg, b), b); if (r < worst) { worst = r; at = b; } }
    if (worst < floor - 0.005) fails.push(\`\${worst.toFixed(2)}:1 < \${floor} (over rgb(\${at.slice(0, 3).map(Math.round).join(",")})) on \${el.tagName.toLowerCase()}.\${String(el.className).trim().replace(/\\s+/g, ".")} "\${(el.value || el.textContent).trim().slice(0, 30)}"\`);
  }
  return fails;
})()`;

async function contrast(page, label) {
  const fails = [...new Set(await page.evaluate(CONTRAST_JS))];
  failures += fails.length;
  for (const f of fails.slice(0, 20)) console.log(`FAIL ${label}: contrast ${f}`);
  if (fails.length > 20) console.log(`     ... ${fails.length - 20} more`);
}

async function axe(page, label) {
  await contrast(page, label);
  await page.addScriptTag({ content: AXE });
  const violations = await page.evaluate(async () =>
    (await window.axe.run(document, { runOnly: ["wcag2a", "wcag2aa"] })).violations.map((v) => ({
      id: v.id, nodes: v.nodes.map((n) => `${n.target.join(" ")} :: ${(n.any[0] || {}).message || n.failureSummary}`),
    })));
  for (const v of violations) {
    failures += v.nodes.length;
    console.log(`FAIL ${label}: ${v.id} (${v.nodes.length})`);
    for (const n of v.nodes.slice(0, 12)) console.log(`     ${n.slice(0, 220)}`);
  }
  return violations.length;
}

for (const theme of ["light", "dark"]) {
  for (const width of [1440, 390]) {
    const ctx = await browser.newContext({ viewport: { width, height: 900 }, colorScheme: theme, reducedMotion: "reduce" });
    await ctx.addInitScript((t) => { try { localStorage.setItem("flag-theme-preference", t); } catch {} }, theme);
    const page = await ctx.newPage();
    page.on("pageerror", (e) => { failures++; console.log(`FAIL ${theme} ${width}: page error ${e.message}`); });
    for (const path of PAGES) {
      await page.goto(base + path, { waitUntil: "networkidle" });
      await page.evaluate(() => document.fonts.ready);
      await axe(page, `${theme} ${width} ${path}`);
      if (path !== "/preview/index.html") continue;

      // Every focusable element must show a visible focus indicator.
      const unfocused = await page.evaluate(async () => {
        const out = [];
        const sel = "a[href]:not([tabindex='-1']), button:not([disabled]), input:not([disabled]):not([tabindex='-1']), select, textarea, summary, [tabindex='0']";
        for (const el of document.querySelectorAll(sel)) {
          if (!el.getClientRects().length || getComputedStyle(el).visibility === "hidden") continue;
          el.focus({ focusVisible: true });
          if (document.activeElement !== el) continue;
          const shown = (node) => {
            for (const n of [node, node.parentElement, node.nextElementSibling && node.nextElementSibling.querySelector && node.nextElementSibling]) {
              if (!n) continue;
              const cs = getComputedStyle(n);
              if ((cs.outlineStyle !== "none" && parseFloat(cs.outlineWidth) > 0) || (cs.boxShadow && cs.boxShadow !== "none")) return true;
              const box = n.querySelector && n.querySelector(".ds-checkbox__box");
              if (box && getComputedStyle(box).boxShadow !== "none") return true;
            }
            return false;
          };
          if (!shown(el)) out.push(el.outerHTML.slice(0, 120));
        }
        document.activeElement && document.activeElement.blur();
        return out;
      });
      for (const u of unfocused) { failures++; console.log(`FAIL ${theme} ${width}: no visible focus on ${u}`); }

      // Date picker in range mode with an in-range span.
      const opened = await page.evaluate(() => {
        const date = document.querySelector("#f-date");
        if (!date || !date._flatpickr) return false;
        const fp = date._flatpickr;
        fp.set("mode", "range");
        const d = new Date(); d.setDate(5);
        const e = new Date(d); e.setDate(12);
        fp.setDate([d, e], false);
        fp.open();
        return true;
      });
      if (opened) {
        await page.waitForFunction(() => { const c = document.querySelector(".flatpickr-calendar.open"); return c && getComputedStyle(c).opacity === "1" && !c.getAnimations().some((a) => a.playState === "running"); }, null, { timeout: 5000 });
        await axe(page, `${theme} ${width} date picker (range)`);
        await page.evaluate(() => document.querySelector("#f-date")._flatpickr.close());
      }
      const timed = await page.evaluate(() => {
        const dt = document.querySelector("#f-datetime");
        if (!dt || !dt._flatpickr) return false;
        dt._flatpickr.open();
        return true;
      });
      if (timed) {
        await page.waitForFunction(() => { const c = document.querySelector(".flatpickr-calendar.open"); return c && getComputedStyle(c).opacity === "1" && !c.getAnimations().some((a) => a.playState === "running"); }, null, { timeout: 5000 });
        await axe(page, `${theme} ${width} date-time picker`);
        await page.evaluate(() => document.querySelector("#f-datetime")._flatpickr.close());
      }
    }
    await ctx.close();
  }
}
await browser.close();
server.close();
if (failures) {
  console.log(`audit-preview: ${failures} problem(s)`);
  process.exit(1);
}
console.log("audit-preview: ok (axe WCAG 2 A/AA + visible focus, light and dark, 1440 and 390, pickers open)");
