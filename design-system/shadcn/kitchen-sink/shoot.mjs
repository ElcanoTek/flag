// Renders the kitchen sink in light/dark at 1440/390, opens each overlay,
// and runs axe. Usage: node shoot.mjs OUT_DIR [URL] [theme-width]
import { chromium } from "playwright"
import AxeBuilder from "@axe-core/playwright"
import fs from "node:fs"
const out = process.argv[2]
const url = process.argv[3] ?? "http://localhost:8813/"
const only = process.argv[4]
fs.mkdirSync(out, { recursive: true })
const browser = await chromium.launch()
const report = {}
const overlays = ["select", "dialog", "alert-dialog", "sheet", "dropdown", "popover", "tooltip", "toast"]
for (const theme of ["dark", "light"]) {
  for (const width of [1440, 390]) {
    if (only && only !== `${theme}-${width}`) continue
    const ctx = await browser.newContext({ viewport: { width, height: 900 }, colorScheme: theme, reducedMotion: "reduce" })
    await ctx.addInitScript((t) => localStorage.setItem("flag-theme-preference", t), theme)
    const page = await ctx.newPage()
    const errors = []
    page.on("pageerror", (e) => errors.push(String(e)))
    page.on("console", (m) => m.type() === "error" && errors.push(m.text()))
    await page.goto(url)
    await page.waitForSelector("[data-section=overlays]")
    await page.evaluate(() => document.fonts.ready)
    await page.waitForTimeout(300)
    const tag = `${theme}-${width}`
    await page.screenshot({ path: `${out}/kitchen-sink-${tag}.png`, fullPage: true })
    const axe = await new AxeBuilder({ page }).analyze()
    report[`page-${tag}`] = axe.violations.map((v) => ({ id: v.id, impact: v.impact, nodes: v.nodes.map((n) => n.target.join(" ") + " :: " + n.failureSummary.split("\n").slice(1, 2).join("")) }))
    for (const o of overlays) {
      const btn = page.locator(`[data-open=${o}]`)
      await btn.scrollIntoViewIfNeeded()
      if (o === "tooltip") await btn.focus()
      else await btn.click()
      await page.waitForTimeout(400)
      await page.screenshot({ path: `${out}/overlay-${o}-${tag}.png` })
      if (width === 1440) {
        const a = await new AxeBuilder({ page }).analyze()
        report[`${o}-${tag}`] = a.violations.map((v) => ({ id: v.id, impact: v.impact, nodes: v.nodes.map((n) => n.target.join(" ") + " :: " + n.failureSummary.split("\n").slice(1, 2).join("")) }))
      }
      await page.keyboard.press("Escape")
      if (o === "toast") await page.evaluate(() => document.querySelectorAll("[data-sonner-toast]").forEach((t) => t.remove()))
      await page.mouse.click(5, 5)
      await page.waitForTimeout(250)
    }
    // keyboard focus states: tab through the button row
    await page.goto(url)
    await page.waitForSelector("[data-section=overlays]")
    await page.locator("[data-section=button] button").first().focus()
    await page.keyboard.press("Tab")
    await page.keyboard.press("Shift+Tab")
    await page.locator("[data-section=button]").screenshot({ path: `${out}/focus-button-${tag}.png` })
    report[`errors-${tag}`] = errors
    await ctx.close()
  }
}
await browser.close()
fs.writeFileSync(`${out}/axe-report.json`, JSON.stringify(report, null, 2))
for (const [k, v] of Object.entries(report)) console.log(k, Array.isArray(v) ? (v.length ? JSON.stringify(v, null, 1).slice(0, 1500) : "ok") : v)
// Page-level violations fail the run. Open-overlay scans are reported only:
// Radix modal menus aria-hide <main> while open (aria-hidden-focus,
// landmark-one-main, page-has-heading-one) and portal popups sit outside
// landmarks (region); see Flag's design-system/SHADCN.md "Accessibility".
const pageViolations = Object.entries(report).filter(([k, v]) => k.startsWith("page-") && v.length)
const pageErrors = Object.entries(report).filter(([k, v]) => k.startsWith("errors-") && v.length)
if (pageViolations.length || pageErrors.length) process.exitCode = 1
