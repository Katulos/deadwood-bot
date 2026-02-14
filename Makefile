.DEFAULT_GOAL := help
.PHONY: help extract fluent, test

locales := locales

.PHONY: help
help: ## Display this help screen
	@grep -E '^[a-z.A-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: clean
clean: clean-build clean-test clean-pyc ## Clean project

.PHONY: clean-build
clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	rm -fr .mypy_cache
	rm -fr .ruff_cache
	find . -name '*.egg-info' -not -path '.venv/*' -exec rm -fr {} +
	find . -name '*.egg' -not -path '.venv/*' -exec rm -f {} +

.PHONY: clean-pyc
clean-pyc:
	find . -name '*.pyc' -not -path '.venv/*' -exec rm -f {} +
	find . -name '*.pyo' -not -path '.venv/*' -exec rm -f {} +
	find . -name '*~' -not -path '.venv/*' -exec rm -f {} +
	find . -name '__pycache__' -not -path '.venv/*' -exec rm -fr {} +

.PHONY: clean-test
clean-test:
	rm -fr .tox/
	rm -fr .nox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

.PHONY: nox
nox: clean  ## Run nox tests
	uvx nox

.PHONY: test
test: nox ## Run tests

.PHONY: pre-commit
pre-commit: clean ## Run pre-commit
	git add . && uvx pre-commit run -a

.PHONY: prc
prc: pre-commit

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
