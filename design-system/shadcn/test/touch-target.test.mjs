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
  CheckIcon: "CheckIcon",
  MinusIcon: "MinusIcon",
  CircleIcon: "CircleIcon",
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
const radixStub = {
  Checkbox: { Root: "CheckboxRoot", Indicator: "CheckboxIndicator" },
  RadioGroup: { Root: "RadioGroupRoot", Item: "RadioGroupItem", Indicator: "RadioGroupIndicator" },
  Switch: { Root: "SwitchRoot", Thumb: "SwitchThumb" },
}
const mods = { "@/lib/utils": utils, "radix-ui": radixStub }
const { Checkbox } = loadTsModule("registry/flag/ui/checkbox.tsx", mods)
const { RadioGroupItem } = loadTsModule("registry/flag/ui/radio-group.tsx", mods)
const { Switch } = loadTsModule("registry/flag/ui/switch.tsx", mods)

const HIT_AREA = [
  "any-pointer-coarse:after:absolute",
  "any-pointer-coarse:after:top-1/2",
  "any-pointer-coarse:after:left-1/2",
    "any-pointer-coarse:after:-translate-1/2",
]

for (const [name, render, size] of [
  ["Checkbox", (p) => Checkbox(p), ["any-pointer-coarse:after:size-6"]],
  ["RadioGroupItem", (p) => RadioGroupItem(p), ["any-pointer-coarse:after:size-6"]],
  ["Switch", (p) => Switch(p), ["any-pointer-coarse:after:h-6", "any-pointer-coarse:after:w-full"]],
]) {
  test(`${name} gets a 24px minimum hit area on coarse pointers, anchored to itself`, () => {
    const tokens = render({}).props.className.split(/\s+/)
    assert.ok(tokens.includes("relative"), `${name} must be position: relative for its ::after`)
    for (const t of [...HIT_AREA, ...size]) assert.ok(tokens.includes(t), `${name} is missing ${t}`)
    // Never wider than 24px beyond the control: neighbours 24px apart must not overlap.
    assert.ok(!tokens.some((t) => /after:(size|w|h)-(7|8|9|10|11|12)\b/.test(t)), `${name} hit area grew past 24px`)
  })
}
