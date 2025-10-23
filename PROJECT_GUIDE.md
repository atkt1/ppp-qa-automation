# QA Test Automation Framework - Complete Project Guide

**A comprehensive guide to understanding the structure, purpose, and usage of every component in the test automation framework.**

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture & Design Patterns](#architecture--design-patterns)
3. [Directory Structure](#directory-structure)
4. [Configuration Files](#configuration-files)
5. [Core Framework](#core-framework)
6. [Team Alpha Implementation](#team-alpha-implementation)
7. [Running Tests](#running-tests)
8. [Adding New Teams](#adding-new-teams)
9. [Best Practices](#best-practices)

---

## 🎯 Project Overview

### Purpose
This is a **multi-team test automation framework** built with **Python, Playwright, and pytest**. It supports:
- **Web UI testing** with Page Object Model (POM)
- **API testing** with REST clients
- **Multiple teams** working independently
- **YAML-based test data** management
- **Comprehensive reporting** with Allure
- **CI/CD integration** with GitLab CI

### Technology Stack
- **Python 3.9+** - Programming language
- **Playwright** - Browser automation (Chromium, Firefox, WebKit)
- **pytest** - Test framework
- **Poetry** - Dependency management
- **Allure** - Test reporting
- **Loguru** - Advanced logging
- **PyYAML** - Test data management

### Key Features
✅ Page Object Model for maintainable UI tests
✅ Reusable base classes and utilities
✅ Team isolation (team_alpha, team_beta, team_gamma)
✅ Centralized locator management
✅ YAML test data with type safety
✅ Video recording and screenshots
✅ Parallel test execution
✅ Comprehensive logging

---

## 🏗️ Architecture & Design Patterns

### Design Patterns Used

1. **Page Object Model (POM)**
   - Separates page structure from test logic
   - Each page is a Python class with methods for interactions
   - Example: `GoogleSearchPage`, `GoogleShoppingPage`

2. **Singleton Pattern**
   - Used in: Configuration (`Config`), YAML data loaders
   - Ensures one instance, improves performance

3. **Factory Pattern**
   - Base classes create concrete implementations
   - `BasePage`, `BaseApiClient`, `BaseYamlDataLoader`

4. **Repository Pattern**
   - Centralized data access through data loaders
   - YAML files act as data repositories

### Framework Layers

```
┌─────────────────────────────────────────┐
│         Tests (test_*.py)               │  ← Test cases
├─────────────────────────────────────────┤
│     Page Objects / API Clients          │  ← Business logic
├─────────────────────────────────────────┤
│  Locators / Test Data (YAML)            │  ← Data layer
├─────────────────────────────────────────┤
│    Core Framework (base classes)        │  ← Reusable components
├─────────────────────────────────────────┤
│    Playwright / pytest                   │  ← Test infrastructure
└─────────────────────────────────────────┘
```

---

## 📁 Directory Structure

```
ppMonoRepo/
│
├── 🔧 Configuration Files (Root Level)
│   ├── .env                        # Environment variables
│   ├── .gitignore                  # Git ignore rules
│   ├── .gitlab-ci.yml              # CI/CD pipeline
│   ├── Makefile                    # Build automation
│   ├── pyproject.toml              # Poetry dependencies
│   ├── pytest.ini                  # Pytest configuration
│   └── conftest.py                 # Root-level pytest fixtures
│
├── 🎯 Core Framework
│   └── core/
│       ├── __init__.py
│       ├── config.py               # Configuration management
│       ├── logger.py               # Logging setup
│       ├── conftest.py             # Core fixtures
│       ├── base/                   # Base classes
│       │   ├── page_base.py        # BasePage for all pages
│       │   └── api_client.py       # BaseApiClient for APIs
│       ├── data/                   # Data utilities
│       │   └── yaml_loader.py      # Generic YAML loader
│       └── utils/                  # Utility functions
│           ├── string_utils.py     # Text processing
│           ├── wait_utils.py       # Retry & wait logic
│           └── element_utils.py    # Element interactions
│
├── 👥 Team Alpha (Example Implementation)
│   └── team_alpha/
│       ├── __init__.py
│       ├── conftest.py             # Team-specific fixtures
│       ├── locators/               # Centralized locators
│       │   ├── __init__.py
│       │   └── locators.py         # All page locators
│       ├── pages/                  # Page Object Models
│       │   ├── google_search_page.py
│       │   └── google_shopping_page.py
│       ├── api_clients/            # API client implementations
│       │   └── reqres_api_client.py
│       ├── test_data/              # Test data management
│       │   ├── data_loader.py      # Team's data loader
│       │   ├── google_shopping.yaml # Test data
│       │   └── README.md           # Usage docs
│       └── tests/                  # Test cases
│           ├── api/                # API tests
│           │   └── test_reqres_api.py
│           ├── web/                # Web UI tests
│           │   └── test_google_shopping.py
│           └── integration/        # Integration tests
│
├── 🚀 Team Beta (Placeholder)
│   └── team_beta/
│       └── README.md               # Setup instructions
│
├── 🚀 Team Gamma (Placeholder)
│   └── team_gamma/
│       └── README.md               # Setup instructions
│
└── 📂 Generated Directories (gitignored)
    ├── logs/                       # Test execution logs
    ├── screenshots/                # Failure screenshots
    ├── videos/                     # Test recordings
    ├── allure-results/             # Raw Allure data
    └── allure-report/              # Generated reports
```

---

## ⚙️ Configuration Files

### Root Level Configuration

#### `.env`
**Purpose**: Environment-specific configuration variables

**Key Settings**:
```env
ENV=local                           # Environment: local, dev, staging, prod
WEB_BASE_URL=https://www.google.com # Web application URL
API_BASE_URL=https://reqres.in      # API base URL
API_AUTH_TOKEN=reqres-free-v1       # API authentication token
HEADLESS=false                      # Run browser in headless mode
BROWSER=chromium                    # Browser: chromium, firefox, webkit
RECORD_VIDEO=true                   # Enable video recording
PYTEST_WORKERS=auto                 # Parallel execution workers
```

**When to modify**:
- Changing test environments
- Testing different browsers
- Enabling/disabling video recording
- Adjusting parallel execution

---

#### `pyproject.toml`
**Purpose**: Python project configuration and dependencies (Poetry)

**Sections**:
```toml
[tool.poetry]                       # Project metadata
name = "qa-automation"
version = "1.0.0"
python = ">=3.9,<3.12"

[tool.poetry.dependencies]          # Production dependencies
playwright = "^1.48.0"
pytest = "^7.4.0"
pytest-playwright = "^0.4.4"
allure-pytest = "^2.13.0"
pyyaml = "^6.0.3"
loguru = "^0.7.0"
python-dotenv = "^1.0.0"
faker = "^19.0.0"

[tool.poetry.group.dev.dependencies] # Dev dependencies
pytest-xdist = "^3.5.0"             # Parallel execution
```

**When to modify**:
- Adding new Python packages
- Updating dependency versions
- Adding development tools

---

#### `pytest.ini`
**Purpose**: Pytest configuration and test behavior

**Configuration**:
```ini
[pytest]
testpaths = team_alpha team_beta team_gamma  # Where to find tests

# Markers for test categorization
markers =
    smoke: Smoke tests (critical path)
    regression: Full regression suite
    api: API tests
    ui: UI tests
    team_alpha: Team Alpha tests
    team_beta: Team Beta tests

# Test output options
addopts =
    --strict-markers              # Fail on unknown markers
    -v                            # Verbose output
    --tb=short                    # Short traceback format
    --alluredir=allure-results    # Allure report directory
    --clean-alluredir             # Clean before generating

# Logging
log_cli = true                    # Show logs in console
log_cli_level = INFO              # Log level
```

**When to modify**:
- Adding new test markers
- Changing test discovery paths
- Adjusting logging levels
- Modifying Allure settings

---

#### `Makefile`
**Purpose**: Command automation and shortcuts

**Available Commands**:
```makefile
make help                 # Show all available commands
make install              # Install dependencies
make install-browsers     # Install Playwright browsers
make test-api             # Run API tests only
make test-web             # Run web tests only
make test-all             # Run all tests
make test-smoke           # Run smoke tests
make allure-report        # Generate Allure report
make allure-serve         # Generate and open report
make clean-videos         # Delete video recordings
```

**When to modify**:
- Adding new test execution shortcuts
- Creating team-specific commands
- Adding cleanup tasks

---

#### `.gitlab-ci.yml`
**Purpose**: CI/CD pipeline configuration for GitLab

**Pipeline Stages**:
```yaml
stages:
  - install      # Install dependencies
  - test         # Run tests
  - report       # Generate reports

# Example job
team_alpha_tests:
  stage: test
  script:
    - make test-team-alpha
  artifacts:
    paths:
      - allure-results/
      - logs/
      - screenshots/
```

**When to modify**:
- Adding new test jobs for teams
- Changing CI environment
- Modifying artifact retention

---

#### `conftest.py` (Root)
**Purpose**: Global pytest fixtures available to all teams

**What it provides**:
- Common test setup/teardown
- Shared fixtures accessible everywhere
- Currently minimal - most fixtures in `core/conftest.py`

---

## 🎯 Core Framework

### `core/` - Reusable Framework Components

#### `core/config.py`
**Purpose**: Centralized configuration management (Singleton)

**Functionality**:
```python
from core.config import config

# Access configuration anywhere
config.api_base_url        # https://reqres.in
config.headless            # True/False
config.browser             # chromium/firefox/webkit
config.record_video        # True/False
```

**Key Features**:
- Loads from `.env` file
- Type conversion (string to bool/int)
- Default values for missing settings
- Singleton pattern (one instance)

**When to modify**:
- Adding new configuration parameters
- Changing default values
- Adding validation logic

---

#### `core/logger.py`
**Purpose**: Logging configuration using Loguru

**Features**:
```python
from core.logger import log

log.info("Test started")
log.warning("Element not found")
log.error("Test failed")
log.debug("Detailed debug info")
```

**Configuration**:
- **File**: `logs/test_run_{date}.log`
- **Rotation**: Daily rotation
- **Compression**: Old logs compressed to `.gz`
- **Retention**: 7 days
- **Format**: Timestamp, level, module, function, message

**When to modify**:
- Changing log retention period
- Adjusting log format
- Adding custom log sinks

---

#### `core/conftest.py`
**Purpose**: Core pytest fixtures for all teams

**Key Fixtures**:

1. **`api_request_context`** (session scope)
   ```python
   def test_api(api_request_context):
       response = api_request_context.get("/users")
   ```
   - Creates Playwright API context
   - Adds authentication headers
   - Shared across all tests in session

2. **`browser_type_launch_args`** (session scope)
   - Configures browser launch arguments
   - Handles headless vs headed mode
   - Sets window size and flags

3. **`browser_context_args`** (session scope)
   - Configures browser context
   - Sets viewport size
   - Enables video recording if configured

4. **`test_logging`** (function scope, autouse)
   - Logs test start/completion
   - Captures test information

5. **`pytest_runtest_makereport`** (hook)
   - Captures screenshots on failure
   - Logs test results

**When to modify**:
- Adding global fixtures
- Changing browser configuration
- Modifying failure handling

---

### `core/base/` - Base Classes

#### `core/base/page_base.py`
**Purpose**: Base class for all Page Object Models

**Provides Common Methods**:
```python
from core.base.page_base import BasePage

class MyPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    # Inherit methods:
    # - navigate(url)
    # - get_title()
    # - wait_for_element(selector)
    # - click(selector)
    # - fill(selector, text)
    # - take_screenshot(name)
    # - etc.
```

**Available Methods**:
- `navigate(url)` - Go to URL
- `get_title()` - Get page title
- `get_url()` - Get current URL
- `wait_for_element(selector)` - Wait for element
- `click(selector)` - Click element
- `fill(selector, text)` - Fill input
- `is_visible(selector)` - Check visibility
- `take_screenshot(name)` - Capture screenshot
- `wait_for_load_state(state)` - Wait for page load

**When to extend**:
- Every page object should inherit from BasePage
- Add custom methods in subclasses

---

#### `core/base/api_client.py`
**Purpose**: Base class for all API clients

**Provides HTTP Methods**:
```python
from core.base.api_client import BaseApiClient

class MyApiClient(BaseApiClient):
    def get_users(self):
        return self.get("/users")

    # Inherit methods:
    # - get(endpoint, params, headers)
    # - post(endpoint, data, headers)
    # - put(endpoint, data, headers)
    # - patch(endpoint, data, headers)
    # - delete(endpoint, headers)
    # - assert_status_code(response, expected)
```

**Features**:
- Automatic logging of requests/responses
- Error handling
- Response validation helpers
- JSON parsing

**When to extend**:
- Create API client per API (e.g., ReqResApiClient)
- Add domain-specific methods

---

### `core/data/` - Data Management

#### `core/data/yaml_loader.py`
**Purpose**: Generic base class for YAML test data loading

**Usage Pattern**:
```python
from core.data import BaseYamlDataLoader

class MyTeamDataLoader(BaseYamlDataLoader):
    def __init__(self):
        yaml_file = Path(__file__).parent / "data.yaml"
        super().__init__(yaml_file)

    def get_user(self, key: str):
        data = self.get_section_item("users", key)
        return UserData(**data)
```

**Features**:
- **Singleton pattern**: One instance per subclass
- **Caching**: YAML loaded once, cached
- **Generic accessors**: `get_section()`, `get_section_item()`
- **Error handling**: Clear messages for missing data
- **Helper methods**: `list_sections()`, `has_section()`

**Why use it**:
- Eliminates YAML loading boilerplate
- Consistent pattern across teams
- Type-safe with data classes
- Performance optimization with caching

---

### `core/utils/` - Utility Functions

#### `core/utils/string_utils.py`
**Purpose**: String and text processing utilities

**Key Functions**:
```python
from core.utils import extract_price_from_text, sanitize_text

# Extract price from text
price = extract_price_from_text("Product costs $1,299.99")  # "$1,299.99"
price_float = extract_price_from_text("$999.99", return_as_float=True)  # 999.99

# Clean text
clean = sanitize_text("  Hello   World  \n  ")  # "Hello World"

# Truncate
short = truncate_text("Long text...", max_length=20)  # "Long text..."

# Extract patterns
email = extract_email_from_text("Contact: user@example.com")
url = extract_url_from_text("Visit https://example.com")
```

**Use cases**:
- Price extraction from e-commerce sites
- Data cleaning and normalization
- Pattern extraction (emails, URLs, numbers)
- Text formatting

---

#### `core/utils/wait_utils.py`
**Purpose**: Wait, retry, and polling utilities

**Key Functions**:
```python
from core.utils import wait_with_retry, retry_on_exception, wait_for_condition

# Retry a function
result = wait_with_retry(
    lambda: get_element(),
    max_attempts=3,
    wait_time=2.0,
    exponential_backoff=True
)

# Use as decorator
@retry_on_exception(max_attempts=3, wait_time=1.0)
def flaky_operation():
    return api.get_data()

# Wait for condition
wait_for_condition(
    lambda: element.is_visible(),
    timeout=30.0,
    poll_interval=0.5
)
```

**Use cases**:
- Handling flaky tests
- Polling dynamic content
- API rate limiting
- Waiting for state changes

---

#### `core/utils/element_utils.py`
**Purpose**: Playwright element interaction helpers

**Key Functions**:
```python
from core.utils import handle_optional_dialog, safe_extract_text, try_multiple_locators

# Handle optional dialogs (cookie consent, popups)
handle_optional_dialog(page, "button:has-text('Accept')", action="click")

# Safe text extraction with fallback
text = safe_extract_text(element, default="Not found", timeout=3000)

# Try multiple selectors
element = try_multiple_locators(
    page,
    ["span.price", "div.product-price", "span:has-text('$')"],
    return_first=True
)

# Safe click with retries
safe_click(element, timeout=5000, retry_count=3)
```

**Use cases**:
- Handling optional popups/dialogs
- Robust element interaction
- Fallback strategies for locators
- Dynamic page handling

---

## 👥 Team Alpha Implementation

### Overview
Team Alpha is the **reference implementation** showing how to structure team-specific code.

### `team_alpha/conftest.py`
**Purpose**: Team-specific fixtures and configuration

**Key Fixture**:
```python
@pytest.fixture
def reqres_api_client(api_request_context):
    """Provides ReqRes API client for tests"""
    return ReqResApiClient(api_request_context)
```

**Autouse Fixture**:
```python
@pytest.fixture(autouse=True)
def log_test_info(request):
    """Automatically logs test information"""
    # Runs before/after every test in team_alpha
```

---

### `team_alpha/locators/`

#### `locators.py`
**Purpose**: Centralized locators for all pages

**Structure**:
```python
class GoogleSearchLocators:
    """All Google Search page selectors"""
    SEARCH_INPUT = 'textarea[name="q"]'
    SEARCH_BUTTON = 'button[type="submit"]'
    SHOPPING_TAB = 'a[href*="tbm=shop"]'
    COOKIE_ACCEPT_ALL = 'button:has-text("Accept all")'

class GoogleShoppingLocators:
    """All Google Shopping page selectors"""
    PRODUCT_PRICE = 'span[aria-label*="$"]'
    PRODUCT_TITLE = 'h3, h4'
    FILTER_PRICE = 'button:has-text("Price")'
```

**Benefits**:
- ✅ One place to update selectors
- ✅ Easy to maintain
- ✅ Reusable across tests
- ✅ Version control friendly

#### `__init__.py`
**Purpose**: Package exports and helper functions

```python
from team_alpha.locators import GoogleSearchLocators

# All locators accessible from one import
```

---

### `team_alpha/pages/`

#### `google_search_page.py`
**Purpose**: Page Object for Google Search

**Structure**:
```python
class GoogleSearchPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Initialize locators
        self.search_input = page.locator(GoogleSearchLocators.SEARCH_INPUT)

    def navigate(self):
        """Navigate to Google homepage"""
        # Implementation

    def search(self, query):
        """Perform a search"""
        # Implementation

    def click_shopping_tab(self):
        """Click Shopping tab"""
        # Implementation
```

**Key Methods**:
- `navigate()` - Go to Google
- `search(query)` - Search for text
- `click_shopping_tab()` - Switch to Shopping
- `verify_search_results_displayed()` - Validation

**Uses**:
- `BasePage` methods
- `GoogleSearchLocators` selectors
- `handle_optional_dialog` utility (cookie consent)

---

#### `google_shopping_page.py`
**Purpose**: Page Object for Google Shopping

**Key Methods**:
- `get_first_product_price()` - Extract first product price
- `get_first_product_details()` - Get title, price, seller
- `verify_shopping_results_displayed()` - Validate page loaded
- `get_product_count()` - Count products on page

**Uses**:
- `extract_price_from_text` - Regex price extraction
- `try_multiple_locators` - Fallback strategies
- `safe_extract_text` - Safe text extraction

---

### `team_alpha/api_clients/`

#### `reqres_api_client.py`
**Purpose**: API client for ReqRes.in API

**Structure**:
```python
class ReqResApiClient(BaseApiClient):
    @allure.step("Get list of users")
    def get_users(self, page: int = 1):
        return self.get(f"/api/users?page={page}")

    @allure.step("Create user")
    def create_user(self, name: str, job: str):
        data = {"name": name, "job": job}
        return self.post("/api/users", data=data)
```

**Implements**:
- `get_users(page)` - GET /api/users
- `create_user(name, job)` - POST /api/users
- `update_user(user_id, data)` - PUT /api/users/{id}
- `delete_user(user_id)` - DELETE /api/users/{id}
- `register_user(email, password)` - POST /api/register
- `login_user(email, password)` - POST /api/login
- `get_resources(page)` - GET /api/unknown

---

### `team_alpha/test_data/`

#### `google_shopping.yaml`
**Purpose**: Test data for shopping tests

**Structure**:
```yaml
products:
  samsung_s24_ultra:
    search_term: "samsung s24 ultra"
    expected_keywords:
      - "Samsung"
      - "S24"
    min_price: 800
    max_price: 1500
    description: "Samsung Galaxy S24 Ultra"

result_counts:
  minimum_results: 3
  maximum_results: 100

config:
  timeout: 30
  retry_attempts: 3
```

---

#### `data_loader.py`
**Purpose**: Team Alpha's data loader implementation

**Extends**: `BaseYamlDataLoader`

**Structure**:
```python
class TeamAlphaDataLoader(BaseYamlDataLoader):
    def __init__(self):
        yaml_file = Path(__file__).parent / "google_shopping.yaml"
        super().__init__(yaml_file)

    def get_product(self, key: str) -> ProductData:
        product = self.get_section_item("products", key)
        return ProductData(**product)
```

**Data Classes**:
- `ProductData` - Product information
- `ResultCountConfig` - Expected result counts
- `TestConfig` - Test configuration

**Convenience Functions**:
```python
from team_alpha.test_data import load_product_data

data = load_product_data("samsung_s24_ultra")
print(data.search_term)  # "samsung s24 ultra"
```

---

### `team_alpha/tests/`

#### `tests/api/test_reqres_api.py`
**Purpose**: API test suite for ReqRes API

**Test Structure**:
```python
@pytest.mark.team_alpha
@pytest.mark.api
@allure.feature("ReqRes API")
class TestReqResUserAPI:
    @pytest.mark.smoke
    def test_get_users_list(self, api_request_context):
        client = ReqResApiClient(api_request_context)
        response = client.get_users(page=2)
        assert response.ok
        body = response.json()
        assert body["page"] == 2
```

**Test Classes**:
1. `TestReqResUserAPI` - User CRUD operations (4 tests)
2. `TestReqResAuthAPI` - Authentication (3 tests)
3. `TestReqResResourceAPI` - Resources (2 tests)

**Total**: 9 API tests

---

#### `tests/web/test_google_shopping.py`
**Purpose**: Web UI test suite for Google Shopping

**Test Structure**:
```python
@pytest.mark.team_alpha
@pytest.mark.ui
@allure.feature("Google Shopping")
class TestGoogleShopping:
    @pytest.mark.smoke
    def test_samsung_s24_ultra_price_check(self, page):
        # Load test data
        product_data = load_product_data("samsung_s24_ultra")

        # Initialize page objects
        search_page = GoogleSearchPage(page)
        shopping_page = GoogleShoppingPage(page)

        # Perform test
        search_page.navigate()
        search_page.search(product_data.search_term)
        search_page.click_shopping_tab()

        # Verify
        price = shopping_page.get_first_product_price()
        assert "$" in price
```

**Test Methods**:
1. `test_samsung_s24_ultra_price_check` - Extract price
2. `test_samsung_s24_ultra_product_details` - Get details
3. `test_multiple_shopping_results` - Count results

**Total**: 3 web tests

---

## 🚀 Running Tests

### Basic Commands

```bash
# Install dependencies
poetry install
poetry run playwright install

# Run all tests
make test-all
poetry run pytest

# Run specific test types
make test-api          # API tests only
make test-web          # Web tests only
make test-smoke        # Smoke tests only

# Run specific team tests
poetry run pytest team_alpha/

# Run with markers
poetry run pytest -m smoke
poetry run pytest -m "api and team_alpha"

# Run in parallel
poetry run pytest -n auto

# Run in headless mode
HEADLESS=true poetry run pytest

# Run with video recording
RECORD_VIDEO=true poetry run pytest
```

### Makefile Commands

```bash
make help              # Show all commands
make install           # Install dependencies
make install-browsers  # Install Playwright browsers
make test-api          # Run API tests
make test-web          # Run web tests
make test-all          # Run all tests
make test-smoke        # Run smoke tests
make allure-report     # Generate report
make allure-serve      # Generate and open report
make clean-videos      # Delete videos
```

### Allure Reports

```bash
# Generate HTML report
make allure-report

# Generate and open in browser
make allure-serve

# View existing report
cd allure-report && python -m http.server 8000
```

### Test Markers

```python
@pytest.mark.smoke         # Critical smoke tests
@pytest.mark.regression    # Full regression suite
@pytest.mark.api           # API tests
@pytest.mark.ui            # UI tests
@pytest.mark.team_alpha    # Team Alpha tests
```

---

## 🆕 Adding New Teams

### Step 1: Create Team Structure

```bash
# Create directories
mkdir -p team_beta/{locators,pages,api_clients,test_data,tests/{api,web,integration}}

# Create __init__.py files
touch team_beta/__init__.py
touch team_beta/locators/__init__.py
touch team_beta/pages/__init__.py
touch team_beta/api_clients/__init__.py
touch team_beta/test_data/__init__.py
touch team_beta/tests/__init__.py
touch team_beta/tests/api/__init__.py
touch team_beta/tests/web/__init__.py
touch team_beta/tests/integration/__init__.py
```

### Step 2: Create Team Conftest

```python
# team_beta/conftest.py
import pytest
from core.logger import log

@pytest.fixture(scope="function", autouse=True)
def log_test_info(request):
    """Team Beta test logging"""
    test_name = request.node.name
    log.info(f"TEAM BETA TEST: {test_name}")
    yield
    log.info(f"COMPLETED: {test_name}")
```

### Step 3: Create Data Loader

```python
# team_beta/test_data/data_loader.py
from pathlib import Path
from dataclasses import dataclass
from core.data import BaseYamlDataLoader

@dataclass
class MyData:
    field1: str
    field2: int

class TeamBetaDataLoader(BaseYamlDataLoader):
    def __init__(self):
        yaml_file = Path(__file__).parent / "test_data.yaml"
        super().__init__(yaml_file)

    def get_data(self, key: str) -> MyData:
        data = self.get_section_item("data", key)
        return MyData(**data)
```

### Step 4: Create YAML File

```yaml
# team_beta/test_data/test_data.yaml
data:
  item1:
    field1: "value1"
    field2: 100
```

### Step 5: Create Locators

```python
# team_beta/locators/locators.py
class MyPageLocators:
    """Locators for MyPage"""
    BUTTON = 'button#submit'
    INPUT = 'input[name="username"]'
```

### Step 6: Create Page Object

```python
# team_beta/pages/my_page.py
from core.base.page_base import BasePage
from team_beta.locators import MyPageLocators

class MyPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.button = page.locator(MyPageLocators.BUTTON)

    def click_button(self):
        self.button.click()
```

### Step 7: Write Tests

```python
# team_beta/tests/web/test_my_feature.py
import pytest
import allure
from team_beta.pages.my_page import MyPage

@pytest.mark.team_beta
@pytest.mark.ui
class TestMyFeature:
    def test_something(self, page):
        my_page = MyPage(page)
        my_page.click_button()
        assert True
```

### Step 8: Update Configuration

```ini
# pytest.ini - Add marker
[pytest]
markers =
    team_beta: Team Beta tests
```

```makefile
# Makefile - Add command
test-team-beta:  ## Run Team Beta tests
	poetry run pytest team_beta/ -v
```

---

## ✅ Best Practices

### Project Organization

1. **One Team Per Directory**
   - Keep team code isolated
   - Avoid cross-team dependencies
   - Use core framework for shared code

2. **Use Base Classes**
   - Inherit from `BasePage` for pages
   - Inherit from `BaseApiClient` for APIs
   - Inherit from `BaseYamlDataLoader` for data

3. **Centralize Locators**
   - All locators in `locators/locators.py`
   - Group by page/feature
   - Never hardcode locators in tests

4. **Use Test Data Files**
   - YAML for structured data
   - Type-safe with data classes
   - Version controlled

### Test Writing

1. **Follow AAA Pattern**
   ```python
   def test_something():
       # Arrange
       setup_data()

       # Act
       perform_action()

       # Assert
       verify_result()
   ```

2. **Use Descriptive Names**
   ```python
   # Good
   def test_user_can_login_with_valid_credentials()

   # Bad
   def test_login()
   ```

3. **Add Allure Annotations**
   ```python
   @allure.feature("User Management")
   @allure.story("User Login")
   @allure.title("User can login with valid credentials")
   def test_login():
       pass
   ```

4. **Use Markers**
   ```python
   @pytest.mark.smoke
   @pytest.mark.team_alpha
   def test_critical_path():
       pass
   ```

### Code Quality

1. **DRY (Don't Repeat Yourself)**
   - Extract common logic to utilities
   - Use base classes
   - Create helper functions

2. **Single Responsibility**
   - One test tests one thing
   - Page objects represent one page
   - Methods do one thing

3. **Clear Error Messages**
   ```python
   # Good
   assert price >= min_price, f"Price {price} is below minimum {min_price}"

   # Bad
   assert price >= min_price
   ```

4. **Use Type Hints**
   ```python
   def get_user(self, user_id: int) -> User:
       pass
   ```

### Performance

1. **Use Fixtures Wisely**
   - `session` scope for expensive setup
   - `function` scope for isolation
   - `autouse=True` for common setup

2. **Parallel Execution**
   ```bash
   pytest -n auto  # Use all CPU cores
   ```

3. **Skip Slow Tests in Development**
   ```python
   @pytest.mark.slow
   def test_long_running():
       pass

   # Run: pytest -m "not slow"
   ```

### Debugging

1. **Use Logging**
   ```python
   from core.logger import log
   log.info("Starting test")
   log.debug(f"User data: {user}")
   ```

2. **Screenshots on Failure**
   - Automatic in framework
   - Saved to `screenshots/`

3. **Video Recording**
   - Enable with `RECORD_VIDEO=true`
   - Videos in `videos/`

4. **Allure Reports**
   - Step-by-step execution
   - Attachments (logs, screenshots)
   - Test history

---

## 📚 Additional Resources

### Documentation Files
- `team_alpha/test_data/README.md` - Test data usage guide
- `team_alpha/tests/web/README_GOOGLE_SHOPPING.md` - Google Shopping test docs
- `team_beta/README.md` - Team Beta setup guide
- `team_gamma/README.md` - Team Gamma setup guide

### Generated Artifacts
- `logs/` - Test execution logs (Loguru format)
- `screenshots/` - Failure screenshots (PNG)
- `videos/` - Test recordings (WebM)
- `allure-results/` - Raw Allure data (JSON)
- `allure-report/` - HTML test reports

### External Links
- [Playwright Documentation](https://playwright.dev/python/)
- [pytest Documentation](https://docs.pytest.org/)
- [Allure Documentation](https://docs.qameta.io/allure/)
- [Poetry Documentation](https://python-poetry.org/docs/)

---

## 🎓 Quick Reference

### Common Imports
```python
# Core framework
from core.base.page_base import BasePage
from core.base.api_client import BaseApiClient
from core.data import BaseYamlDataLoader
from core.logger import log
from core.config import config

# Core utilities
from core.utils import (
    extract_price_from_text,
    sanitize_text,
    wait_with_retry,
    handle_optional_dialog,
    safe_extract_text,
)

# Playwright
from playwright.sync_api import Page, Locator, APIRequestContext

# pytest & Allure
import pytest
import allure
```

### Directory Shortcuts
```bash
cd core/                    # Framework code
cd team_alpha/              # Team Alpha
cd team_alpha/tests/        # Tests
cd team_alpha/pages/        # Page objects
cd team_alpha/locators/     # Locators
cd team_alpha/test_data/    # Test data
```

---

**End of Project Guide**

For questions or issues, please refer to the inline code documentation or contact the QA team.
