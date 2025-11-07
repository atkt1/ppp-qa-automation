# QA Automation Framework - Makefile

.PHONY: help install install-allure clean clean-videos allure-report allure-serve \
	alpha-test-all alpha-test-api alpha-test-web alpha-test-web-headed alpha-test-smoke \
	alpha-test-api-parallel alpha-test-web-parallel alpha-test-smoke-parallel \
	beta-test-all beta-test-api beta-test-web beta-test-web-headed beta-test-smoke \
	beta-test-api-parallel beta-test-web-parallel beta-test-smoke-parallel \
	gamma-test-all gamma-test-api gamma-test-web gamma-test-web-headed gamma-test-smoke \
	gamma-test-api-parallel gamma-test-web-parallel gamma-test-smoke-parallel \
	test-all test-one test-one-headed test-collect fixtures \
	format lint lint-fix format-check validate-yaml \
	install-hooks pre-commit pre-commit-update pr-ready

# Unexport environment variables to let .env file take precedence
unexport ENV
unexport WEB_BASE_URL
unexport API_BASE_URL
unexport HEADLESS
unexport API_AUTH_TOKEN
unexport RECORD_VIDEO

help: ## Show this help message
	@echo "QA Automation Framework - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""

install: ## Install all dependencies
	poetry install
	poetry run playwright install

install-hooks: ## Install pre-commit hooks
	poetry run pre-commit install
	@echo "✅ Pre-commit hooks installed successfully!"
	@echo "Hooks will run automatically on git commit"

install-allure: ## Install Allure CLI (macOS with Homebrew)
	@echo "Installing Allure CLI..."
	brew install allure
	@echo "Allure installation complete. Run 'allure --version' to verify."

# ==========================================
# Testing - Team Alpha
# ==========================================

alpha-test-all: ## Run all tests for Team Alpha
	poetry run pytest team_alpha/ -v

alpha-test-api: ## Run API tests for Team Alpha
	poetry run pytest team_alpha/tests/api/ -v

alpha-test-api-parallel: ## Run API tests in parallel for Team Alpha
	poetry run pytest team_alpha/tests/api/ -v -n auto

alpha-test-web: ## Run web tests (headless) for Team Alpha
	poetry run pytest team_alpha/tests/web/ -v

alpha-test-web-parallel: ## Run web tests in parallel for Team Alpha
	poetry run pytest team_alpha/tests/web/ -v -n auto

alpha-test-web-headed: ## Run web tests with visible browser for Team Alpha
	poetry run pytest team_alpha/tests/web/ --headed -v

alpha-test-smoke: ## Run smoke tests for Team Alpha
	poetry run pytest team_alpha/ -m smoke -v

alpha-test-smoke-parallel: ## Run smoke tests in parallel for Team Alpha
	poetry run pytest team_alpha/ -m smoke -v -n auto

# ==========================================
# Testing - Team Beta
# ==========================================

beta-test-all: ## Run all tests for Team Beta
	poetry run pytest team_beta/ -v

beta-test-api: ## Run API tests for Team Beta
	poetry run pytest team_beta/tests/api/ -v

beta-test-api-parallel: ## Run API tests in parallel for Team Beta
	poetry run pytest team_beta/tests/api/ -v -n auto

beta-test-web: ## Run web tests (headless) for Team Beta
	poetry run pytest team_beta/tests/web/ -v

beta-test-web-parallel: ## Run web tests in parallel for Team Beta
	poetry run pytest team_beta/tests/web/ -v -n auto

beta-test-web-headed: ## Run web tests with visible browser for Team Beta
	poetry run pytest team_beta/tests/web/ --headed -v

beta-test-smoke: ## Run smoke tests for Team Beta
	poetry run pytest team_beta/ -m smoke -v

beta-test-smoke-parallel: ## Run smoke tests in parallel for Team Beta
	poetry run pytest team_beta/ -m smoke -v -n auto

# ==========================================
# Testing - Team Gamma
# ==========================================

gamma-test-all: ## Run all tests for Team Gamma
	poetry run pytest team_gamma/ -v

gamma-test-api: ## Run API tests for Team Gamma
	poetry run pytest team_gamma/tests/api/ -v

gamma-test-api-parallel: ## Run API tests in parallel for Team Gamma
	poetry run pytest team_gamma/tests/api/ -v -n auto

gamma-test-web: ## Run web tests (headless) for Team Gamma
	poetry run pytest team_gamma/tests/web/ -v

gamma-test-web-parallel: ## Run web tests in parallel for Team Gamma
	poetry run pytest team_gamma/tests/web/ -v -n auto

gamma-test-web-headed: ## Run web tests with visible browser for Team Gamma
	poetry run pytest team_gamma/tests/web/ --headed -v

gamma-test-smoke: ## Run smoke tests for Team Gamma
	poetry run pytest team_gamma/ -m smoke -v

gamma-test-smoke-parallel: ## Run smoke tests in parallel for Team Gamma
	poetry run pytest team_gamma/ -m smoke -v -n auto

# ==========================================
# Testing - Utilities
# ==========================================

test-one: ## Run a single test (usage: make test-one TEST=path/to/test.py::TestClass::test_method)
	poetry run pytest $(TEST) -v

test-one-headed: ## Run a single web test with visible browser
	poetry run pytest $(TEST) --headed -v

test-collect: ## Show all available tests without running them
	poetry run pytest --collect-only -q

fixtures: ## List all available fixtures
	poetry run pytest --fixtures

allure-report: ## Generate Allure HTML report from results
	allure generate allure-results --clean -o allure-report

allure-serve: ## Generate and open Allure report in browser
	allure serve allure-results

clean: ## Clean up generated files
	rm -rf .pytest_cache allure-results allure-report logs/*.log videos screenshots

clean-videos: ## Clean up video recordings only
	rm -rf videos/*.webm
	@echo "Video files cleaned up"

format: ## Format and lint code (isort → black → ruff --fix → validate-yaml)
	@echo "Running code formatting and linting..."
	@echo "1/4 Running isort..."
	@poetry run isort .
	@echo "2/4 Running black..."
	@poetry run black .
	@echo "3/4 Running ruff with auto-fix..."
	@poetry run ruff check --fix .
	@echo "4/4 Validating YAML files..."
	@poetry run python scripts/validate_yaml.py
	@echo ""
	@echo "✅ All formatting and validation complete!"

lint: ## Run linting with ruff
	poetry run ruff check .

lint-fix: ## Run linting with auto-fix
	poetry run ruff check --fix .

format-check: ## Check if formatting is needed (CI mode)
	poetry run isort --check-only .
	poetry run black --check .
	poetry run ruff check .

validate-yaml: ## Validate all YAML files (syntax, duplicates, indentation)
	@poetry run python scripts/validate_yaml.py

pre-commit: ## Run all pre-commit checks manually
	@poetry run pre-commit run --all-files

pre-commit-update: ## Update pre-commit hooks to latest versions
	@poetry run pre-commit autoupdate

test-all: alpha-test-all ## Run all tests (defaults to Team Alpha for backward compatibility)

pr-ready: format alpha-test-all ## Comprehensive check before submitting PR (format + test)
	@echo ""
	@echo "======================================"
	@echo "✅ PR Ready Checks Completed!"
	@echo "======================================"
	@echo "✓ Code formatted (Black + isort)"
	@echo "✓ Linting passed (Ruff)"
	@echo "✓ YAML files validated"
	@echo "✓ All tests passed (Team Alpha)"
	@echo ""
	@echo "Your code is ready for PR submission!"
	@echo "Don't forget to:"
	@echo "  - Update documentation if needed"
	@echo "  - Add/update test cases"
	@echo "  - Fill out PR template completely"
	@echo "======================================"
