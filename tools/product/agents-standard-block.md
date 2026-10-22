<!-- BEGIN:elcano-frontend-standard v2 (shared verbatim by every Elcano repo; scripts/stack-check.sh pins its hash; change it everywhere or nowhere) -->
## Elcano frontend standard (v2)

Every Elcano web product follows one of two tiers. `stack.conf` at the repo
root declares which, and `scripts/stack-check.sh` (run by CI) enforces it.

**The server is Go and serves everything.** The browser talks to one origin:
the Go binary serves the HTML, the static assets and the JSON API, and it owns
sign-in (the `elcano_auth` cookie from the auth service), sessions, CSRF and
security headers. There is no Node, Python or other JavaScript server in
production. Static files ship inside the binary with `go:embed`; Caddy only
terminates TLS and reverse-proxies to Go.

**Tier A — server-rendered (the default).** Go `html/template` pages, plain
CSS that reads Flag tokens, and small plain-JavaScript modules (no framework,
no bundler, no transpiler, no npm runtime dependencies). npm may appear only
as a dev dependency for browser tests (Playwright, axe). Pick Tier A unless the
page is a long-lived, state-heavy application. Components use Flag's CSS
component classes, which mirror the names and states of Flag's shadcn/ui
components so both tiers look and behave alike.

**Tier B — interactive app.** React + TypeScript built by Vite into a static
bundle that the Go server embeds and serves (same origin, so no CORS). No
server-side rendering, no Next.js, no runtime server code in TypeScript; data
comes from the Go JSON API. Base UI components come from Flag's shadcn/ui
registry (React + Radix + Tailwind, themed by Flag tokens; registry URL in
Flag's README): `npx shadcn add` copies them into the app, where they live and
are reviewed like our own code. Build a component by hand only when the
registry lacks it, then upstream it to Flag. Keep other runtime npm
dependencies few and justified in AGENTS.md. Use Tier B only when Tier A would
mean re-implementing a client-side state framework by hand (streaming chat,
multi-step builders).

**Both tiers:**

- Design comes from Flag (`ElcanoTek/flag`). Vendored Flag files are listed in
  `flag.lock` with their hashes; `scripts/flag-sync.sh check` fails CI on any
  hand edit. Update with `scripts/flag-sync.sh sync`, never by editing in place.
  Product styling lives outside the vendored directories and reads tokens.
- No third-party CDNs: every script, stylesheet and font is served by our own
  binary. Fonts are Flag's Nebula Sans and Hack only.
- A strict Content-Security-Policy (no `unsafe-inline` scripts, no remote
  script hosts), `X-Content-Type-Options: nosniff`, and `frame-ancestors`.
- Hashed or versioned asset URLs with long-lived caching; HTML is `no-cache`.
- Accessibility is tested (Playwright + axe where a browser suite exists).
- Exceptions (a non-Go backend, an extra runtime dependency) are written down
  in this repo's AGENTS.md with the reason, not left implicit.
<!-- END:elcano-frontend-standard -->
