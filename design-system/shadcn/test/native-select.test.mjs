import assert from "node:assert/strict"
import fs from "node:fs"
import { createRequire } from "node:module"
import path from "node:path"
import test from "node:test"
import { fileURLToPath } from "node:url"
import vm from "node:vm"
import { ts } from "@ts-morph/common"

const HERE = path.dirname(fileURLToPath(import.meta.url))
const SHADCN_ROOT = path.resolve(HERE, "..")
const requireFromShadcn = createRequire(path.join(SHADCN_ROOT, "package.json"))

// Minimal React/JSX runtime stub so registry TSX modules can be transpiled and
// executed directly under `node --test` without pulling React into dev tooling.
const reactStub = {
  createElement(type, props, ...children) {
    return { type, props: { ...props, children } }
  },
}
const jsxStub = {
  jsx(type, props) {
    return { type, props }
  },
  jsxs(type, props) {
    return { type, props }
  },
}
const lucideStub = {
  ChevronDownIcon: "ChevronDownIcon",
}

function loadTsModule(relPath, extraModules = {}) {
  const fullPath = path.join(SHADCN_ROOT, relPath)
  const source = fs.readFileSync(fullPath, "utf8")
  const { outputText } = ts.transpileModule(source, {
    fileName: fullPath,
    compilerOptions: {
      module: ts.ModuleKind.CommonJS,
      target: ts.ScriptTarget.ES2022,
      jsx: ts.JsxEmit.ReactJSX,
    },
  })
  const mod = { exports: {} }
  const customRequire = (id) => {
    if (id in extraModules) return extraModules[id]
    if (id === "react") return reactStub
    if (id === "react/jsx-runtime") return jsxStub
    if (id === "lucide-react") return lucideStub
    return requireFromShadcn(id)
  }
  vm.runInNewContext(
    `(function (exports, require, module) { ${outputText}\n})`,
    {}
  )(mod.exports, customRequire, mod)
  return mod.exports
}

const utils = loadTsModule("registry/flag/lib/utils.ts")
const { NativeSelect } = loadTsModule(
  "registry/flag/ui/native-select.tsx",
  { "@/lib/utils": utils }
)

function selectTokens(props = {}) {
  const tree = NativeSelect(props)
  const [selectEl, iconEl] = tree.props.children
  return {
    wrapperClass: tree.props.className.split(/\s+/),
    selectProps: selectEl.props,
    tokens: selectEl.props.className.split(/\s+/),
    iconTokens: iconEl.props.className.split(/\s+/),
  }
}

test("NativeSelect reserves right chevron gutter by default and in sm size", () => {
  const def = selectTokens()
  assert.equal(def.selectProps["data-size"], "default")
  assert.ok(def.tokens.includes("pl-3"))
  assert.ok(def.tokens.includes("pr-8"))
  assert.ok(def.tokens.includes("data-[size=sm]:pl-2.5"))
  assert.ok(def.tokens.includes("data-[size=sm]:pr-7"))
  assert.ok(def.iconTokens.includes("right-2.5"))

  const sm = selectTokens({ size: "sm" })
  assert.equal(sm.selectProps["data-size"], "sm")
  assert.ok(sm.tokens.includes("pr-8"))
  assert.ok(sm.tokens.includes("data-[size=sm]:pr-7"))
})

test("NativeSelect preserves chevron right-padding when caller passes px-* or p-*", () => {
  const withPx = selectTokens({ className: "px-2.5" })
  assert.ok(withPx.tokens.includes("px-2.5"))
  assert.ok(!withPx.tokens.includes("pl-3"), "px-2.5 should replace default pl-3")
  assert.ok(
    withPx.tokens.includes("pr-8"),
    "px-2.5 must not strip right chevron clearance pr-8"
  )
  assert.ok(
    withPx.tokens.includes("data-[size=sm]:pr-7"),
    "px-2.5 must not strip sm right chevron clearance"
  )
  assert.ok(
    withPx.tokens.indexOf("pr-8") > withPx.tokens.indexOf("px-2.5"),
    "pr-8 must follow px-2.5"
  )

  const withP = selectTokens({ className: "p-2" })
  assert.ok(withP.tokens.includes("p-2"))
  assert.ok(!withP.tokens.includes("py-1"), "p-2 should replace default py-1")
  assert.ok(!withP.tokens.includes("pl-3"), "p-2 should replace default pl-3")
  assert.ok(withP.tokens.includes("pr-8"))
  assert.ok(withP.tokens.includes("data-[size=sm]:pr-7"))
})

test("NativeSelect yields only to physical pr-* overrides and preserves pr-8 alongside logical pe-*", () => {
  const withPr = selectTokens({ className: "pr-10" })
  assert.ok(withPr.tokens.includes("pr-10"))
  assert.ok(!withPr.tokens.includes("pr-8"))
  assert.ok(!withPr.tokens.includes("data-[size=sm]:pr-7"))

  const smWithPr = selectTokens({ size: "sm", className: "px-2 pr-10" })
  assert.ok(smWithPr.tokens.includes("px-2"))
  assert.ok(smWithPr.tokens.includes("pr-10"))
  assert.ok(!smWithPr.tokens.includes("pr-8"))
  assert.ok(
    !smWithPr.tokens.includes("data-[size=sm]:pr-7"),
    "explicit pr-10 on size=sm must not be out-specified by data-[size=sm]:pr-7"
  )

  const withPe = selectTokens({ className: "pe-9" })
  assert.ok(withPe.tokens.includes("pe-9"))
  assert.ok(
    withPe.tokens.includes("pr-8"),
    "logical pe-* pads left in RTL while chevron stays at physical right-2.5"
  )

  const withImportantPostfix = selectTokens({ className: "pr-6!" })
  assert.ok(withImportantPostfix.tokens.includes("pr-6!"))
  assert.ok(!withImportantPostfix.tokens.includes("pr-8"))

  const withSmOnlyPr = selectTokens({
    size: "sm",
    className: "data-[size=sm]:pr-9",
  })
  assert.ok(withSmOnlyPr.tokens.includes("pr-8"))
  assert.ok(withSmOnlyPr.tokens.includes("data-[size=sm]:pr-9"))
  assert.ok(!withSmOnlyPr.tokens.includes("data-[size=sm]:pr-7"))
})

test("NativeSelect keeps base pr-8 for responsive overrides and non-padding prefixes", () => {
  const responsive = selectTokens({ className: "sm:pr-10" })
  assert.ok(responsive.tokens.includes("pr-8"))
  assert.ok(responsive.tokens.includes("sm:pr-10"))

  const peerAndPrint = selectTokens({
    className: "peer-disabled:opacity-40 print:hidden",
  })
  assert.ok(peerAndPrint.tokens.includes("pr-8"))
  assert.ok(peerAndPrint.tokens.includes("data-[size=sm]:pr-7"))
})
