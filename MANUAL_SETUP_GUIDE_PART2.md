# Manual Project Setup Guide - Part 2

**Continuation of manual setup guide**

This is Part 2 covering Phase 3 (Team Alpha) and Phase 4 (Configuration & Final Setup).

**Prerequisites**: Complete MANUAL_SETUP_GUIDE.md Part 1 first (Phases 1 & 2).

---

## Phase 3 Continued: Team Alpha Implementation

### Recap from Part 1

You should have created:
- ✅ `team_alpha/__init__.py`
- ✅ `team_alpha/conftest.py`
- ✅ `team_alpha/locators/__init__.py`
- ✅ `team_alpha/locators/locators.py`

---

### Step 3.6: Create Page Objects Package Init

**File**: `team_alpha/pages/__init__.py`

```python
"""
Page Objects Package for Team Alpha

Contains page object models for web UI automation.
"""

from team_alpha.pages.google_search_page import GoogleSearchPage
from team_alpha.pages.google_shopping_page import GoogleShoppingPage

__all__ = [
    'GoogleSearchPage',
    'GoogleShoppingPage',
]
```

---

### Step 3.7: Create Google Search Page Object

**File**: `team_alpha/pages/google_search_page.py`

**⚠️ IMPORTANT**: 94 lines - Type carefully

```python
"""
Google Search Page Object Model

Represents the Google search page with its elements and actions.
"""

from playwright.sync_api import Page, expect
from core.base.page_base import BasePage
from core.logger import log
from core.utils import handle_optional_dialog
from team_alpha.locators import GoogleSearchLocators


class GoogleSearchPage(BasePage):
    """
    Page Object for Google Search page.

    Provides methods to interact with Google search functionality.
    """

    def __init__(self, page: Page):
        """
        Initialize Google Search page.

        Args:
            page: Playwright Page object
        """
        super().__init__(page)

        # Store locators as page elements
        self.search_input = page.locator(GoogleSearchLocators.SEARCH_INPUT)
        self.search_button = page.locator(GoogleSearchLocators.SEARCH_BUTTON)
        self.shopping_tab = page.locator(GoogleSearchLocators.SHOPPING_TAB)
        self.search_results = page.locator(GoogleSearchLocators.SEARCH_RESULTS)

    def navigate_to_google(self):
        """Navigate to Google homepage."""
        from core.config import config
        log.info("Navigating to Google homepage")
        self.navigate(config.web_base_url)
        self.wait_for_load_state("networkidle")

    def search(self, query: str):
        """
        Perform a search on Google.

        Args:
            query: Search term to enter

        Example:
            >>> page = GoogleSearchPage(page)
            >>> page.search("playwright automation")
        """
        log.info(f"Searching for: {query}")

        # Handle cookie consent if present
        handle_optional_dialog(
            self.page,
            GoogleSearchLocators.COOKIE_ACCEPT_ALL,
            action="click",
            timeout=2000
        )

        # Perform search
        self.search_input.click()
        self.search_input.fill(query)
        self.search_input.press("Enter")

        # Wait for results
        self.wait_for_load_state("networkidle")

    def click_shopping_tab(self):
        """
        Click the Shopping tab in search results.

        Navigates from general search results to shopping results.
        """
        log.info("Clicking Shopping tab")
        self.shopping_tab.click()
        self.wait_for_load_state("networkidle")

    def get_search_results_count(self) -> int:
        """
        Get the number of search results displayed.

        Returns:
            Count of search result items
        """
        count = self.search_results.count()
        log.info(f"Found {count} search results")
        return count

    def verify_search_results_present(self):
        """
        Verify that search results are displayed.

        Raises:
            AssertionError: If no results are found
        """
        log.info("Verifying search results are present")
        expect(self.search_results.first).to_be_visible(timeout=10000)
        assert self.get_search_results_count() > 0, "No search results found"
```

**Verification**: `python -c "from team_alpha.pages import GoogleSearchPage; print('OK')"`

---

### Step 3.8: Create Google Shopping Page Object

**File**: `team_alpha/pages/google_shopping_page.py`

**⚠️ IMPORTANT**: 163 lines - Consider copying from source or breaking into sections

**SECTION 1: Imports and class definition**

```python
"""
Google Shopping Page Object Model

Represents Google Shopping search results page.
"""

from typing import List, Optional
from playwright.sync_api import Page, Locator
from core.base.page_base import BasePage
from core.logger import log
from core.utils import (
    extract_price_from_text,
    safe_extract_text,
    try_multiple_locators
)
from team_alpha.locators import GoogleShoppingLocators


class GoogleShoppingPage(BasePage):
    """
    Page Object for Google Shopping results page.

    Provides methods to interact with product listings.
    """

    def __init__(self, page: Page):
        """
        Initialize Google Shopping page.

        Args:
            page: Playwright Page object
        """
        super().__init__(page)

        # Product-related locators
        self.product_cards = page.locator(GoogleShoppingLocators.PRODUCT_CARDS)
```

**SECTION 2: Wait and verification methods**

```python
    def wait_for_products(self, timeout: int = 10000):
        """
        Wait for product cards to load.

        Args:
            timeout: Maximum wait time in milliseconds
        """
        log.info("Waiting for products to load")
        self.product_cards.first.wait_for(state="visible", timeout=timeout)
        self.wait_for_load_state("networkidle")

    def verify_products_displayed(self):
        """
        Verify that product cards are displayed.

        Raises:
            AssertionError: If no products found
        """
        log.info("Verifying products are displayed")
        count = self.get_product_count()
        assert count > 0, "No products found on the page"
        log.info(f"Products verified: {count} products displayed")

    def get_product_count(self) -> int:
        """
        Get the number of products displayed.

        Returns:
            Number of product cards visible
        """
        count = self.product_cards.count()
        log.info(f"Found {count} products")
        return count
```

**SECTION 3: Price extraction methods**

```python
    def get_first_product_price(self) -> str:
        """
        Extract price from the first product.

        Uses multiple fallback strategies to find price.

        Returns:
            Price string (e.g., "$1,299.99") or "Price not found"
        """
        log.info("Extracting first product price")

        # Strategy 1: Try multiple locators
        price_locators = [
            GoogleShoppingLocators.PRODUCT_PRICE,
            'span:has-text("$")',
            'div.a8Pemb',
        ]

        price_element = try_multiple_locators(
            self.page,
            price_locators,
            timeout=5000,
            return_first=True
        )

        if price_element:
            price = safe_extract_text(price_element.first, default="")
            if price:
                log.info(f"Found price: {price}")
                return price

        # Strategy 2: Search within first product card
        first_card = self.product_cards.first
        if first_card.is_visible(timeout=5000):
            card_text = safe_extract_text(first_card, default="")
            price = extract_price_from_text(card_text, currency_symbol="$")
            if price:
                log.info(f"Extracted price from card: {price}")
                return price

        # Strategy 3: Last resort - extract from entire page
        log.warning("Price not found with locators, trying page scan")
        all_text = self.page.content()
        price = extract_price_from_text(all_text, currency_symbol="$")
        if price:
            log.info(f"Extracted price from page: {price}")
            return price

        log.warning("Could not find product price")
        return "Price not found"
```

**SECTION 4: Product data extraction**

```python
    def get_first_product_title(self) -> str:
        """
        Get the title of the first product.

        Returns:
            Product title or "Title not found"
        """
        log.info("Getting first product title")

        first_card = self.product_cards.first
        if first_card.is_visible(timeout=5000):
            # Try to find title within the card
            title_selectors = GoogleShoppingLocators.PRODUCT_TITLE.split(', ')
            for selector in title_selectors:
                try:
                    title_elem = first_card.locator(selector).first
                    if title_elem.is_visible(timeout=2000):
                        title = safe_extract_text(title_elem)
                        if title:
                            log.info(f"Found title: {title}")
                            return title
                except Exception:
                    continue

        log.warning("Could not find product title")
        return "Title not found"

    def get_all_product_prices(self, max_count: int = 10) -> List[str]:
        """
        Extract prices from multiple products.

        Args:
            max_count: Maximum number of prices to extract

        Returns:
            List of price strings
        """
        log.info(f"Extracting up to {max_count} product prices")
        prices = []

        cards = self.product_cards.all()[:max_count]

        for idx, card in enumerate(cards, 1):
            try:
                card_text = safe_extract_text(card, default="")
                price = extract_price_from_text(card_text, currency_symbol="$")
                if price:
                    prices.append(price)
                    log.debug(f"Product {idx}: {price}")
            except Exception as e:
                log.debug(f"Could not extract price from product {idx}: {e}")
                continue

        log.info(f"Extracted {len(prices)} prices")
        return prices
```

**Verification**: `python -c "from team_alpha.pages import GoogleShoppingPage; print('OK')"`

---

### Step 3.9: Create API Clients Package Init

**File**: `team_alpha/api_clients/__init__.py`

```python
"""
API Clients Package for Team Alpha

Contains API client implementations for external services.
"""

from team_alpha.api_clients.reqres_api_client import ReqResApiClient

__all__ = ['ReqResApiClient']
```

---

### Step 3.10: Create ReqRes API Client

**File**: `team_alpha/api_clients/reqres_api_client.py`

**⚠️ IMPORTANT**: 183 lines - Consider copying from source

Due to length, here's a condensed version with key methods:

```python
"""
ReqRes API Client

Client for interacting with the ReqRes test API (https://reqres.in).
"""

import allure
from typing import Dict, Any
from playwright.sync_api import APIRequestContext, APIResponse
from core.base.api_client import BaseApiClient
from core.logger import log


class ReqResApiClient(BaseApiClient):
    """
    API client for ReqRes test API.

    Provides methods for user and resource management endpoints.
    """

    # Endpoint constants
    USERS_ENDPOINT = "/api/users"
    REGISTER_ENDPOINT = "/api/register"
    LOGIN_ENDPOINT = "/api/login"

    @allure.step("Get list of users (page {page})")
    def get_users(self, page: int = 1) -> APIResponse:
        """Get list of users."""
        log.info(f"Getting users list (page {page})")
        return self.get(self.USERS_ENDPOINT, params={"page": page})

    @allure.step("Get single user with ID: {user_id}")
    def get_user_by_id(self, user_id: int) -> APIResponse:
        """Get single user by ID."""
        endpoint = f"{self.USERS_ENDPOINT}/{user_id}"
        log.info(f"Getting user with ID: {user_id}")
        return self.get(endpoint)

    @allure.step("Create new user: {name}")
    def create_user(self, name: str, job: str) -> APIResponse:
        """Create a new user."""
        data = {"name": name, "job": job}
        log.info(f"Creating user: {name}, {job}")
        return self.post(self.USERS_ENDPOINT, data=data)

    @allure.step("Update user {user_id}")
    def update_user(self, user_id: int, name: str, job: str) -> APIResponse:
        """Update existing user."""
        endpoint = f"{self.USERS_ENDPOINT}/{user_id}"
        data = {"name": name, "job": job}
        log.info(f"Updating user {user_id}")
        return self.put(endpoint, data=data)

    @allure.step("Delete user {user_id}")
    def delete_user(self, user_id: int) -> APIResponse:
        """Delete a user."""
        endpoint = f"{self.USERS_ENDPOINT}/{user_id}"
        log.info(f"Deleting user {user_id}")
        return self.delete(endpoint)

    # Add more methods as needed...
```

**Note**: See source file for complete implementation with register/login methods.

**Verification**: `python -c "from team_alpha.api_clients import ReqResApiClient; print('OK')"`

---

**Continue to next section for test data and tests...**

## Step 3.11-3.14: Test Data Files

### Create `team_alpha/test_data/__init__.py`

```python
"""
Test Data Package for Team Alpha

Contains test data loaders and data files.
"""

from team_alpha.test_data.data_loader import (
    TeamAlphaDataLoader,
    load_product_data,
    load_search_query,
)

__all__ = [
    'TeamAlphaDataLoader',
    'load_product_data',
    'load_search_query',
]
```

### Create `team_alpha/test_data/google_shopping.yaml`

```yaml
# Test Data for Google Shopping Tests

products:
  gaming_laptop:
    search_query: "gaming laptop"
    expected_min_price: 500
    expected_results_count: 10

  smartphone:
    search_query: "iPhone 15"
    expected_min_price: 700
    expected_results_count: 5

  headphones:
    search_query: "wireless headphones"
    expected_min_price: 50
    expected_results_count: 10

search_queries:
  valid:
    - "laptop"
    - "smartphone"
    - "tablet"

  invalid:
    - ""
    - "   "

config:
  default_timeout: 30000
  retry_attempts: 3
```

### Create `team_alpha/test_data/data_loader.py`

```python
"""
Team Alpha Data Loader

Loads test data from YAML files specific to Team Alpha.
"""

from pathlib import Path
from dataclasses import dataclass
from typing import List
from core.data import BaseYamlDataLoader


@dataclass
class ProductData:
    """Product test data model."""
    search_query: str
    expected_min_price: int
    expected_results_count: int


class TeamAlphaDataLoader(BaseYamlDataLoader):
    """Team Alpha specific data loader."""

    def __init__(self):
        yaml_file = Path(__file__).parent / "google_shopping.yaml"
        super().__init__(yaml_file)

    def get_product(self, product_key: str) -> ProductData:
        """Get product data by key."""
        product = self.get_section_item("products", product_key)
        return ProductData(**product)

    def get_search_queries(self, category: str = "valid") -> List[str]:
        """Get search queries list."""
        return self.get_section_item("search_queries", category)


# Convenience functions
_loader = TeamAlphaDataLoader()

def load_product_data(key: str) -> ProductData:
    """Load product data by key."""
    return _loader.get_product(key)

def load_search_query(category: str = "valid") -> List[str]:
    """Load search queries."""
    return _loader.get_search_queries(category)
```

---

## Phase 3: Tests

Due to the large number of test files, here's a summary approach:

### Test Files to Create:

1. **`team_alpha/tests/__init__.py`** - Empty or basic docstring
2. **`team_alpha/tests/api/__init__.py`** - Empty
3. **`team_alpha/tests/web/__init__.py`** - Empty
4. **`team_alpha/tests/api/test_reqres_users.py`** - API tests (~150 lines)
5. **`team_alpha/tests/web/test_google_search.py`** - Basic search tests (~80 lines)
6. **`team_alpha/tests/web/test_google_shopping.py`** - Shopping tests (~120 lines)

**Recommendation**: Copy these test files from source as they are:
- Educational (show test patterns)
- Contain working examples
- Easier to copy than type (500+ lines total)

**Quick reference for test structure**:

```python
# test_example.py
import pytest
import allure
from playwright.sync_api import Page

@pytest.mark.team_alpha
@pytest.mark.ui
@allure.feature("Feature Name")
class TestFeature:

    @pytest.mark.smoke
    @allure.title("Test description")
    def test_something(self, page: Page):
        # Arrange
        # Act
        # Assert
        pass
```

---

## Phase 4: Configuration & Final Setup

### Step 4.1: Create `core/conftest.py`

**File**: `core/conftest.py` - Root-level pytest configuration

```python
"""
Core Pytest Configuration

Root-level fixtures available to all teams.
"""

import pytest
from playwright.sync_api import Page, APIRequestContext, Playwright
from core.config import config
from core.logger import log


def pytest_configure(config_obj):
    """Configure pytest with custom markers."""
    config_obj.addinivalue_line("markers", "team_alpha: Team Alpha tests")
    config_obj.addinivalue_line("markers", "ui: Web UI tests")
    config_obj.addinivalue_line("markers", "api: API tests")
    config_obj.addinivalue_line("markers", "smoke: Smoke tests")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context with custom settings."""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "record_video_dir": "videos/" if config.record_video else None,
    }


@pytest.fixture
def api_request_context(playwright: Playwright) -> APIRequestContext:
    """Fixture providing API request context."""
    context = playwright.request.new_context(
        base_url=config.api_base_url,
        extra_http_headers={
            "Content-Type": "application/json",
        }
    )
    yield context
    context.dispose()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach screenshot on test failure."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            screenshot_path = f"screenshots/failure_{item.name}.png"
            page.screenshot(path=screenshot_path, full_page=True)
            log.info(f"Screenshot saved: {screenshot_path}")
```

---

### Step 4.2: Create `pytest.ini`

**File**: `pytest.ini`

```ini
[pytest]
# Pytest configuration for the test automation framework

# Test discovery
python_files = test_*.py
python_classes = Test*
python_functions = test_*
testpaths = team_alpha

# Output options
addopts =
    -v
    --strict-markers
    --tb=short
    --alluredir=allure-results
    --clean-alluredir

# Markers
markers =
    team_alpha: Team Alpha tests
    ui: Web UI tests
    api: API tests
    smoke: Smoke tests that run quickly
    regression: Full regression test suite
    slow: Tests that take longer to execute

# Logging
log_cli = false
log_cli_level = INFO
log_file = logs/pytest.log
log_file_level = DEBUG

# Warnings
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
```

---

### Step 4.3: Create `Makefile`

**File**: `Makefile`

```makefile
# Makefile for Test Automation Framework

.PHONY: help install test-all test-api test-web test-smoke clean

# Default target
help:
	@echo "Available commands:"
	@echo "  make install          - Install dependencies"
	@echo "  make test-all         - Run all tests"
	@echo "  make test-api         - Run API tests only"
	@echo "  make test-web         - Run web UI tests only"
	@echo "  make test-smoke       - Run smoke tests only"
	@echo "  make allure-report    - Generate Allure report"
	@echo "  make allure-serve     - Generate and open Allure report"
	@echo "  make clean-videos     - Clean video recordings"
	@echo "  make clean            - Clean all generated files"

# Install dependencies
install:
	poetry install
	poetry run playwright install chromium

# Run all tests
test-all:
	poetry run pytest

# Run API tests
test-api:
	poetry run pytest -m api

# Run web UI tests
test-web:
	poetry run pytest -m ui

# Run smoke tests
test-smoke:
	poetry run pytest -m smoke

# Run tests in headed mode
test-headed:
	HEADLESS=false poetry run pytest

# Run single test
test-one:
	poetry run pytest -k "$(TEST)"

# Generate Allure report
allure-report:
	allure generate allure-results --clean -o allure-report

# Generate and serve Allure report
allure-serve:
	allure serve allure-results

# Install Allure (MacOS)
install-allure:
	brew install allure

# Clean video recordings
clean-videos:
	rm -rf videos/

# Clean all generated files
clean:
	rm -rf .pytest_cache/
	rm -rf allure-results/
	rm -rf allure-report/
	rm -rf videos/
	rm -rf screenshots/
	rm -rf logs/
	find . -type d -name __pycache__ -exec rm -rf {} +
```

---

## 💾 CHECKPOINT 3 - FINAL

**At this point, you should have:**
- ✅ Complete core framework (14 files)
- ✅ Team Alpha implementation (20+ files)
- ✅ Configuration files (3 files)
- ✅ All tests ready to run

**Total: 43 files complete (100%)**

---

## Phase 5: Verification & First Run

### Step 5.1: Install Dependencies

```bash
cd qa-automation-framework
poetry install
poetry run playwright install chromium
```

### Step 5.2: Verify Framework

```bash
# Verify core imports
python -c "from core.config import config; from core.base import BasePage; print('Core OK')"

# Verify team imports
python -c "from team_alpha.pages import GoogleSearchPage; print('Team Alpha OK')"

# Verify utilities
python -c "from core.utils import extract_price_from_text; print('Utils OK')"
```

### Step 5.3: Run Tests

```bash
# Collect tests (should show 12 tests)
poetry run pytest --collect-only

# Run smoke tests
make test-smoke

# Run all tests
make test-all

# Generate report
make allure-serve
```

---

## 🎉 Success Checklist

- [ ] All 43 files created
- [ ] Dependencies installed
- [ ] Playwright browsers installed
- [ ] Tests collect successfully (12 tests)
- [ ] Smoke tests pass
- [ ] Allure report generates
- [ ] No import errors

---

## Troubleshooting

### Import Errors
```bash
# Check Python path
python -c "import sys; print('\n'.join(sys.path))"

# Verify pyproject.toml packages setting
poetry install --no-cache
```

### Test Discovery Issues
```bash
# Check pytest can find tests
pytest --collect-only -v
```

### Browser Issues
```bash
# Reinstall browsers
poetry run playwright install --force chromium
```

---

## Next Steps

1. **Customize**: Update .env with your actual test URLs
2. **Expand**: Add more teams following Team Alpha pattern
3. **CI/CD**: Add .gitlab-ci.yml or similar
4. **Documentation**: Customize README.md for your team

---

## File Structure - Complete

```
qa-automation-framework/
├── .gitignore
├── .env
├── pyproject.toml
├── pytest.ini
├── Makefile
├── core/
│   ├── __init__.py
│   ├── config.py
│   ├── logger.py
│   ├── conftest.py
│   ├── base/
│   │   ├── __init__.py
│   │   ├── page_base.py
│   │   └── api_client.py
│   ├── data/
│   │   ├── __init__.py
│   │   └── yaml_loader.py
│   └── utils/
│       ├── __init__.py
│       ├── string_utils.py
│       ├── wait_utils.py
│       └── element_utils.py
└── team_alpha/
    ├── __init__.py
    ├── conftest.py
    ├── pages/
    │   ├── __init__.py
    │   ├── google_search_page.py
    │   └── google_shopping_page.py
    ├── api_clients/
    │   ├── __init__.py
    │   └── reqres_api_client.py
    ├── locators/
    │   ├── __init__.py
    │   └── locators.py
    ├── test_data/
    │   ├── __init__.py
    │   ├── data_loader.py
    │   └── google_shopping.yaml
    └── tests/
        ├── __init__.py
        ├── api/
        │   ├── __init__.py
        │   └── test_reqres_users.py
        └── web/
            ├── __init__.py
            ├── test_google_search.py
            └── test_google_shopping.py
```

---

**Manual Setup Guide Complete! 🎊**

You now have a fully functional QA test automation framework ready for use in your secure environment.
