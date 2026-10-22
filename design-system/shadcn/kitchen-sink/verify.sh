#!/bin/sh
# verify.sh — install Flag's shadcn registry into a throwaway Vite + React +
# TypeScript + Tailwind 4 app exactly as a Tier B product would, render the
# kitchen sink (App.tsx) in light and dark at 1440 and 390 px, and run axe.
#
#   sh design-system/shadcn/kitchen-sink/verify.sh [OUT_DIR] [--preview]
#
# Serves design-system/preview/ locally so the registry resolves at
# http://localhost:$PORT/r/{name}.json, the same path as production.
# Needs Node 22+, python3 and a Chromium for Playwright (PLAYWRIGHT_BROWSERS_PATH;
# the pinned playwright below matches chromium-1194). Writes PNGs and
# axe-report.json to OUT_DIR (default: a temp dir). --preview also refreshes
# the screenshots the Flag preview shows (preview/shadcn/*.webp; needs
# ImageMagick).
set -eu
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
DS=$(CDPATH= cd -- "$HERE/../.." && pwd)
OUT=${1:-$(mktemp -d)}
case "$OUT" in /*) ;; *) OUT="$PWD/$OUT" ;; esac
PORT=${PORT:-8812}
APP_PORT=$((PORT + 1))
WORK=$(mktemp -d)
cleanup() { kill $SRV $APPSRV 2>/dev/null || true; rm -rf "$WORK"; }
SRV=; APPSRV=
trap cleanup EXIT

(cd "$DS/preview" && exec python3 -m http.server "$PORT" >/dev/null 2>&1) & SRV=$!

cd "$WORK"
cat > package.json <<'JSON'
{
  "name": "flag-shadcn-kitchen-sink",
  "private": true,
  "type": "module",
  "dependencies": { "react": "19.3.1", "react-dom": "19.3.1" },
  "devDependencies": {
    "@axe-core/playwright": "4.11.3",
    "@tailwindcss/vite": "4.3.3",
    "@types/node": "22.15.0",
    "@types/react": "19.3.0",
    "@types/react-dom": "19.3.0",
    "@vitejs/plugin-react": "6.1.2",
    "playwright": "1.56.1",
    "tailwindcss": "4.3.3",
    "typescript": "5.9.3",
    "vite": "8.3.4"
  }
}
JSON
cat > vite.config.ts <<'TS'
import path from "node:path"
import react from "@vitejs/plugin-react"
import tailwindcss from "@tailwindcss/vite"
import { defineConfig } from "vite"
export default defineConfig({
  base: "./",
  plugins: [react(), tailwindcss()],
  resolve: { alias: { "@": path.resolve(__dirname, "./src") } },
})
TS
cat > tsconfig.json <<'JSON'
{
  "compilerOptions": {
    "target": "ES2022", "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext", "moduleResolution": "bundler", "jsx": "react-jsx",
    "strict": true, "noEmit": true, "skipLibCheck": true, "isolatedModules": true,
    "types": ["vite/client"], "baseUrl": ".", "paths": { "@/*": ["./src/*"] }
  },
  "include": ["src"]
}
JSON
cat > index.html <<'HTML'
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Flag shadcn kitchen sink</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
HTML
# components.json written by hand (see SHADCN.md), pointing @flag at the local server.
cat > components.json <<JSON
{
  "\$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": false,
  "tsx": true,
  "tailwind": { "config": "", "css": "src/index.css", "baseColor": "neutral", "cssVariables": true, "prefix": "" },
  "iconLibrary": "lucide",
  "aliases": { "components": "@/components", "utils": "@/lib/utils", "ui": "@/components/ui", "lib": "@/lib", "hooks": "@/hooks" },
  "registries": { "@flag": "http://localhost:$PORT/r/{name}.json" }
}
JSON
# The vendored Flag files (flag-sync in a real product).
mkdir -p src/flag/shadcn src/flag/theme
cp -R "$DS/fonts" "$DS/tokens" src/flag/
cp "$DS/shadcn/theme.css" src/flag/shadcn/theme.css
cp "$DS/theme/theme-controller.js" src/flag/theme/theme-controller.js
cat > src/index.css <<'CSS'
@import "tailwindcss";
@import "tw-animate-css";
@import "./flag/fonts/fonts.css";
@import "./flag/tokens/design-tokens.css";
@import "./flag/shadcn/theme.css";
CSS
cat > src/main.tsx <<'TSX'
import "./flag/theme/theme-controller.js"
import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import "./index.css"
import { App } from "./App"
createRoot(document.getElementById("root")!).render(<StrictMode><App /></StrictMode>)
TSX
echo 'declare module "*.js"' > src/vendored-js.d.ts
cp "$HERE/App.tsx" src/App.tsx

npm install --no-audit --no-fund >/dev/null
ITEMS=$(node -e 'console.log(require(process.argv[1]).items.map(i => "@flag/" + i.name).join(" "))' "$DS/shadcn/registry.json")
# shellcheck disable=SC2086
npx --yes shadcn@4.21.4 add $ITEMS -y
npx tsc --noEmit -p .
npx vite build >/dev/null

(cd dist && exec python3 -m http.server "$APP_PORT" >/dev/null 2>&1) & APPSRV=$!
sleep 1
cp "$HERE/shoot.mjs" ./shoot.mjs
node shoot.mjs "$OUT" "http://localhost:$APP_PORT/"

if [ "${2:-}" = "--preview" ]; then
  for t in dark light; do
    convert "$OUT/kitchen-sink-$t-1440.png" -quality 80 "$DS/preview/shadcn/kitchen-sink-$t.webp"
    for o in dialog dropdown select; do
      convert "$OUT/overlay-$o-$t-1440.png" -quality 80 "$DS/preview/shadcn/overlay-$o-$t.webp"
    done
  done
fi
echo "verify.sh: renders and axe-report.json in $OUT"
