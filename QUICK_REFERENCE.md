# Quick Reference Guide

**Fast lookup for common tasks and patterns in the QA Test Automation Framework**

---

## 🚀 Quick Start

```bash
# Clone and setup
git clone <repo-url>
cd ppMonoRepo
poetry install
poetry run playwright install chromium

# Run tests
make test-all

# View reports
make allure-serve
```

---

## 📂 File Locations Cheat Sheet

| What                  | Where                                      |
|-----------------------|--------------------------------------------|
| Environment config    | `.env`                                     |
| Test configuration    | `pytest.ini`                               |
| Dependencies          | `pyproject.toml`                           |
| Command shortcuts     | `Makefile`                                 |
| Core base classes     | `core/base/`                               |
| Reusable utilities    | `core/utils/`                              |
| Team tests            | `team_alpha/tests/`                        |
| Page objects          | `team_alpha/pages/`                        |
| API clients           | `team_alpha/api_clients/`                  |
| Locators              | `team_alpha/locators/locators.py`          |
| Test data             | `team_alpha/test_data/google_shopping.yaml`|
| Generated logs        | `logs/`                                    |
| Screenshots           | `screenshots/`                             |
| Videos                | `videos/`                                  |
| Allure reports        | `allure-report/`                           |

---

## 🎯 Common Test Commands

```bash
# Run tests
make test-all              # All tests
make test-api              # API tests only
make test-web              # Web UI tests only
make test-smoke            # Smoke tests only

# With pytest directly
poetry run pytest                              # All tests
poetry run pytest team_alpha/                  # Team tests
poetry run pytest -m smoke                     # By marker
poetry run pytest -k "test_login"              # By name pattern
poetry run pytest -n auto                      # Parallel
poetry run pytest -v                           # Verbose
poetry run pytest --lf                         # Last failed
poetry run pytest --sw                         # Stepwise

# Environment control
HEADLESS=true poetry run pytest                # Headless browser
RECORD_VIDEO=true poetry run pytest            # Record videos
BROWSER=firefox poetry run pytest              # Different browser

# Reports
make allure-report         # Generate HTML report
make allure-serve          # Generate and open

# Cleanup
make clean-videos          # Delete video files
rm -rf logs/ screenshots/  # Delete logs/screenshots
```

---

## 💻 Code Patterns

### Create a New Page Object

```python
# team_alpha/pages/my_page.py
from playwright.sync_api import Page, Locator
from core.base.page_base import BasePage
from core.logger import log
from team_alpha.locators import MyPageLocators

class MyPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.button = page.locator(MyPageLocators.BUTTON)
        self.input = page.locator(MyPageLocators.INPUT)

    def click_button(self):
        log.info("Clicking button")
        self.button.click()

    def fill_input(self, text: str):
        self.input.fill(text)
```

### Create a New API Client

```python
# team_alpha/api_clients/my_api_client.py
import allure
from playwright.sync_api import APIRequestContext, APIResponse
from core.base.api_client import BaseApiClient

class MyApiClient(BaseApiClient):
    @allure.step("Get users")
    def get_users(self) -> APIResponse:
        return self.get("/api/users")

    @allure.step("Create user: {name}")
    def create_user(self, name: str, email: str) -> APIResponse:
        data = {"name": name, "email": email}
        return self.post("/api/users", data=data)
```

### Create Locators

```python
# team_alpha/locators/locators.py
class MyPageLocators:
    """Locators for MyPage"""
    BUTTON = 'button#submit'
    INPUT = 'input[name="username"]'
    TITLE = 'h1.page-title'
    ERROR_MESSAGE = 'div.error'

    # Multiple fallback selectors
    PRICE = 'span.price, div.product-price, [data-testid="price"]'
```

### Write a Web Test

```python
# team_alpha/tests/web/test_my_feature.py
import pytest
import allure
from playwright.sync_api import Page
from team_alpha.pages.my_page import MyPage

@pytest.mark.team_alpha
@pytest.mark.ui
@allure.feature("My Feature")
class TestMyFeature:

    @pytest.mark.smoke
    @allure.title("User can perform action")
    def test_user_action(self, page: Page):
        # Arrange
        my_page = MyPage(page)

        # Act
        my_page.navigate("https://example.com")
        my_page.fill_input("test data")
        my_page.click_button()

        # Assert
        assert my_page.get_title() == "Success"
```

### Write an API Test

```python
# team_alpha/tests/api/test_my_api.py
import pytest
import allure
from playwright.sync_api import APIRequestContext
from team_alpha.api_clients.my_api_client import MyApiClient

@pytest.mark.team_alpha
@pytest.mark.api
@allure.feature("User API")
class TestUserAPI:

    def test_get_users(self, api_request_context: APIRequestContext):
        # Arrange
        client = MyApiClient(api_request_context)

        # Act
        response = client.get_users()

        # Assert
        assert response.ok
        body = response.json()
        assert "users" in body
```

### Create Test Data

```yaml
# team_alpha/test_data/my_data.yaml
users:
  admin:
    username: "admin"
    password: "admin123"
    role: "administrator"

  guest:
    username: "guest"
    password: "guest123"
    role: "viewer"

config:
  timeout: 30
  retries: 3
```

```python
# team_alpha/test_data/data_loader.py
from pathlib import Path
from dataclasses import dataclass
from typing import Dict
from core.data import BaseYamlDataLoader

@dataclass
class UserData:
    username: str
    password: str
    role: str

class TeamAlphaDataLoader(BaseYamlDataLoader):
    def __init__(self):
        yaml_file = Path(__file__).parent / "my_data.yaml"
        super().__init__(yaml_file)

    def get_user(self, key: str) -> UserData:
        data = self.get_section_item("users", key)
        return UserData(**data)

# Convenience function
_loader = TeamAlphaDataLoader()

def load_user_data(key: str) -> UserData:
    return _loader.get_user(key)
```

```python
# Use in tests
from team_alpha.test_data import load_user_data

def test_login():
    user = load_user_data("admin")
    login(user.username, user.password)
```

---

## 🔧 Using Core Utilities

### String Utilities

```python
from core.utils import (
    extract_price_from_text,
    sanitize_text,
    truncate_text,
    extract_email_from_text,
)

# Extract price
price = extract_price_from_text("Product: $1,299.99")  # "$1,299.99"
price_float = extract_price_from_text("$999", return_as_float=True)  # 999.0

# Clean text
clean = sanitize_text("  Hello   World  \n")  # "Hello World"

# Truncate
short = truncate_text("Long text here", max_length=10)  # "Long te..."

# Extract email
email = extract_email_from_text("Contact: user@test.com")  # "user@test.com"
```

### Wait/Retry Utilities

```python
from core.utils import wait_with_retry, retry_on_exception, wait_for_condition

# Retry function
result = wait_with_retry(
    lambda: get_element(),
    max_attempts=3,
    wait_time=2.0
)

# Decorator
@retry_on_exception(max_attempts=3)
def flaky_api_call():
    return api.get_data()

# Wait for condition
wait_for_condition(
    lambda: page.locator("#result").is_visible(),
    timeout=10.0,
    poll_interval=0.5
)
```

### Element Utilities

```python
from core.utils import (
    handle_optional_dialog,
    safe_extract_text,
    try_multiple_locators,
    safe_click,
)

# Handle optional popups
handle_optional_dialog(page, "button:has-text('Accept cookies')")

# Safe text extraction
text = safe_extract_text(element, default="Not found")

# Try multiple locators
element = try_multiple_locators(
    page,
    ["span.price", "div.cost", "span:has-text('$')"]
)

# Safe click with retry
safe_click(button, timeout=5000, retry_count=3)
```

---

## 🎨 Allure Annotations

```python
import allure

# Feature and Story
@allure.feature("User Management")
@allure.story("User Login")
def test_login():
    pass

# Title and Description
@allure.title("User can login with valid credentials")
@allure.description("This test verifies login functionality")
def test_login():
    pass

# Severity
@allure.severity(allure.severity_level.CRITICAL)
def test_critical():
    pass

# Steps
@allure.step("Navigate to login page")
def navigate_to_login():
    pass

# Or inline
with allure.step("Enter credentials"):
    page.fill("#username", "user")
    page.fill("#password", "pass")

# Attachments
allure.attach(screenshot, name="Screenshot", attachment_type=allure.attachment_type.PNG)
allure.attach(response.text(), name="API Response", attachment_type=allure.attachment_type.JSON)
```

---

## 🏷️ pytest Markers

```python
# Mark single test
@pytest.mark.smoke
def test_critical():
    pass

# Multiple markers
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.team_alpha
def test_something():
    pass

# Parametrize
@pytest.mark.parametrize("username,password", [
    ("user1", "pass1"),
    ("user2", "pass2"),
])
def test_login(username, password):
    pass

# Skip
@pytest.mark.skip(reason="Not implemented yet")
def test_future():
    pass

# Skip if condition
@pytest.mark.skipif(sys.platform == "win32", reason="Unix only")
def test_unix_only():
    pass

# Expected to fail
@pytest.mark.xfail(reason="Known bug")
def test_broken():
    pass
```

---

## 📊 Configuration Quick Access

### From .env
```python
from core.config import config

config.headless          # True/False
config.browser           # "chromium"/"firefox"/"webkit"
config.api_base_url      # "https://api.example.com"
config.api_auth_token    # "token123"
config.record_video      # True/False
```

### Logging
```python
from core.logger import log

log.debug("Debug message")
log.info("Info message")
log.warning("Warning message")
log.error("Error message")
log.critical("Critical message")
```

---

## 🔍 Common Playwright Patterns

### Page Interactions
```python
# Navigate
page.goto("https://example.com")

# Click
page.click("#button")
page.locator("button").click()

# Fill input
page.fill("#username", "test")
page.locator("#password").fill("pass")

# Press key
page.press("#input", "Enter")

# Select dropdown
page.select_option("#dropdown", "value")

# Check/uncheck
page.check("#checkbox")
page.uncheck("#checkbox")

# Get text
text = page.inner_text("#element")
text = page.locator("h1").inner_text()

# Get attribute
href = page.get_attribute("a", "href")

# Wait
page.wait_for_selector("#element")
page.wait_for_url("**/dashboard")
page.wait_for_load_state("networkidle")
page.wait_for_timeout(1000)  # milliseconds
```

### Locator Strategies
```python
# By ID
page.locator("#element-id")

# By class
page.locator(".class-name")

# By attribute
page.locator('[data-testid="submit"]')

# By text
page.locator("text=Login")
page.locator("button:has-text('Submit')")

# By role
page.locator("role=button[name='Submit']")

# CSS selector
page.locator("div.container > button.primary")

# XPath
page.locator("//button[@type='submit']")

# Multiple matches
page.locator("li").first
page.locator("li").last
page.locator("li").nth(2)
page.locator("li").count()
```

### Assertions
```python
from playwright.sync_api import expect

# Visible
expect(page.locator("#element")).to_be_visible()

# Hidden
expect(page.locator("#element")).to_be_hidden()

# Enabled
expect(page.locator("button")).to_be_enabled()

# Text content
expect(page.locator("h1")).to_have_text("Welcome")
expect(page.locator("h1")).to_contain_text("Wel")

# Value
expect(page.locator("#input")).to_have_value("test")

# Attribute
expect(page.locator("a")).to_have_attribute("href", "/home")

# Count
expect(page.locator("li")).to_have_count(5)

# URL
expect(page).to_have_url("https://example.com")
expect(page).to_have_url(re.compile(r".*dashboard"))

# Title
expect(page).to_have_title("Dashboard")
```

---

## 🐛 Debugging Tips

### Enable Playwright Inspector
```bash
PWDEBUG=1 poetry run pytest tests/test_file.py
```

### Slow Down Execution
```python
page = browser.new_page(slow_mo=1000)  # 1 second delay
```

### Screenshots
```python
page.screenshot(path="screenshot.png")
page.screenshot(path="full-page.png", full_page=True)
```

### Console Logs
```python
page.on("console", lambda msg: print(f"Browser: {msg.text}"))
```

### Network Requests
```python
page.on("request", lambda req: print(f">> {req.method} {req.url}"))
page.on("response", lambda res: print(f"<< {res.status} {res.url}"))
```

### Pause Execution
```python
page.pause()  # Opens Playwright Inspector
```

---

## 📝 Common pytest Fixtures

```python
# Playwright fixtures
def test_example(page):                    # Browser page
def test_example(context):                 # Browser context
def test_example(browser):                 # Browser instance
def test_example(browser_type):            # Browser type

# Core fixtures (from core/conftest.py)
def test_example(api_request_context):     # API context

# Team fixtures (from team_alpha/conftest.py)
def test_example(reqres_api_client):       # ReqRes API client

# Built-in pytest fixtures
def test_example(tmp_path):                # Temp directory
def test_example(monkeypatch):             # Monkeypatch
def test_example(capsys):                  # Capture stdout/stderr
def test_example(request):                 # Test request info
```

---

## 🎬 Video Recording

```bash
# Enable in .env
RECORD_VIDEO=true

# Or via command line
RECORD_VIDEO=true poetry run pytest

# Videos saved to: videos/
# Format: .webm
# Resolution: 1920x1080
# Works in both headed and headless mode
```

---

## 📸 Screenshots

```bash
# Automatic on failure
# Saved to: screenshots/
# Format: failure_{test_name}.png

# Manual in test
page.screenshot(path="screenshots/my-screenshot.png")
```

---

## 🚦 CI/CD (.gitlab-ci.yml)

```yaml
# Example job
test:
  stage: test
  script:
    - poetry install
    - poetry run playwright install chromium
    - make test-all
  artifacts:
    when: always
    paths:
      - allure-results/
      - logs/
      - screenshots/
    expire_in: 1 week
```

---

## 🔗 Useful Links

- **Playwright Python**: https://playwright.dev/python/
- **pytest**: https://docs.pytest.org/
- **Allure**: https://docs.qameta.io/allure/
- **Poetry**: https://python-poetry.org/docs/
- **Loguru**: https://loguru.readthedocs.io/

---

## 📞 Getting Help

1. Check inline documentation (`docstrings`)
2. Read `PROJECT_GUIDE.md` for detailed explanations
3. Check test examples in `team_alpha/tests/`
4. Review base classes in `core/base/`
5. Contact the QA team

---

**Quick Reference v1.0** | Last updated: 2025-10-17
