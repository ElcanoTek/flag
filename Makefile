# Flag's checks and local preview. Nothing to install: sh, perl, python3.
.PHONY: check preview sync-email help

help: ## List targets
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | sed 's/:.*## /\t/'

check: ## Run every check CI runs
	@sh scripts/check-all.sh

preview: ## Serve the preview at http://localhost:8765/preview/
	@echo "Preview: http://localhost:8765/preview/"
	@cd design-system && python3 -m http.server 8765

sync-email: ## Copy email-safe.html into the preview after editing it
	@sh design-system/sync-email-preview.sh
