# QA Automation Framework - Makefile

.PHONY: help install install-allure test test-api test-web test-smoke clean clean-videos allure-report allure-serve

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

install-allure: ## Install Allure CLI (macOS with Homebrew)
	@echo "Installing Allure CLI..."
	brew install allure
	@echo "Allure installation complete. Run 'allure --version' to verify."

test: ## Run all tests
	poetry run pytest -v

test-parallel: ## Run all tests in parallel (auto-detect CPU cores)
	poetry run pytest -v -n auto

test-parallel-4: ## Run tests in parallel with 4 workers
	poetry run pytest -v -n 4

test-api: ## Run API tests only
	poetry run pytest team_alpha/tests/api/ -v

test-api-parallel: ## Run API tests in parallel
	poetry run pytest team_alpha/tests/api/ -v -n auto

test-web: ## Run web tests (headless)
	poetry run pytest team_alpha/tests/web/ -v

test-web-parallel: ## Run web tests in parallel (headless)
	poetry run pytest team_alpha/tests/web/ -v -n auto

test-web-headed: ## Run web tests with visible browser
	poetry run pytest team_alpha/tests/web/ --headed -v

test-smoke: ## Run smoke tests only
	poetry run pytest -m smoke -v

test-smoke-parallel: ## Run smoke tests in parallel
	poetry run pytest -m smoke -v -n auto

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

format: ## Format code with black and isort
	poetry run black .
	poetry run isort .

lint: ## Run linting with ruff
	poetry run ruff check .
