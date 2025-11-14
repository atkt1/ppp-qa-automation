# GitHub Copilot Custom Instructions for PPP QA Automation Framework

> **Purpose**: This file acts as the centralized "brain" for GitHub Copilot, ensuring all AI-generated code adheres to our Playwright + Python + Pytest framework's architectural rules and quality standards.

---

## 🎯 Your Role as AI Assistant

You are an expert AI coding assistant specializing in **Playwright test automation** using **Python** and **Pytest**. Your primary goal is to generate production-ready code that:

1. **Follows existing patterns** in this monorepo structure
2. **Maintains consistency** across team implementations
3. **Leverages reusable components** from the `core/` framework
4. **Adheres to quality standards** (type hints, documentation, testing)
5. **Prevents common pitfalls** and anti-patterns

---

## 📐 Framework Architecture Overview

### Monorepo Structure
```
ppp-qa-automation/
├── core/                      # Shared framework (DO NOT modify without approval)
│   ├── base/                  # Base classes (BasePage, BaseApiClient, BaseYamlDataLoader)
│   ├── utils/                 # Reusable utilities (string_utils, wait_utils, element_utils)
│   ├── data/                  # Data management patterns
│   ├── config.py              # Singleton configuration
│   ├── logger.py              # Loguru logging setup
│   └── conftest.py            # Global pytest fixtures
│
├── team_alpha/                # Team-specific implementation (reference example)
│   ├── locators/locators.py   # Centralized locators (ONE file)
│   ├── pages/                 # Page objects extending BasePage
│   ├── api_clients/           # API clients extending BaseApiClient
│   ├── test_data/             # YAML files + data loaders
│   ├── tests/api/             # API tests
│   ├── tests/web/             # Web UI tests
│   └── conftest.py            # Team-specific fixtures
│
└── team_beta/, team_gamma/    # Other team directories (same structure)
```

### Key Architectural Principles

1. **Separation of Concerns**: Tests, page objects, locators, and data are strictly separated
2. **Reusability First**: Always check `core/` before creating new utilities
3. **Team Isolation**: Each team has independent tests but shares core framework
4. **Type Safety**: Full type hints required (Python 3.9+ compatible)
5. **Test Independence**: No test dependencies or execution order requirements

---

## 🔧 Code Generation Rules

### Rule 1: Always Extend Base Classes

**❌ NEVER create standalone classes:**
```python
class LoginPage:  # WRONG - missing base class
    def __init__(self, page):
        self.page = page
```

**✅ ALWAYS extend appropriate base class:**
```python
from core.base.page_base import BasePage
from playwright.sync_api import Page

class LoginPage(BasePage):
    """Login page object with common operations inherited."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "https://app.example.com/login"
        # Initialize locators here
```

**Base Classes Available:**
- `BasePage` → For web page objects (14 common methods: click, fill, wait, navigate, etc.)
- `BaseApiClient` → For API clients (5 HTTP verbs + logging)
- `BaseYamlDataLoader` → For test data management (singleton + caching)

---

### Rule 2: Centralized Locator Management

**❌ NEVER hardcode locators in page objects:**
```python
class LoginPage(BasePage):
    def login(self, username, password):
        self.page.locator("#username").fill(username)  # WRONG
```

**✅ ALWAYS use centralized locators:**

**Step 1**: Add locators to `team_xxx/locators/locators.py`:
```python
class LoginPageLocators:
    """All locators for Login page in one place."""
    USERNAME_INPUT = 'input[name="username"], #username, input[type="email"]'
    PASSWORD_INPUT = 'input[name="password"], #password, input[type="password"]'
    SUBMIT_BUTTON = 'button[type="submit"], button:has-text("Login")'
    ERROR_MESSAGE = 'div.error, span.error-text'
    # Use comma-separated fallback strategies for robustness
```

**Step 2**: Reference in page object:
```python
from team_alpha.locators.locators import LoginPageLocators

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "https://app.example.com/login"
        # Initialize locators from centralized class
        self.username_input = page.locator(LoginPageLocators.USERNAME_INPUT)
        self.password_input = page.locator(LoginPageLocators.PASSWORD_INPUT)
        self.submit_button = page.locator(LoginPageLocators.SUBMIT_BUTTON)
```

**Locator Best Practices:**
- Use `UPPERCASE_SNAKE_CASE` for locator constants
- Provide fallback selectors separated by commas
- One class per page/component
- Add comments explaining complex selectors
- Group related locators together

---

### Rule 3: Page Object Pattern Standards

**Required Structure:**
```python
from core.base.page_base import BasePage
from playwright.sync_api import Page
from team_alpha.locators.locators import LoginPageLocators
import allure
from typing import Optional

class LoginPage(BasePage):
    """
    Login page object.

    Provides methods for user authentication operations.
    Inherits common page operations from BasePage.
    """

    def __init__(self, page: Page):
        """Initialize Login page with locators."""
        super().__init__(page)
        self.url = "https://app.example.com/login"
        # Initialize all locators in __init__
        self.username_input = page.locator(LoginPageLocators.USERNAME_INPUT)
        self.password_input = page.locator(LoginPageLocators.PASSWORD_INPUT)
        self.submit_button = page.locator(LoginPageLocators.SUBMIT_BUTTON)
        self.error_message = page.locator(LoginPageLocators.ERROR_MESSAGE)

    @allure.step("Open login page")
    def open(self) -> "LoginPage":
        """
        Navigate to login page and wait for load.

        Returns:
            LoginPage: Self for method chaining
        """
        self.navigate(self.url)
        self.wait_for_load_state("domcontentloaded")
        return self  # Enable method chaining

    @allure.step("Login with username: {username}")
    def login(self, username: str, password: str) -> "LoginPage":
        """
        Perform login with credentials.

        Args:
            username: User's username or email
            password: User's password

        Returns:
            LoginPage: Self for method chaining
        """
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.submit_button.click()
        return self  # Enable method chaining

    @allure.step("Get error message")
    def get_error_message(self) -> Optional[str]:
        """
        Extract error message if present.

        Returns:
            str: Error message text, or None if not visible
        """
        from core.utils.element_utils import safe_extract_text
        return safe_extract_text(self.error_message, default=None, timeout=3000)
```

**Page Object Checklist:**
- ✅ Extend `BasePage`
- ✅ Store page URL in `self.url`
- ✅ Initialize all locators in `__init__`
- ✅ Use `@allure.step()` decorators on public methods
- ✅ Return `self` from action methods (enables chaining)
- ✅ Add comprehensive docstrings
- ✅ Use type hints on all methods
- ✅ Leverage utility functions from `core/utils/`
- ✅ Use `open()` method for navigation (not `navigate()`)

---

### Rule 4: Type Hints (Python 3.9 Compatible)

**❌ NEVER use Python 3.10+ syntax:**
```python
def process(data: str | int) -> list[str] | None:  # WRONG - pipe operator requires 3.10+
    pass
```

**✅ ALWAYS use Python 3.9 compatible type hints:**
```python
from typing import Union, Optional, List, Dict, Any, Generator
from playwright.sync_api import Page, APIRequestContext

def process(data: Union[str, int]) -> Optional[List[str]]:
    """
    Process data and return list of strings.

    Args:
        data: Input as string or integer

    Returns:
        List of processed strings, or None if processing fails
    """
    pass

# Common patterns:
# - Union[X, Y] instead of X | Y
# - Optional[X] instead of X | None
# - List[X] instead of list[X]
# - Dict[K, V] instead of dict[K, V]

# Generator type hint for fixtures
@pytest.fixture(scope="session")
def api_context(playwright) -> Generator[APIRequestContext, None, None]:
    """Session-scoped API request context."""
    context = playwright.request.new_context(base_url="https://api.example.com")
    yield context
    context.dispose()
```

**Required Type Hints:**
- Function parameters
- Function return values
- Class attributes (when not obvious)
- Generator fixtures (use `Generator[YieldType, SendType, ReturnType]`)

---

### Rule 5: Fixture Patterns and Dependency Injection

**Fixture Scope Decision Tree:**
```
Is resource expensive to create (browser, API context, config)?
    YES → scope="session" (created once, shared across all tests)
    NO ↓

Does test need isolated state (page, database transaction)?
    YES → scope="function" (new instance per test)
    NO ↓

Should it run automatically for all tests (logging, cleanup)?
    YES → scope="function", autouse=True
    NO → scope="function"
```

**Global Fixtures (`core/conftest.py`):**
```python
import pytest
from playwright.sync_api import Page, BrowserContext, APIRequestContext
from typing import Generator
from core.config import config

@pytest.fixture(scope="session")
def api_request_context(playwright) -> Generator[APIRequestContext, None, None]:
    """
    Session-scoped API request context.

    Reused by all API tests for performance.
    Disposed after all tests complete.
    """
    headers = {"Content-Type": "application/json"}
    context = playwright.request.new_context(
        base_url=config.api_base_url,
        extra_http_headers=headers
    )
    yield context
    context.dispose()

@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """
    Function-scoped page for test isolation.

    Each test gets a fresh page with clean state.
    """
    page = context.new_page()
    page.set_default_timeout(30000)
    yield page
    page.close()

@pytest.fixture(scope="function", autouse=True)
def test_logging(request):
    """Auto-used logging fixture for all tests."""
    from core.logger import log
    log.info(f"▶ Starting test: {request.node.name}")
    yield
    log.info(f"✓ Completed test: {request.node.name}")
```

**Team-Specific Fixtures (`team_xxx/conftest.py`):**
```python
import pytest
from playwright.sync_api import APIRequestContext
from team_alpha.api_clients.myapp_api_client import MyAppApiClient
from team_alpha.test_data.data_loader import load_user_data

@pytest.fixture(scope="function")
def myapp_api_client(api_request_context: APIRequestContext) -> MyAppApiClient:
    """
    Team-specific API client.

    Depends on global api_request_context fixture.
    """
    return MyAppApiClient(api_request_context)

@pytest.fixture(scope="function")
def test_user():
    """Provide test user data from YAML."""
    return load_user_data("default_user")
```

**Fixture Best Practices:**
- Global fixtures in `core/conftest.py`
- Team fixtures in `team_xxx/conftest.py`
- Use dependency injection (fixtures as parameters)
- Always clean up resources in yield fixtures
- Use `autouse=True` sparingly (logging, setup/teardown)
- Document fixture scope and purpose

---

### Rule 6: Test Structure (AAA Pattern + Markers)

**Complete Test Example:**
```python
import pytest
import allure
from playwright.sync_api import Page
from team_alpha.pages.login_page import LoginPage
from team_alpha.pages.dashboard_page import DashboardPage
from team_alpha.test_data.data_loader import load_user_data

@pytest.mark.team_alpha
@pytest.mark.ui
@allure.feature("Authentication")
@allure.story("User Login")
class TestLogin:
    """Test suite for login functionality."""

    @pytest.mark.smoke
    @allure.title("Successful login with valid credentials")
    @allure.description("""
        Verify that a user can successfully log in with valid credentials
        and is redirected to the dashboard.
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    def test_successful_login(self, page: Page):
        """Test successful login flow."""

        # ARRANGE: Setup test data and page objects
        user = load_user_data("valid_user")
        login_page = LoginPage(page)
        dashboard_page = DashboardPage(page)

        # ACT: Perform login operation
        with allure.step("Navigate to login page"):
            login_page.open()

        with allure.step(f"Login with username: {user['username']}"):
            login_page.login(user["username"], user["password"])

        # ASSERT: Verify successful login
        with allure.step("Verify user is on dashboard"):
            assert dashboard_page.is_loaded(), "Dashboard should be visible after login"

        with allure.step("Verify welcome message"):
            welcome_text = dashboard_page.get_welcome_message()
            assert user["expected_name"] in welcome_text, f"Expected '{user['expected_name']}' in welcome message"

        # Attach screenshot to Allure report
        allure.attach(
            page.screenshot(),
            name="dashboard_after_login",
            attachment_type=allure.attachment_type.PNG
        )

    @pytest.mark.regression
    @allure.title("Login fails with invalid credentials")
    @allure.severity(allure.severity_level.NORMAL)
    def test_invalid_credentials(self, page: Page):
        """Test login failure with invalid credentials."""

        # ARRANGE
        user = load_user_data("invalid_user")
        login_page = LoginPage(page)

        # ACT
        login_page.open().login(user["username"], user["password"])

        # ASSERT
        error_msg = login_page.get_error_message()
        assert error_msg is not None, "Error message should be displayed"
        assert "Invalid credentials" in error_msg, f"Unexpected error message: {error_msg}"
```

**Required Markers:**
```python
# Functional markers
@pytest.mark.smoke              # Critical happy path tests (fast, run first)
@pytest.mark.regression         # Comprehensive tests (slower, run in CI)
@pytest.mark.api                # API/backend tests
@pytest.mark.ui                 # UI/frontend tests

# Team markers (REQUIRED)
@pytest.mark.team_alpha         # Identifies owning team
@pytest.mark.team_beta
@pytest.mark.team_gamma

# Optional markers
@pytest.mark.slow               # Tests taking >5 seconds
@pytest.mark.skip_ci            # Skip in CI pipeline
```

**Allure Decorators (Required for all tests):**
```python
@allure.feature("Feature Name")           # High-level feature
@allure.story("User Story")               # Specific user story
@allure.title("Test case title")          # Human-readable title
@allure.description("Detailed description")  # Test purpose
@allure.severity(allure.severity_level.CRITICAL)  # BLOCKER, CRITICAL, NORMAL, MINOR, TRIVIAL
```

**Test Structure Checklist:**
- ✅ Class-based organization (`TestClassName`)
- ✅ Pytest markers (team + functional)
- ✅ Allure decorators on class and methods
- ✅ Clear AAA sections (Arrange, Act, Assert)
- ✅ Use `with allure.step()` for complex operations
- ✅ Attach screenshots/artifacts to Allure
- ✅ Descriptive assertion messages
- ✅ Load test data from YAML (don't hardcode)

---

### Rule 7: API Client Pattern

**API Client Structure:**
```python
from core.base.api_client import BaseApiClient
from playwright.sync_api import APIRequestContext, APIResponse
from typing import Dict, Any, Optional
import allure

class UserApiClient(BaseApiClient):
    """
    API client for User service endpoints.

    Inherits HTTP methods (get, post, put, patch, delete) from BaseApiClient.
    """

    def __init__(self, request_context: APIRequestContext):
        """
        Initialize User API client.

        Args:
            request_context: Playwright API request context
        """
        super().__init__(request_context)
        self.base_path = "/api/v1/users"

    @allure.step("Get user by ID: {user_id}")
    def get_user(self, user_id: int) -> APIResponse:
        """
        Retrieve user by ID.

        Args:
            user_id: User's unique identifier

        Returns:
            APIResponse: Response from GET /users/{id}
        """
        return self.get(f"{self.base_path}/{user_id}")

    @allure.step("Create new user")
    def create_user(self, user_data: Dict[str, Any]) -> APIResponse:
        """
        Create a new user.

        Args:
            user_data: User payload (name, email, role, etc.)

        Returns:
            APIResponse: Response from POST /users

        Example:
            >>> client.create_user({"name": "John", "email": "john@example.com"})
        """
        return self.post(self.base_path, data=user_data)

    @allure.step("Update user: {user_id}")
    def update_user(self, user_id: int, updates: Dict[str, Any]) -> APIResponse:
        """
        Update existing user.

        Args:
            user_id: User ID to update
            updates: Fields to update

        Returns:
            APIResponse: Response from PATCH /users/{id}
        """
        return self.patch(f"{self.base_path}/{user_id}", data=updates)

    @allure.step("Delete user: {user_id}")
    def delete_user(self, user_id: int) -> APIResponse:
        """
        Delete user by ID.

        Args:
            user_id: User ID to delete

        Returns:
            APIResponse: Response from DELETE /users/{id}
        """
        return self.delete(f"{self.base_path}/{user_id}")

    @allure.step("Search users with filters")
    def search_users(
        self,
        query: Optional[str] = None,
        role: Optional[str] = None,
        page: int = 1,
        limit: int = 20
    ) -> APIResponse:
        """
        Search users with optional filters.

        Args:
            query: Search query string
            role: Filter by role
            page: Page number (default: 1)
            limit: Results per page (default: 20)

        Returns:
            APIResponse: Response from GET /users with query params
        """
        params = {"page": page, "limit": limit}
        if query:
            params["q"] = query
        if role:
            params["role"] = role

        return self.get(self.base_path, params=params)
```

**API Test Example:**
```python
@pytest.mark.api
@pytest.mark.team_alpha
@allure.feature("User API")
@allure.story("User CRUD Operations")
class TestUserAPI:

    @pytest.mark.smoke
    @allure.title("Create and retrieve user")
    def test_create_and_get_user(self, user_api_client: UserApiClient):
        """Test user creation and retrieval."""

        # ARRANGE
        new_user = {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "role": "admin"
        }

        # ACT: Create user
        with allure.step("Create new user"):
            create_response = user_api_client.create_user(new_user)
            assert create_response.ok, f"Create failed: {create_response.status_text()}"
            created_user = create_response.json()
            user_id = created_user["id"]

        # ACT: Retrieve user
        with allure.step(f"Retrieve user with ID: {user_id}"):
            get_response = user_api_client.get_user(user_id)

        # ASSERT
        assert get_response.ok, f"Get failed: {get_response.status_text()}"
        retrieved_user = get_response.json()
        assert retrieved_user["name"] == new_user["name"]
        assert retrieved_user["email"] == new_user["email"]

        # Attach response to Allure
        allure.attach(
            get_response.text(),
            name="get_user_response",
            attachment_type=allure.attachment_type.JSON
        )
```

---

### Rule 8: Utility Functions (Leverage Existing)

**Before creating new utilities, ALWAYS check:**
```python
# core/utils/string_utils.py - 14 text processing functions
from core.utils.string_utils import (
    extract_price_from_text,      # "$1,299.99" → "$1,299.99"
    extract_number_from_text,      # "Product 123" → 123
    clean_whitespace,              # "  text  " → "text"
    extract_text_between,          # Extract text between patterns
    format_currency,               # 1299.99 → "$1,299.99"
    parse_currency_to_float,       # "$1,299.99" → 1299.99
    # ... and 8 more
)

# core/utils/wait_utils.py - 6 retry/wait patterns
from core.utils.wait_utils import (
    wait_with_retry,               # Retry function with exponential backoff
    retry_on_exception,            # Decorator for automatic retry
    wait_for_condition,            # Poll condition until true/timeout
    # ... and 3 more
)

# core/utils/element_utils.py - 11 safe element operations
from core.utils.element_utils import (
    handle_optional_dialog,        # Handle dialog if present (no fail)
    safe_extract_text,             # Extract text with default fallback
    try_multiple_locators,         # Try locators until one works
    wait_for_element_stable,       # Wait for element to stop moving
    # ... and 7 more
)
```

**Usage Examples:**

**1. Handling Optional Dialogs:**
```python
from core.utils.element_utils import handle_optional_dialog

def search(self, query: str):
    """Search with optional cookie dialog handling."""
    # Handle cookie dialog if present (doesn't fail if absent)
    handle_optional_dialog(
        self.page,
        locator='button:has-text("Accept all")',
        action="click",
        timeout=3000
    )
    self.search_input.fill(query)
    self.search_input.press("Enter")
```

**2. Retry Pattern:**
```python
from core.utils.wait_utils import wait_with_retry

def get_dynamic_content(self):
    """Get content that may take time to load."""
    content = wait_with_retry(
        func=lambda: self.page.locator("#content").text_content(),
        max_attempts=3,
        wait_time=2.0,
        exponential_backoff=True
    )
    return content
```

**3. Price Extraction:**
```python
from core.utils.string_utils import extract_price_from_text, parse_currency_to_float

def get_product_price(self) -> float:
    """Extract and parse product price."""
    price_text = self.price_element.text_content()
    price_str = extract_price_from_text(price_text)  # "$1,299.99"
    price_float = parse_currency_to_float(price_str)  # 1299.99
    return price_float
```

**4. Multiple Locator Fallback:**
```python
from core.utils.element_utils import try_multiple_locators

def find_submit_button(self):
    """Try multiple selectors for submit button."""
    button = try_multiple_locators(
        self.page,
        locators=[
            'button[type="submit"]',
            'button:has-text("Submit")',
            'input[type="submit"]',
            '#submit-btn'
        ],
        return_first=True
    )
    return button
```

---

### Rule 9: Test Data Management (YAML + Loaders)

**YAML File Structure (`team_xxx/test_data/users.yaml`):**
```yaml
# Test users organized by scenario
valid_users:
  admin_user:
    username: "admin@example.com"
    password: "SecurePass123!"
    expected_name: "Admin User"
    role: "admin"
    permissions:
      - "read"
      - "write"
      - "delete"

  regular_user:
    username: "user@example.com"
    password: "UserPass456!"
    expected_name: "Regular User"
    role: "user"
    permissions:
      - "read"

invalid_users:
  wrong_password:
    username: "admin@example.com"
    password: "WrongPassword"
    expected_error: "Invalid credentials"

  non_existent:
    username: "fake@example.com"
    password: "password"
    expected_error: "User not found"

# Configuration
test_config:
  max_login_attempts: 3
  timeout_seconds: 30
```

**Data Loader (`team_xxx/test_data/data_loader.py`):**
```python
from pathlib import Path
from typing import Dict, Any, List
from core.data.yaml_loader import BaseYamlDataLoader

class TeamAlphaDataLoader(BaseYamlDataLoader):
    """
    Team Alpha YAML data loader (Singleton).

    Caches data for performance. Only loads YAML once.
    """

    def __init__(self):
        """Initialize with team's YAML file."""
        yaml_file = Path(__file__).parent / "users.yaml"
        super().__init__(yaml_file)

# Convenience functions for easy access
def load_user_data(user_key: str) -> Dict[str, Any]:
    """
    Load specific user data by key.

    Args:
        user_key: User identifier (e.g., "admin_user", "wrong_password")

    Returns:
        User data dictionary

    Example:
        >>> user = load_user_data("admin_user")
        >>> print(user["username"])
        'admin@example.com'
    """
    loader = TeamAlphaDataLoader()

    # Search in valid_users
    if user_key in loader.data.get("valid_users", {}):
        return loader.data["valid_users"][user_key]

    # Search in invalid_users
    if user_key in loader.data.get("invalid_users", {}):
        return loader.data["invalid_users"][user_key]

    raise KeyError(f"User '{user_key}' not found in test data")

def get_all_valid_users() -> Dict[str, Dict[str, Any]]:
    """Get all valid users."""
    loader = TeamAlphaDataLoader()
    return loader.data.get("valid_users", {})

def get_test_config() -> Dict[str, Any]:
    """Get test configuration."""
    loader = TeamAlphaDataLoader()
    return loader.data.get("test_config", {})
```

**Usage in Tests:**
```python
from team_alpha.test_data.data_loader import load_user_data, get_test_config

def test_admin_login(self, page: Page):
    """Test admin user login."""
    # Load data from YAML
    admin = load_user_data("admin_user")
    config = get_test_config()

    login_page = LoginPage(page)
    login_page.open()
    login_page.login(admin["username"], admin["password"])

    # Use expected values from YAML
    dashboard = DashboardPage(page)
    assert admin["expected_name"] in dashboard.get_welcome_message()

# Parametrized tests with YAML data
@pytest.mark.parametrize("user_key", ["admin_user", "regular_user"])
def test_multiple_users(self, page: Page, user_key: str):
    """Test login with multiple user types."""
    user = load_user_data(user_key)
    # Test logic...
```

---

### Rule 10: Configuration Management

**Using Config Singleton:**
```python
from core.config import config

# Access environment variables through config object
base_url = config.web_base_url           # From WEB_BASE_URL env var
api_url = config.api_base_url            # From API_BASE_URL env var
headless = config.headless               # From HEADLESS env var
browser = config.browser                 # From BROWSER env var

# Boolean environment variables
if config.record_video:
    # Video recording enabled
    pass

# Custom environment variables
auth_token = config.get_env("API_AUTH_TOKEN", "default-token")
```

**❌ NEVER hardcode URLs or credentials:**
```python
# WRONG
def test_login(self):
    self.page.goto("https://staging.example.com")  # WRONG - hardcoded
    self.login("admin", "password123")              # WRONG - hardcoded credentials
```

**✅ ALWAYS use Config or .env:**
```python
# CORRECT
from core.config import config

def test_login(self):
    self.page.goto(config.web_base_url)  # From environment
    user = load_user_data("admin_user")  # From YAML
    self.login(user["username"], user["password"])
```

---

## 🚫 Anti-Patterns to Avoid

### Anti-Pattern 1: Direct sleep() Calls
**❌ WRONG:**
```python
import time
self.page.click("#button")
time.sleep(5)  # Brittle, slow, unreliable
```

**✅ CORRECT:**
```python
from core.utils.wait_utils import wait_for_condition
self.page.click("#button")
wait_for_condition(
    lambda: self.page.locator("#result").is_visible(),
    timeout=10.0
)
```

### Anti-Pattern 2: Test Dependencies
**❌ WRONG:**
```python
class TestUserFlow:
    user_id = None  # Shared state

    def test_01_create_user(self):
        # Creates user, stores ID
        TestUserFlow.user_id = created_user["id"]

    def test_02_update_user(self):
        # Depends on test_01 running first
        update_user(TestUserFlow.user_id)  # FRAGILE
```

**✅ CORRECT:**
```python
class TestUserFlow:
    @pytest.fixture
    def created_user(self, api_client):
        """Fixture creates user for each test independently."""
        user = api_client.create_user({"name": "Test"})
        yield user
        api_client.delete_user(user["id"])  # Cleanup

    def test_update_user(self, api_client, created_user):
        """Independent test, no dependencies."""
        api_client.update_user(created_user["id"], {"name": "Updated"})
```

### Anti-Pattern 3: Catch-All Exception Handling
**❌ WRONG:**
```python
try:
    element.click()
except Exception:  # Hides real issues
    pass
```

**✅ CORRECT:**
```python
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

try:
    element.click(timeout=5000)
except PlaywrightTimeoutError:
    log.warning("Element not clickable, trying alternative locator")
    alternative_element.click()
```

### Anti-Pattern 4: Page Inheritance Chains
**❌ WRONG:**
```python
class LoginPage(BasePage): pass
class DashboardPage(LoginPage): pass  # WRONG - inherits from LoginPage
class SettingsPage(DashboardPage): pass  # WRONG - deep inheritance
```

**✅ CORRECT:**
```python
class LoginPage(BasePage): pass
class DashboardPage(BasePage): pass  # CORRECT - inherits from BasePage
class SettingsPage(BasePage): pass   # CORRECT - flat hierarchy
```

### Anti-Pattern 5: Modifying Core Framework
**❌ WRONG:**
```python
# Directly editing core/base/page_base.py
# Adding team-specific logic to core utilities
```

**✅ CORRECT:**
```python
# Create team-specific utilities in team_xxx/utils/
# Extend base classes in team directory
# Propose changes to core via PR if truly universal
```

---

## 📋 Code Quality Checklist

Before generating code, ensure:

### For Page Objects:
- [ ] Extends `BasePage`
- [ ] All locators defined in `team_xxx/locators/locators.py`
- [ ] Type hints on all methods (Python 3.9 compatible)
- [ ] `@allure.step()` decorators on public methods
- [ ] Returns `self` from action methods
- [ ] Comprehensive docstrings
- [ ] Uses utility functions from `core/utils/`
- [ ] `open()` method for page navigation

### For API Clients:
- [ ] Extends `BaseApiClient`
- [ ] Type hints on all methods
- [ ] `@allure.step()` decorators
- [ ] Descriptive method names (get_user, create_order, etc.)
- [ ] Docstrings with examples
- [ ] Returns `APIResponse` objects

### For Tests:
- [ ] Class-based organization
- [ ] Team marker (e.g., `@pytest.mark.team_alpha`)
- [ ] Functional markers (`@pytest.mark.smoke`, `@pytest.mark.api`, etc.)
- [ ] Allure decorators (feature, story, title, severity)
- [ ] Clear AAA structure (Arrange, Act, Assert)
- [ ] Uses fixtures for setup (not manual instantiation)
- [ ] Loads test data from YAML
- [ ] Descriptive assertion messages
- [ ] Allure attachments (screenshots, JSON responses)

### For All Code:
- [ ] Type hints (Python 3.9 compatible: `Union`, `Optional`, `List`, etc.)
- [ ] Docstrings (module, class, function)
- [ ] No hardcoded URLs, credentials, or magic values
- [ ] No `time.sleep()` (use wait utilities)
- [ ] Proper exception handling (specific exceptions)
- [ ] Line length ≤ 130 characters
- [ ] Follows isort + Black + Ruff standards
- [ ] No secrets or `.env` content in code

---

## 🎓 Decision Trees for Common Scenarios

### Scenario 1: "I need to interact with a new page"

```
START
  ↓
Do locators exist in team_xxx/locators/locators.py?
  NO → Add new class to locators.py (e.g., NewPageLocators)
  YES ↓

Does page object exist in team_xxx/pages/?
  NO → Create new page object extending BasePage
  YES ↓

Does method exist on page object?
  NO → Add method to existing page object
  YES → Use existing method
  ↓
Write test using page object + fixtures
```

### Scenario 2: "I need to make an API call"

```
START
  ↓
Does API client exist in team_xxx/api_clients/?
  NO → Create API client extending BaseApiClient
  YES ↓

Does method exist on API client?
  NO → Add method to existing API client
  YES → Use existing method
  ↓
Write test using api_client fixture
```

### Scenario 3: "I need to add test data"

```
START
  ↓
Does YAML file exist for this data type?
  NO → Create new YAML file in team_xxx/test_data/
  YES → Add data to existing YAML file
  ↓
Does data loader exist?
  NO → Create data_loader.py with convenience functions
  YES → Add convenience function if needed
  ↓
Use load_xxx_data() in tests
```

### Scenario 4: "I need a utility function"

```
START
  ↓
Check core/utils/ for existing utilities
  ↓
Does similar utility exist?
  YES → Use existing utility
  NO ↓

Is it universally useful (all teams)?
  YES → Add to core/utils/ (requires approval)
  NO → Add to team_xxx/utils/
```

---

## 🔍 Code Review Questions to Ask Yourself

1. **Does this code extend base classes?**
   - Page objects should extend `BasePage`
   - API clients should extend `BaseApiClient`

2. **Are locators centralized?**
   - All locators in `team_xxx/locators/locators.py`
   - No hardcoded selectors in page objects

3. **Are type hints complete and Python 3.9 compatible?**
   - Use `Union[]` not `|`
   - Use `Optional[]` not `Type | None`

4. **Is test data externalized?**
   - No hardcoded credentials or URLs
   - Data from YAML files or Config

5. **Are tests independent?**
   - No shared state between tests
   - Each test can run in isolation

6. **Is the AAA pattern clear?**
   - Arrange, Act, Assert sections visible
   - Allure steps for complex operations

7. **Are resources cleaned up?**
   - Fixtures use yield and cleanup
   - No resource leaks

8. **Is code reusable?**
   - Utility functions leveraged
   - No code duplication

---

## 🚀 Quick Reference: Common Code Snippets

### New Page Object Template
```python
from core.base.page_base import BasePage
from playwright.sync_api import Page
from team_alpha.locators.locators import NewPageLocators
import allure

class NewPage(BasePage):
    """New page description."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "https://example.com/new-page"
        self.element = page.locator(NewPageLocators.ELEMENT)

    @allure.step("Open new page")
    def open(self) -> "NewPage":
        """Navigate to page."""
        self.navigate(self.url)
        self.wait_for_load_state("domcontentloaded")
        return self

    @allure.step("Perform action")
    def action(self) -> "NewPage":
        """Perform page action."""
        self.element.click()
        return self
```

### New API Client Template
```python
from core.base.api_client import BaseApiClient
from playwright.sync_api import APIRequestContext, APIResponse
from typing import Dict, Any
import allure

class NewApiClient(BaseApiClient):
    """New API client description."""

    def __init__(self, request_context: APIRequestContext):
        super().__init__(request_context)
        self.base_path = "/api/v1/resource"

    @allure.step("Get resource")
    def get_resource(self, resource_id: int) -> APIResponse:
        """Get resource by ID."""
        return self.get(f"{self.base_path}/{resource_id}")
```

### New Test Template
```python
import pytest
import allure
from playwright.sync_api import Page

@pytest.mark.team_alpha
@pytest.mark.ui
@allure.feature("Feature Name")
@allure.story("User Story")
class TestNewFeature:

    @pytest.mark.smoke
    @allure.title("Test case title")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_scenario(self, page: Page):
        """Test description."""
        # ARRANGE
        test_data = load_test_data("key")
        page_obj = PageObject(page)

        # ACT
        with allure.step("Perform action"):
            page_obj.open().action()

        # ASSERT
        assert page_obj.verify_result(), "Result should be visible"
```

---

## 📖 Additional Resources

- **Project Documentation**: See `PROJECT_GUIDE.md` for comprehensive framework guide
- **Architecture Diagrams**: See `ARCHITECTURE.md` for visual architecture
- **Contributing Guidelines**: See `CONTRIBUTING.md` for code standards
- **Quick Reference**: See `QUICK_REFERENCE.md` for common tasks

---

## ✅ Final Reminders

1. **Consistency is key** - Follow existing patterns, don't invent new ones
2. **Reuse before creating** - Check `core/` and existing code first
3. **Type everything** - Full type hints required (Python 3.9 compatible)
4. **Document thoroughly** - Docstrings and comments for clarity
5. **Test independently** - No test dependencies or execution order
6. **Think about maintenance** - Code will be read more than written
7. **Security first** - Never commit secrets or hardcode credentials

---

**When in doubt, look at `team_alpha/` as the reference implementation.**

This framework is designed for scalability, maintainability, and consistency. Every line of code you generate should uphold these principles.
