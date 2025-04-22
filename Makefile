.DEFAULT_GOAL := help
.PHONY: help extract fluent, test

locales := locales

.PHONY: help
help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

# i18n
.PHONY: extract
extract:
	@ftl_extract --default-ftl-file main.ftl \
		-k _ -k gettext -k ngettext -k i18n \
		-k I18N -k LF -k LazyProxy -k L -k I18NFormat \
		-l en -l ru \
		./app $(locales)

.PHONY: fluent
fluent: extract

.PHONY: test
test:  # Run tests
	pytest tests/
