# Flag's checks and local preview. Nothing to install: sh, perl, python3.
.PHONY: check audit preview sync help

help: ## List targets
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | sed 's/:.*## /\t/'

check: ## Run every check CI runs
	@sh scripts/check-all.sh

# Rendered audit (not in CI: needs Node, Playwright's Chromium and axe-core).
# Uses AUDIT_NODE_PATH if set, else installs both into .audit/ once.
AUDIT_NODE_PATH ?= .audit/node_modules
audit: ## Render the preview in Chromium: axe, computed contrast, focus, pickers open
	@if [ "$(AUDIT_NODE_PATH)" = ".audit/node_modules" ] && [ ! -d .audit/node_modules/axe-core ]; then \
	  npm install --no-save --silent --prefix .audit playwright axe-core && .audit/node_modules/.bin/playwright install chromium; fi
	@NODE_PATH=$(AUDIT_NODE_PATH) node scripts/audit_preview.mjs

preview: ## Serve the preview at http://localhost:8765/preview/
	@echo "Preview: http://localhost:8765/preview/"
	@cd design-system && python3 -m http.server 8765

sync: ## Refresh the preview copies of components.css and email-safe.html
	@sh design-system/sync-preview.sh
