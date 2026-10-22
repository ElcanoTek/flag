# Product tools

The canonical copies of the files every Elcano product repo shares verbatim
with every other one. They live here, outside `design-system/`, so they are
never vendored as design files; a product copies them once and keeps them
byte-identical afterwards.

| File | Version | Goes to (in the product) | What it does |
| --- | --- | --- | --- |
| [`flag-sync.sh`](flag-sync.sh) | `FLAG_SYNC_VERSION=15` | `scripts/flag-sync.sh` | Vendors Flag files and records them in `flag.lock`; `check` is the offline drift gate |
| [`stack-check.sh`](stack-check.sh) | `STACK_CHECK_VERSION=24` | `scripts/stack-check.sh` | The PR gate for the Elcano frontend standard (reads `stack.conf`; runs `flag-sync.sh check`) |
| [`flag-drift.yml`](flag-drift.yml) | | `.github/workflows/flag-drift.yml` | Weekly job: runs `flag-sync.sh status` against Flag's `main` |
| [`agents-standard-block.md`](agents-standard-block.md) | block v2 | pasted into `AGENTS.md` | The shared standard; `stack-check.sh` pins its sha256 |

Both scripts locate the product root as the parent of their own directory, so
they only work from a product's `scripts/`; do not run them from here.

## Bootstrapping a product

From the product repo root, with Flag checked out beside it as `../flag`:

```sh
mkdir -p scripts .github/workflows
cp ../flag/tools/product/flag-sync.sh ../flag/tools/product/stack-check.sh scripts/
cp ../flag/tools/product/flag-drift.yml .github/workflows/
chmod +x scripts/flag-sync.sh scripts/stack-check.sh
# Paste agents-standard-block.md into AGENTS.md unchanged, then write
# stack.conf (tier=, web=, npm=, backend=; see the header of stack-check.sh).
scripts/flag-sync.sh add ../flag tokens/design-tokens.css static/flag/tokens/design-tokens.css
scripts/flag-sync.sh add ../flag LICENSE static/flag/LICENSE
scripts/stack-check.sh
```

`add` paths name a file under Flag's `design-system/` first, then the
destination in the product. [APPLY_TO_PRODUCT.md](../../design-system/APPLY_TO_PRODUCT.md#vendoring-and-drift)
has the full workflow.

## Changing them

These files change in every product at once or not at all: bump the
version line, update this table and APPLY_TO_PRODUCT.md (`make check` fails
when the versions they name differ from the scripts, or when either script is
not shellcheck-clean), then copy the new file into every product repo.
