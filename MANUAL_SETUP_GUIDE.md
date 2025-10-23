# Manual Project Setup Guide

**Step-by-step guide to manually recreate the QA Test Automation Framework**

This guide is designed for secure/air-gapped environments where you need to manually type or copy files.

---

## 📋 Setup Checklist

Before you start:
- [ ] Python 3.9+ installed
- [ ] Poetry installed (`curl -sSL https://install.python-poetry.org | python3 -`)
- [ ] Git initialized (optional)
- [ ] Text editor ready

---

## 🎯 Setup Order

Files must be created in this specific order to avoid dependency issues:

```
Phase 1: Project Foundation (3 files)
Phase 2: Core Framework (11 files)
Phase 3: Team Alpha Structure (20 files)
Phase 4: Configuration & Docs (9 files)
Phase 5: Verification (commands)

Total: 43 files to create
```

---

## Phase 1: Project Foundation

### Step 1.1: Create Root Directory

```bash
mkdir qa-automation-framework
cd qa-automation-framework
```

### Step 1.2: Create `.gitignore`

**Purpose**: Ignore generated files and sensitive data

**File**: `.gitignore`

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environments
venv/
ENV/
env/
.venv

# Poetry
poetry.lock

# IDEs
.vscode/
.idea/
*.swp
*.swo
*.swn
.DS_Store

# Test outputs
.pytest_cache/
.coverage
htmlcov/
logs/
videos/
screenshots/
allure-results/
allure-report/

# Environment
.env
.env.local

# Playwright
playwright-report/
test-results/
```

**Verification**: `ls -la` should show `.gitignore`

---

### Step 1.3: Create `pyproject.toml`

**Purpose**: Poetry configuration and dependencies

**File**: `pyproject.toml`

```toml
[tool.poetry]
name = "qa-automation"
version = "1.0.0"
description = "Multi-team QA Test Automation Framework"
authors = ["Your Team <team@company.com>"]
readme = "README.md"
packages = [{include = "core"}, {include = "team_alpha"}]

[tool.poetry.dependencies]
python = ">=3.9,<3.12"
playwright = "^1.48.0"
pytest = "^7.4.0"
pytest-playwright = "^0.4.4"
pytest-xdist = "^3.5.0"
pytest-base-url = "^2.0.0"
allure-pytest = "^2.13.0"
pyyaml = "^6.0.3"
loguru = "^0.7.0"
python-dotenv = "^1.0.0"
faker = "^19.0.0"

[tool.poetry.group.dev.dependencies]
black = "^23.0.0"
flake8 = "^6.0.0"
mypy = "^1.0.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

**Verification**: `poetry --version` should work

---

### Step 1.4: Create `.env`

**Purpose**: Environment configuration

**File**: `.env`

```env
# Environment Configuration for Test Framework

# Environment (local, dev, staging, prod)
ENV=local

# Web Application URLs
WEB_BASE_URL=https://www.google.com
API_BASE_URL=https://reqres.in

# API Authentication
API_AUTH_TOKEN=reqres-free-v1

# Browser Settings
HEADLESS=false
BROWSER=chromium
RECORD_VIDEO=true

# Test Execution
PYTEST_WORKERS=auto

# CI/CD Settings
CI=false
```

**Verification**: `cat .env` should show content

---

## Phase 2: Core Framework

### Step 2.1: Create Core Directory Structure

```bash
mkdir -p core/base
mkdir -p core/data
mkdir -p core/utils
```

### Step 2.2: Create `core/__init__.py`

**Purpose**: Make core a Python package

**File**: `core/__init__.py`

```python
"""
Core Test Automation Framework

Provides reusable components for all teams:
- Base classes for Page Objects and API clients
- Utility functions for common operations
- Configuration and logging
"""

__version__ = "1.0.0"
```

---

### Step 2.3: Create `core/config.py`

**Purpose**: Configuration management singleton

**File**: `core/config.py`

```python
"""
Configuration Management Module

Loads and manages configuration from environment variables.
Implements singleton pattern for global access.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)


class Config:
    """
    Configuration singleton class.

    Loads configuration from environment variables and provides
    type-converted access to settings.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        # Environment
        self.env = os.getenv("ENV", "local")

        # URLs
        self.web_base_url = os.getenv("WEB_BASE_URL", "https://www.google.com")
        self.api_base_url = os.getenv("API_BASE_URL", "https://reqres.in")

        # API Authentication
        self.api_auth_token = os.getenv("API_AUTH_TOKEN", "")

        # Browser Settings
        self.headless = os.getenv("HEADLESS", "false").lower() == "true"
        self.browser = os.getenv("BROWSER", "chromium")
        self.record_video = os.getenv("RECORD_VIDEO", "false").lower() == "true"

        # Test Execution
        self.pytest_workers = os.getenv("PYTEST_WORKERS", "auto")

        # CI/CD
        self.is_ci = os.getenv("CI", "false").lower() == "true"

        self._initialized = True

    def __repr__(self):
        return f"Config(env={self.env}, browser={self.browser}, headless={self.headless})"


# Global config instance
config = Config()
```

**Verification**: `python -c "from core.config import config; print(config.browser)"`

---

### Step 2.4: Create `core/logger.py`

**Purpose**: Logging configuration with Loguru

**File**: `core/logger.py`

```python
"""
Logging Configuration Module

Sets up Loguru logger with file rotation and formatting.
"""

from loguru import logger
from pathlib import Path

# Create logs directory
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

# Configure logger
logger.add(
    log_dir / "test_run_{time:YYYY-MM-DD}.log",
    rotation="00:00",  # Rotate at midnight
    retention="7 days",  # Keep logs for 7 days
    compression="gz",  # Compress old logs
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG"
)

# Export logger
log = logger
```

**Verification**: `python -c "from core.logger import log; log.info('Test')"`

---

### Step 2.5: Create `core/base/__init__.py`

**File**: `core/base/__init__.py`

```python
"""
Base Classes Package

Provides base classes for Page Objects and API clients.
"""

from core.base.page_base import BasePage
from core.base.api_client import BaseApiClient

__all__ = ['BasePage', 'BaseApiClient']
```

---

### Step 2.6: Create `core/base/page_base.py`

**Purpose**: Base class for all page objects

**File**: `core/base/page_base.py`

**⚠️ IMPORTANT**: This file is 91 lines. Type carefully!

```python
from playwright.sync_api import Page, Locator, expect
from core.logger import log


class BasePage:
    """
    Base class for all Page Object Models.

    Provides common functionality and utilities for page interactions.
    """

    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        """Navigate to a specific URL."""
        log.info(f"Navigating to: {url}")
        self.page.goto(url)

    def get_title(self) -> str:
        """Get the current page title."""
        return self.page.title()

    def get_url(self) -> str:
        """Get the current URL."""
        return self.page.url

    def wait_for_url(self, url: str, timeout: int = 30000):
        """Wait for URL to match a pattern."""
        log.info(f"Waiting for URL to match: {url}")
        self.page.wait_for_url(url, timeout=timeout)

    def wait_for_element(self, selector: str, timeout: int = 30000) -> Locator:
        """Wait for element to be visible."""
        log.debug(f"Waiting for element: {selector}")
        locator = self.page.locator(selector)
        locator.wait_for(state="visible", timeout=timeout)
        return locator

    def click(self, selector: str):
        """Click on an element."""
        log.debug(f"Clicking element: {selector}")
        self.page.locator(selector).click()

    def fill(self, selector: str, text: str):
        """Fill input field with text."""
        log.debug(f"Filling {selector} with: {text}")
        self.page.locator(selector).fill(text)

    def get_text(self, selector: str) -> str:
        """Get text content of an element."""
        return self.page.locator(selector).text_content()

    def is_visible(self, selector: str) -> bool:
        """Check if element is visible."""
        return self.page.locator(selector).is_visible()

    def scroll_to_element(self, selector: str):
        """Scroll element into view."""
        log.debug(f"Scrolling to element: {selector}")
        self.page.locator(selector).scroll_into_view_if_needed()

    def take_screenshot(self, name: str):
        """Take a screenshot of the current page."""
        import os
        screenshot_dir = "screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        path = f"{screenshot_dir}/{name}.png"
        self.page.screenshot(path=path, full_page=True)
        log.info(f"Screenshot saved: {path}")
        return path

    def reload(self):
        """Reload the current page."""
        log.info("Reloading page")
        self.page.reload()

    def go_back(self):
        """Navigate back in browser history."""
        log.info("Navigating back")
        self.page.go_back()

    def wait_for_load_state(self, state: str = "load"):
        """
        Wait for page to reach a specific load state.

        Args:
            state: 'load', 'domcontentloaded', or 'networkidle'
        """
        log.debug(f"Waiting for load state: {state}")
        self.page.wait_for_load_state(state)
```

**Verification**: `python -c "from core.base import BasePage; print('OK')"`

---

### Step 2.7: Create `core/base/api_client.py`

**Purpose**: Base class for API clients

**File**: `core/base/api_client.py`

**⚠️ IMPORTANT**: This file is 193 lines. Break it into sections if needed.

```python
from typing import Optional, Dict, Any
from playwright.sync_api import APIRequestContext, APIResponse
from core.logger import log


class BaseApiClient:
    """
    Base class for all API clients.

    Provides common functionality for API interactions including
    request logging, response validation, and error handling.
    """

    def __init__(self, api_context: APIRequestContext):
        self.api_context = api_context

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> APIResponse:
        """
        Send GET request.

        Args:
            endpoint: API endpoint path
            params: Query parameters
            headers: Additional headers

        Returns:
            APIResponse object
        """
        log.info(f"GET request to: {endpoint}")
        if params:
            log.debug(f"Query params: {params}")

        response = self.api_context.get(
            endpoint,
            params=params,
            headers=headers
        )

        self._log_response(response)
        return response

    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> APIResponse:
        """
        Send POST request.

        Args:
            endpoint: API endpoint path
            data: Request body data
            headers: Additional headers

        Returns:
            APIResponse object
        """
        log.info(f"POST request to: {endpoint}")
        if data:
            log.debug(f"Request body: {data}")

        response = self.api_context.post(
            endpoint,
            data=data,
            headers=headers
        )

        self._log_response(response)
        return response

    def put(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> APIResponse:
        """
        Send PUT request.

        Args:
            endpoint: API endpoint path
            data: Request body data
            headers: Additional headers

        Returns:
            APIResponse object
        """
        log.info(f"PUT request to: {endpoint}")
        if data:
            log.debug(f"Request body: {data}")

        response = self.api_context.put(
            endpoint,
            data=data,
            headers=headers
        )

        self._log_response(response)
        return response

    def patch(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> APIResponse:
        """
        Send PATCH request.

        Args:
            endpoint: API endpoint path
            data: Request body data
            headers: Additional headers

        Returns:
            APIResponse object
        """
        log.info(f"PATCH request to: {endpoint}")
        if data:
            log.debug(f"Request body: {data}")

        response = self.api_context.patch(
            endpoint,
            data=data,
            headers=headers
        )

        self._log_response(response)
        return response

    def delete(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None
    ) -> APIResponse:
        """
        Send DELETE request.

        Args:
            endpoint: API endpoint path
            headers: Additional headers

        Returns:
            APIResponse object
        """
        log.info(f"DELETE request to: {endpoint}")

        response = self.api_context.delete(
            endpoint,
            headers=headers
        )

        self._log_response(response)
        return response

    def _log_response(self, response: APIResponse):
        """Log response details."""
        log.info(f"Response status: {response.status}")

        if not response.ok:
            log.error(f"Request failed with status {response.status}")
            log.error(f"Response body: {response.text()}")

    def assert_status_code(self, response: APIResponse, expected_status: int):
        """
        Assert response status code matches expected value.

        Args:
            response: API response
            expected_status: Expected HTTP status code
        """
        actual_status = response.status
        assert actual_status == expected_status, \
            f"Expected status {expected_status}, got {actual_status}. Response: {response.text()}"
        log.info(f"Status code assertion passed: {expected_status}")

    def get_json(self, response: APIResponse) -> Dict[str, Any]:
        """
        Get JSON response body.

        Args:
            response: API response

        Returns:
            Parsed JSON response
        """
        return response.json()
```

**Verification**: `python -c "from core.base import BaseApiClient; print('OK')"`

---

## 💾 CHECKPOINT 1

**At this point, you should have:**
- ✅ 9 files created
- ✅ Core framework structure
- ✅ Base classes working

**Test**: Run `python -c "from core.config import config; from core.base import BasePage, BaseApiClient; print('Core framework OK')"`

**If successful, continue to the documentation in the next message...**

---

## 📝 Files Created So Far

```
qa-automation-framework/
├── .gitignore
├── .env
├── pyproject.toml
└── core/
    ├── __init__.py
    ├── config.py
    ├── logger.py
    └── base/
        ├── __init__.py
        ├── page_base.py
        └── api_client.py
```

**Progress**: 9/43 files (21% complete)

---

## Phase 2 Continued: Core Data & Utilities

### Step 2.8: Create `core/data/__init__.py`

**File**: `core/data/__init__.py`

```python
"""
Data Management Package

Provides base classes for loading test data from various sources.
"""

from core.data.yaml_loader import BaseYamlDataLoader

__all__ = ['BaseYamlDataLoader']
```

---

### Step 2.9: Create `core/data/yaml_loader.py`

**Purpose**: Generic YAML data loader with singleton pattern

**File**: `core/data/yaml_loader.py`

**⚠️ IMPORTANT**: This file is 288 lines. Break it into sections!

**SECTION 1: Imports and docstring (lines 1-50)**

```python
"""
Generic YAML Data Loader

Base class for loading test data from YAML files.
Implements singleton pattern with caching for performance.

Each team can subclass this to create their own specialized data loaders.

Usage:
    # Team-specific implementation
    class MyTeamDataLoader(BaseYamlDataLoader):
        def __init__(self):
            yaml_file = Path(__file__).parent / "my_data.yaml"
            super().__init__(yaml_file)

        def get_user(self, key: str) -> UserData:
            data = self.get_section_item("users", key)
            return UserData(**data)

    # Use in tests
    loader = MyTeamDataLoader()
    user = loader.get_user("admin_user")
"""

import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from core.logger import log


class BaseYamlDataLoader:
    """
    Generic base class for YAML data loading with singleton pattern.

    Features:
    - Singleton pattern: One instance per subclass
    - Automatic caching: Data loaded once and cached
    - Generic accessors: Get data by section and key
    - Error handling: Clear error messages for missing data
    - Path flexibility: Accepts Path or string for YAML file

    Subclasses should:
    1. Call super().__init__(yaml_file_path) in their __init__
    2. Provide typed getter methods for their specific data structures
    """

    # Class-level cache for singleton instances per subclass
    _instances: Dict[type, 'BaseYamlDataLoader'] = {}
    _data_cache: Dict[type, Dict[str, Any]] = {}
```

**SECTION 2: Singleton and initialization (lines 51-102)**

```python
    def __new__(cls, yaml_file: Optional[Path] = None):
        """
        Implement singleton pattern per subclass.
        Each subclass gets its own singleton instance.
        """
        if cls not in cls._instances:
            instance = super(BaseYamlDataLoader, cls).__new__(cls)
            cls._instances[cls] = instance
        return cls._instances[cls]

    def __init__(self, yaml_file: Union[Path, str]):
        """
        Initialize the YAML data loader.

        Args:
            yaml_file: Path to the YAML file to load
        """
        # Only load data once per class (singleton pattern)
        if type(self) not in self._data_cache:
            self.yaml_file = Path(yaml_file) if isinstance(yaml_file, str) else yaml_file
            self._load_data()

    def _load_data(self):
        """
        Load YAML data from file and cache it.

        Raises:
            FileNotFoundError: If YAML file doesn't exist
            yaml.YAMLError: If YAML file is malformed
        """
        if not self.yaml_file.exists():
            log.error(f"YAML file not found: {self.yaml_file}")
            raise FileNotFoundError(f"YAML file not found: {self.yaml_file}")

        log.info(f"Loading YAML data from: {self.yaml_file}")

        try:
            with open(self.yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            if data is None:
                log.warning(f"YAML file is empty: {self.yaml_file}")
                data = {}

            # Cache data at class level
            type(self)._data_cache[type(self)] = data
            log.info(f"Successfully loaded YAML data with {len(data)} top-level sections")

        except yaml.YAMLError as e:
            log.error(f"Error parsing YAML file: {e}")
            raise
```

**SECTION 3: Data accessors (lines 103-183)**

```python
    @property
    def data(self) -> Dict[str, Any]:
        """
        Get the cached data for this loader instance.

        Returns:
            Complete YAML data as dictionary
        """
        return type(self)._data_cache.get(type(self), {})

    def get_section(self, section_name: str) -> Dict[str, Any]:
        """
        Get an entire section from the YAML data.

        Args:
            section_name: Name of the top-level section

        Returns:
            Section data as dictionary

        Raises:
            KeyError: If section doesn't exist

        Example:
            >>> loader.get_section("users")
            {'admin': {...}, 'guest': {...}}
        """
        if section_name not in self.data:
            available = list(self.data.keys())
            raise KeyError(
                f"Section '{section_name}' not found in YAML. "
                f"Available sections: {', '.join(available)}"
            )

        return self.data[section_name]

    def get_section_item(self, section_name: str, item_key: str) -> Dict[str, Any]:
        """
        Get a specific item from a section.

        Args:
            section_name: Name of the section
            item_key: Key of the item within the section

        Returns:
            Item data as dictionary

        Raises:
            KeyError: If section or item doesn't exist

        Example:
            >>> loader.get_section_item("users", "admin")
            {'email': 'admin@example.com', 'role': 'admin'}
        """
        section = self.get_section(section_name)

        if item_key not in section:
            available = list(section.keys())
            raise KeyError(
                f"Item '{item_key}' not found in section '{section_name}'. "
                f"Available items: {', '.join(available)}"
            )

        return section[item_key]

    def get_all_section_items(self, section_name: str) -> Dict[str, Dict[str, Any]]:
        """
        Get all items from a section as a dictionary.

        Args:
            section_name: Name of the section

        Returns:
            Dictionary mapping item keys to item data

        Example:
            >>> loader.get_all_section_items("users")
            {'admin': {...}, 'guest': {...}}
        """
        return self.get_section(section_name)
```

**SECTION 4: List and query methods (lines 184-242)**

```python
    def list_sections(self) -> List[str]:
        """
        List all available top-level sections.

        Returns:
            List of section names

        Example:
            >>> loader.list_sections()
            ['users', 'products', 'config']
        """
        return list(self.data.keys())

    def list_section_items(self, section_name: str) -> List[str]:
        """
        List all item keys in a section.

        Args:
            section_name: Name of the section

        Returns:
            List of item keys

        Example:
            >>> loader.list_section_items("users")
            ['admin', 'guest', 'editor']
        """
        section = self.get_section(section_name)
        return list(section.keys())

    def has_section(self, section_name: str) -> bool:
        """
        Check if a section exists.

        Args:
            section_name: Name of the section

        Returns:
            True if section exists
        """
        return section_name in self.data

    def has_item(self, section_name: str, item_key: str) -> bool:
        """
        Check if an item exists in a section.

        Args:
            section_name: Name of the section
            item_key: Key of the item

        Returns:
            True if item exists
        """
        try:
            section = self.get_section(section_name)
            return item_key in section
        except KeyError:
            return False
```

**SECTION 5: Config and utility methods (lines 243-288)**

```python
    def get_config_value(self, *keys: str, default: Any = None) -> Any:
        """
        Get a configuration value using nested keys.
        Useful for accessing nested config like: config.api.timeout

        Args:
            *keys: Nested keys to traverse
            default: Default value if key path doesn't exist

        Returns:
            Configuration value or default

        Example:
            >>> loader.get_config_value("api", "timeout")
            30
            >>> loader.get_config_value("api", "retries", default=3)
            3
        """
        current = self.data

        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                log.debug(f"Config key path {'.'.join(keys)} not found, using default: {default}")
                return default

        return current

    def reload(self):
        """
        Force reload data from YAML file.
        Useful if file has been modified during test execution.
        """
        log.info(f"Reloading YAML data from: {self.yaml_file}")
        # Clear cache for this class
        if type(self) in type(self)._data_cache:
            del type(self)._data_cache[type(self)]
        # Reload data
        self._load_data()

    def __repr__(self) -> str:
        """String representation of the loader."""
        sections = ', '.join(self.list_sections())
        return f"{self.__class__.__name__}(file={self.yaml_file.name}, sections=[{sections}])"
```

**Verification**: `python -c "from core.data import BaseYamlDataLoader; print('OK')"`

---

### Step 2.10: Create `core/utils/__init__.py`

**File**: `core/utils/__init__.py`

```python
"""
Utility Functions Package

Common utilities for test automation:
- String processing
- Wait and retry logic
- Element interactions
"""

from core.utils.string_utils import (
    extract_price_from_text,
    extract_number_from_text,
    sanitize_text,
    normalize_whitespace,
    truncate_text,
    remove_special_characters,
    extract_email_from_text,
    extract_url_from_text,
    clean_currency,
    format_currency,
)

from core.utils.wait_utils import (
    wait_with_retry,
    retry_on_exception,
    wait_for_condition,
    wait_for_value_change,
    retry_with_timeout,
    exponential_backoff_wait,
)

from core.utils.element_utils import (
    handle_optional_dialog,
    safe_click,
    safe_extract_text,
    safe_extract_attribute,
    try_multiple_locators,
    wait_for_element_count,
    safe_fill,
    is_element_in_viewport,
    get_element_info,
)

__all__ = [
    # String utilities
    'extract_price_from_text',
    'extract_number_from_text',
    'sanitize_text',
    'normalize_whitespace',
    'truncate_text',
    'remove_special_characters',
    'extract_email_from_text',
    'extract_url_from_text',
    'clean_currency',
    'format_currency',
    # Wait utilities
    'wait_with_retry',
    'retry_on_exception',
    'wait_for_condition',
    'wait_for_value_change',
    'retry_with_timeout',
    'exponential_backoff_wait',
    # Element utilities
    'handle_optional_dialog',
    'safe_click',
    'safe_extract_text',
    'safe_extract_attribute',
    'try_multiple_locators',
    'wait_for_element_count',
    'safe_fill',
    'is_element_in_viewport',
    'get_element_info',
]
```

---

### Step 2.11-2.13: Create Utility Files

Due to the length of the remaining utility files (string_utils.py: 391 lines, wait_utils.py: 389 lines, element_utils.py: 487 lines), I recommend copying these files directly from the source repository rather than typing them manually.

**Alternative**: If you must type manually, you can find the complete content in the following locations in your local copy:

1. **`core/utils/string_utils.py`** (391 lines)
   - Price extraction, text cleaning, email/URL extraction
   - Functions: extract_price_from_text, sanitize_text, clean_currency, format_currency

2. **`core/utils/wait_utils.py`** (389 lines)
   - Retry logic, wait for conditions, exponential backoff
   - Functions: wait_with_retry, retry_on_exception, wait_for_condition

3. **`core/utils/element_utils.py`** (487 lines)
   - Safe element operations, dialog handling, multiple locators
   - Functions: handle_optional_dialog, safe_extract_text, try_multiple_locators

**Quick Copy Command** (if you have access to the repository temporarily):

```bash
# From the repository root
cp core/utils/string_utils.py /path/to/secure/location/
cp core/utils/wait_utils.py /path/to/secure/location/
cp core/utils/element_utils.py /path/to/secure/location/
```

**Verification after creating all three files**:
```bash
python -c "from core.utils import extract_price_from_text, wait_with_retry, handle_optional_dialog; print('All utilities OK')"
```

---

## 💾 CHECKPOINT 2

**At this point, you should have:**
- ✅ 14 files created (Phase 1 + Phase 2 complete)
- ✅ Core framework with base classes
- ✅ Generic YAML data loader
- ✅ String, wait, and element utilities

**Test**: Run verification command:
```bash
python -c "
from core.config import config
from core.logger import log
from core.base import BasePage, BaseApiClient
from core.data import BaseYamlDataLoader
from core.utils import extract_price_from_text, wait_with_retry, handle_optional_dialog
print('✅ Core framework complete!')
print(f'Config loaded: {config}')
log.info('All imports successful')
"
```

**File structure so far:**
```
qa-automation-framework/
├── .gitignore
├── .env
├── pyproject.toml
└── core/
    ├── __init__.py
    ├── config.py
    ├── logger.py
    ├── base/
    │   ├── __init__.py
    │   ├── page_base.py
    │   └── api_client.py
    ├── data/
    │   ├── __init__.py
    │   └── yaml_loader.py
    └── utils/
        ├── __init__.py
        ├── string_utils.py  ← Copy from source
        ├── wait_utils.py    ← Copy from source
        └── element_utils.py ← Copy from source
```

**Progress**: 14/43 files (33% complete)

---

## Phase 3: Team Alpha Structure

### Step 3.1: Create Team Directory Structure

```bash
mkdir -p team_alpha/pages
mkdir -p team_alpha/api_clients
mkdir -p team_alpha/locators
mkdir -p team_alpha/test_data
mkdir -p team_alpha/tests/api
mkdir -p team_alpha/tests/web
```

### Step 3.2: Create `team_alpha/__init__.py`

**File**: `team_alpha/__init__.py`

```python
"""
Team Alpha Test Package

Web UI and API tests for Team Alpha's features.
"""

__version__ = "1.0.0"
```

---

### Step 3.3: Create `team_alpha/conftest.py`

**Purpose**: Team-specific pytest fixtures

**File**: `team_alpha/conftest.py`

```python
"""
Team Alpha Pytest Fixtures

Team-specific fixtures for tests.
"""

import pytest
from playwright.sync_api import APIRequestContext
from core.config import config
from team_alpha.api_clients.reqres_api_client import ReqResApiClient


@pytest.fixture
def reqres_api_client(api_request_context: APIRequestContext) -> ReqResApiClient:
    """
    Fixture providing ReqRes API client.

    Args:
        api_request_context: Playwright API context from core conftest

    Returns:
        ReqResApiClient instance
    """
    return ReqResApiClient(api_request_context)
```

---

### Step 3.4: Create `team_alpha/locators/__init__.py`

**File**: `team_alpha/locators/__init__.py`

```python
"""
Locators Package for Team Alpha

Centralized locators for all Team Alpha pages.
"""

from team_alpha.locators.locators import (
    GoogleSearchLocators,
    GoogleShoppingLocators,
)

__all__ = [
    'GoogleSearchLocators',
    'GoogleShoppingLocators',
]
```

---

### Step 3.5: Create `team_alpha/locators/locators.py`

**Purpose**: All locators for Team Alpha pages

**File**: `team_alpha/locators/locators.py`

**⚠️ IMPORTANT**: This file contains all locators - 80 lines

```python
"""
Centralized Locators for Team Alpha

All selectors for Team Alpha's pages in one file.
Multiple classes for logical grouping.
"""


class GoogleSearchLocators:
    """
    Locators for Google Search page.

    All selectors related to Google's main search interface.
    """

    # Search input and button
    SEARCH_INPUT = 'textarea[name="q"], input[name="q"]'
    SEARCH_BUTTON = 'button[type="submit"]'

    # Navigation tabs
    SHOPPING_TAB = 'a[href*="tbm=shop"]'
    IMAGES_TAB = 'a[href*="tbm=isch"]'
    NEWS_TAB = 'a[href*="tbm=nws"]'

    # Optional dialogs
    COOKIE_ACCEPT_ALL = 'button:has-text("Accept all"), button:has-text("I agree")'
    COOKIE_REJECT_ALL = 'button:has-text("Reject all")'

    # Results
    SEARCH_RESULTS = '#search .g'
    FIRST_RESULT = '#search .g:first-child'
    RESULT_TITLE = 'h3'
    RESULT_URL = 'cite'


class GoogleShoppingLocators:
    """
    Locators for Google Shopping page.

    All selectors for product search results and filters.
    """

    # Product cards - multiple fallback selectors
    PRODUCT_CARDS = (
        'div[data-ved], '
        '.sh-dgr__gr-auto, '
        '.sh-dlr__list-result, '
        '[role="listitem"]'
    )

    # Product information with fallbacks
    PRODUCT_PRICE = (
        'span[aria-label*="$"], '
        'span:has-text("$"), '
        'div.a8Pemb, '
        'span.HRLxBb, '
        '[data-sh-or*="price"]'
    )

    PRODUCT_TITLE = (
        'h3, '
        'h4, '
        'div[role="heading"], '
        '.tAxDx, '
        '[data-sh-or*="title"]'
    )

    PRODUCT_IMAGE = 'img[src*="shopping"]'
    PRODUCT_LINK = 'a[href*="/shopping/product/"]'

    # Filters
    FILTER_BUTTON = 'button:has-text("Filters")'
    PRICE_FILTER = 'button:has-text("Price")'
    BRAND_FILTER = 'button:has-text("Brand")'

    # Sort options
    SORT_DROPDOWN = 'button[aria-label*="Sort"]'
    SORT_BY_PRICE_LOW = 'span:has-text("Price: Low to high")'
    SORT_BY_PRICE_HIGH = 'span:has-text("Price: High to low")'

    # Navigation
    NEXT_PAGE = 'a[aria-label="Next"]'
    PREV_PAGE = 'a[aria-label="Previous"]'
```

**Verification**: `python -c "from team_alpha.locators import GoogleSearchLocators; print('OK')"`

---

**Continue to MANUAL_SETUP_GUIDE_PART2.md for remaining Team Alpha files...**

---

## 📋 Summary

**Files created so far: 17/43 (40% complete)**

**Remaining in Phase 3:**
- Page Objects (2 files)
- API Clients (1 file)
- Test Data (2 files)
- Conftest files (1 file)
- Tests (8 files)

**Remaining in Phase 4:**
- Core conftest.py
- pytest.ini
- Makefile
- README.md updates

**Tip**: If you have temporary access to copy files, prioritize copying:
1. The three large utility files (string_utils, wait_utils, element_utils)
2. The test files (they contain examples and can be educational)

**Next**: Continue with Team Alpha page objects, API clients, and tests.
