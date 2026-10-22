# Flag's checks and local preview. Nothing to install: sh, perl, python3.
.PHONY: check preview sync help

help: ## List targets
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | sed 's/:.*## /\t/'

check: ## Run every check CI runs
	@sh scripts/check-all.sh

preview: ## Serve the preview at http://localhost:8765/preview/
	@echo "Preview: http://localhost:8765/preview/"
	@cd design-system && python3 -m http.server 8765

sync: ## Refresh the preview copies of components.css and email-safe.html
	@sh design-system/sync-preview.sh
