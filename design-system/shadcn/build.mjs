#!/usr/bin/env node
// Builds Flag's shadcn/ui registry.
//
//   node build.mjs          validate registry.json against the vendored shadcn
//                           schemas (schema/, from ui.shadcn.com), format it,
//                           and run `shadcn build` into ../preview/r/ (served
//                           at https://flag.elcanotek.com/r/)
//   node build.mjs --check  the same into a temp dir; fail if registry.json is
//                           unformatted or ../preview/r/ differs from what is
//                           committed
//
// Run `npm ci` here first (pins shadcn and ajv exactly).

import { execFileSync } from "node:child_process"
import fs from "node:fs"
import os from "node:os"
import path from "node:path"
import { fileURLToPath } from "node:url"
import Ajv from "ajv"

const HERE = path.dirname(fileURLToPath(import.meta.url))
const OUT = path.resolve(HERE, "../preview/r")
const check = process.argv.includes("--check")
const fail = (msg) => {
  console.error(`shadcn-registry: ${msg}`)
  process.exit(1)
}

// --- validation ---------------------------------------------------------------

function validate(registry) {
  const schemas = path.join(HERE, "schema")
  const item = JSON.parse(fs.readFileSync(path.join(schemas, "registry-item.json"), "utf8"))
  const root = JSON.parse(fs.readFileSync(path.join(schemas, "registry.json"), "utf8"))
  // The schemas name draft-07 by its https URL, which ajv does not bundle;
  // skip meta-validation of the schemas themselves.
  const ajv = new Ajv({ allErrors: true, strict: false, validateSchema: false })
  ajv.addSchema(item, "https://ui.shadcn.com/schema/registry-item.json")
  const ok = ajv.validate(root, registry)
  if (!ok) fail("registry.json does not match the shadcn schema:\n" + ajv.errorsText(ajv.errors, { separator: "\n" }))
  for (const it of registry.items) {
    for (const f of it.files ?? []) {
      if (!fs.existsSync(path.join(HERE, f.path))) fail(`${it.name}: missing ${f.path}`)
    }
    for (const dep of it.registryDependencies ?? []) {
      const name = dep.replace(/^@flag\//, "")
      if (dep.startsWith("@flag/") && !registry.items.some((x) => x.name === name)) {
        fail(`${it.name}: registryDependency ${dep} is not in this registry`)
      }
    }
  }
}

// Every built file is valid against the shadcn schemas and carries its source.
function validateBuilt(dir) {
  const schemas = path.join(HERE, "schema")
  const ajv = new Ajv({ allErrors: true, strict: false, validateSchema: false })
  const item = JSON.parse(fs.readFileSync(path.join(schemas, "registry-item.json"), "utf8"))
  ajv.addSchema(item, "https://ui.shadcn.com/schema/registry-item.json")
  const root = JSON.parse(fs.readFileSync(path.join(schemas, "registry.json"), "utf8"))
  for (const f of fs.readdirSync(dir)) {
    const data = JSON.parse(fs.readFileSync(path.join(dir, f), "utf8"))
    const ok = f === "registry.json" ? ajv.validate(root, data) : ajv.validate(item.$id ?? "https://ui.shadcn.com/schema/registry-item.json", data)
    if (!ok) fail(`built ${f} does not match the shadcn schema:\n` + ajv.errorsText(ajv.errors, { separator: "\n" }))
    for (const file of data.files ?? []) {
      if (f !== "registry.json" && !file.content) fail(`built ${f}: ${file.path} has no content`)
    }
  }
}

// --- build --------------------------------------------------------------------

const regPath = path.join(HERE, "registry.json")
const registry = JSON.parse(fs.readFileSync(regPath, "utf8"))
validate(registry)
const regText = JSON.stringify(registry, null, 2) + "\n"

const shadcn = path.join(HERE, "node_modules", ".bin", "shadcn")
if (!fs.existsSync(shadcn)) fail("run `npm ci` in design-system/shadcn first")

if (!check) {
  fs.writeFileSync(regPath, regText)
  fs.rmSync(OUT, { recursive: true, force: true })
  execFileSync(shadcn, ["build", "registry.json", "-o", OUT], { cwd: HERE, stdio: "inherit" })
  validateBuilt(OUT)
  console.log(`shadcn-registry: built ${registry.items.length} items into ${path.relative(process.cwd(), OUT) || "."}`)
} else {
  if (fs.readFileSync(regPath, "utf8") !== regText) {
    fail("registry.json is not in canonical form; run `npm run build` in design-system/shadcn")
  }
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "flag-registry-"))
  try {
    execFileSync(shadcn, ["build", "registry.json", "-o", tmp], { cwd: HERE, stdio: "ignore" })
    validateBuilt(tmp)
    const want = fs.readdirSync(tmp).sort()
    const have = fs.existsSync(OUT) ? fs.readdirSync(OUT).sort() : []
    const diff = []
    for (const f of new Set([...want, ...have])) {
      const a = want.includes(f) ? fs.readFileSync(path.join(tmp, f), "utf8") : null
      const b = have.includes(f) ? fs.readFileSync(path.join(OUT, f), "utf8") : null
      if (a !== b) diff.push(f)
    }
    if (diff.length) fail(`preview/r/ is stale (${diff.join(", ")}); run \`npm run build\` in design-system/shadcn and commit`)
    console.log(`shadcn-registry: ok (${want.length} files match a fresh build)`)
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true })
  }
}
