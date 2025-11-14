# GitHub Copilot Custom Instructions - Web Testing

## Framework Stack
- **Playwright** (async browser automation)
- **Pytest** (testing framework)
- **Python 3.9-3.11**
- **Allure** (reporting with `@allure.step()`)
- **Loguru** (structured logging via `log.info()`, `log.debug()`)

---

## Page Object Model (POM)

### Inheritance Rule
**ALWAYS** inherit from `BasePage` when creating new page classes:
```python
from core.base.page_base import BasePage
from playwright.sync_api import Page

class NewPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "https://..."
```

### Locator Initialization
Store locators as instance variables from centralized locator classes:
```python
from team_alpha.locators.locators import GoogleSearchLocators

class GoogleSearchPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.search_input = page.locator(GoogleSearchLocators.SEARCH_INPUT)
        self.search_button = page.locator(GoogleSearchLocators.SEARCH_BUTTON)
```

### Method Requirements
**Every public method MUST:**
1. Use `@allure.step()` decorator with dynamic parameters
2. Return `self` for method chaining
3. Include docstring with Args/Returns
4. Log major actions with `log.info()`

```python
@allure.step("Search for: {query}")
def search(self, query: str) -> 'GoogleSearchPage':
    """
    Enter search query and submit.

    Args:
        query: Search term to enter

    Returns:
        Self for method chaining
    """
    log.info(f"Searching for: {query}")
    self.search_input.fill(query)
    self.search_button.click()
    return self
```

### BasePage Inherited Methods
Use these built-in methods from `BasePage`:
- `navigate(url)` - Navigate with logging
- `wait_for_element(selector, timeout)` - Wait for visibility
- `click(selector)`, `fill(selector, text)` - Basic interactions
- `get_text(selector)`, `is_visible(selector)` - Element queries
- `scroll_to_element(selector)` - Scrolling
- `take_screenshot(name)` - Screenshot capture
- `wait_for_load_state(state)` - Page load waiting

---

## Action Composition Pattern

### When to Use Actions
Create Action classes for:
- Multi-page workflows (e.g., login → dashboard → settings)
- Business logic spanning multiple page objects
- Reusable test scenarios across multiple tests

### Action Class Structure
```python
from playwright.sync_api import Page
import allure

class ShoppingActions:
    """Orchestrate multi-page shopping workflows."""

    def __init__(self, page: Page, data_loader=None):
        self.page = page
        self.search_page = GoogleSearchPage(page)
        self.shopping_page = GoogleShoppingPage(page)
        self.data_loader = data_loader or load_product_data

        # Store context for chained operations
        self._current_product_data = None
        self._last_result = None
```

### Fluent Interface Pattern
**ALWAYS return `self`** from action methods for chaining:
```python
@allure.step("Search for product: {product_key}")
def search_for_product(self, product_key: str) -> 'ShoppingActions':
    self._current_product_data = self.data_loader(product_key)
    self.search_page.open()
    self.search_page.search(self._current_product_data.search_term)
    return self

@allure.step("Verify minimum {min_count} results displayed")
def verify_search_results(self, min_count: int = 3) -> 'ShoppingActions':
    count = self.shopping_page.get_product_count()
    assert count >= min_count, f"Expected >={min_count}, found {count}"
    return self
```

### Test Usage
```python
def test_product_workflow(page: Page):
    actions = ShoppingActions(page, load_product_data)
    (actions
        .search_for_product("samsung_s24_ultra")
        .verify_search_results(min_count=3)
        .extract_and_verify_price())
```

---

## Test Structure

### Test Class Template
```python
import pytest
import allure
from playwright.sync_api import Page

@pytest.mark.team_alpha  # Team identifier
@pytest.mark.ui          # Test type: ui or api
@allure.feature("Feature Name")
@allure.story("User Story")
class TestFeatureName:
    """Test suite description."""

    @pytest.mark.smoke  # Priority: smoke, regression
    @allure.title("Descriptive test title")
    @allure.description("What this test validates")
    @allure.severity(allure.severity_level.NORMAL)
    def test_scenario_name(self, page: Page):
        """Test docstring."""
        actions = FeatureActions(page, load_feature_data)
        (actions
            .step_one()
            .step_two()
            .verify_result())
```

### Fixtures Usage
**Available fixtures** (auto-injected by Pytest):
- `page: Page` - Fresh browser page per test (30s timeout)
- `browser_context_args` - Session-scoped context config
- `api_request_context` - Session-scoped API client
- `take_screenshot(name)` - Manual screenshot helper

### Pytest Markers
- `@pytest.mark.team_alpha` / `team_beta` / `team_gamma` - Team identification
- `@pytest.mark.ui` - Web UI test
- `@pytest.mark.smoke` - Critical path test
- `@pytest.mark.regression` - Full regression suite

---

## Centralized Locators

### Locator Organization
**NEVER hardcode selectors in page objects.** Store ALL locators in `team_*/locators/locators.py`:

```python
class GoogleSearchLocators:
    """Google Search page locators."""

    # Use descriptive constant names in UPPER_SNAKE_CASE
    SEARCH_INPUT = 'textarea[name="q"], input[name="q"]'  # Fallback selectors
    SEARCH_BUTTON = 'button[type="submit"]'
    SHOPPING_TAB = 'a[href*="tbm=shop"]'
    COOKIE_ACCEPT_ALL = 'button:has-text("Accept all")'

class GoogleShoppingLocators:
    """Google Shopping page locators."""

    PRODUCT_CARD = "div.sh-dgr__content"
    PRODUCT_TITLE = "h3.tAxDx"
    PRODUCT_PRICE = 'span.a8Pemb, span:has-text("$")'  # Multiple fallbacks
```

### Locator Strategy Priority
1. **Stable attributes**: `[data-testid="..."]`, `[name="..."]`, `[id="..."]`
2. **Semantic selectors**: `button[type="submit"]`, `a[href*="..."]`
3. **Text-based**: `button:has-text("Submit")` (use for labels that don't change)
4. **CSS classes**: `div.product-card` (least stable, use as last resort)

### Multiple Fallbacks
Combine selectors with commas for resilience:
```python
PRICE = 'span.price-primary, span.product-price, span:has-text("$")'
```

---

## Utilities Usage

### Import Core Utilities
```python
from core.utils.element_utils import (
    handle_optional_dialog,
    safe_click,
    safe_extract_text,
    try_multiple_locators,
    wait_for_element_count
)
from core.utils.string_utils import (
    extract_price_from_text,
    extract_number_from_text,
    sanitize_text,
    clean_currency
)
from core.utils.wait_utils import (
    wait_with_retry,
    retry_on_exception,
    wait_for_condition
)
```

### Common Utility Patterns

#### Handle Optional Dialogs
Use for cookie banners, pop-ups, modals that may or may not appear:
```python
handle_optional_dialog(
    self.page,
    CookieLocators.ACCEPT_ALL,
    action="click",
    timeout=2000  # Short timeout, non-blocking
)
```

#### Safe Text Extraction
Always use with default fallback:
```python
title = safe_extract_text(
    self.product_title,
    default="",
    timeout=3000,
    trim=True
)
```

#### Try Multiple Locators
When element structure varies:
```python
price_locators = [
    ShoppingLocators.PRICE_PRIMARY,
    'span.price',
    'div:has-text("$")'
]
price_element = try_multiple_locators(
    self.page,
    price_locators,
    return_first=True
)
```

#### Extract Prices
Always use utility for price parsing:
```python
price_text = safe_extract_text(locator, default="")
price_float = extract_price_from_text(
    price_text,
    currency_symbol="$",
    return_as_float=True
)
```

---

## Error Handling

### Wait Strategies

#### Use Playwright Auto-Waiting
Playwright waits automatically before actions. **DO NOT add explicit waits unless necessary:**
```python
# GOOD - Auto-waits before clicking
locator.click()

# AVOID - Unnecessary explicit wait
locator.wait_for(state="visible")
locator.click()
```

#### Strategic Explicit Waits
Use only when auto-waiting isn't sufficient:
```python
# Wait for URL pattern
self.page.wait_for_url("**/checkout", timeout=10000)

# Wait for network idle
self.page.wait_for_load_state("networkidle")

# Wait for specific element count
wait_for_element_count(
    self.page.locator(ProductLocators.CARD),
    expected_count=5,
    operator=">="
)
```

#### Retry Pattern
Use for flaky operations:
```python
@retry_on_exception(max_attempts=3, wait_time=1.0)
def get_dynamic_content(self):
    content = self.page.locator("#dynamic").text_content()
    if not content:
        raise ValueError("Content not loaded")
    return content
```

### CAPTCHA/Bot Detection
Check for common patterns:
```python
current_url = self.page.url
if "sorry/index" in current_url or "captcha" in current_url:
    raise Exception(f"Bot detection triggered. URL: {current_url}")
```

### Assertion Messages
**ALWAYS include descriptive messages:**
```python
# GOOD
assert price != "Price not found", f"Failed to extract price from listing"
assert product_count >= 3, f"Expected >=3 products, found {product_count}"

# BAD
assert price != "Price not found"
assert product_count >= 3
```

---

## Allure Reporting

### Step Decoration
**Every public method** in page objects and actions MUST use `@allure.step()`:
```python
@allure.step("Click 'Add to Cart' button")
def add_to_cart(self) -> 'ProductPage':
    log.info("Adding product to cart")
    self.add_to_cart_button.click()
    return self
```

### Dynamic Step Parameters
Include dynamic values in step names:
```python
@allure.step("Search for product: {product_name}")
def search_product(self, product_name: str):
    ...

@allure.step("Verify price is ${expected_price}")
def verify_price(self, expected_price: float):
    ...
```

### Attach Data to Reports
For complex data or debugging:
```python
import allure

details_text = f"Title: {title}\nPrice: {price}\nRating: {rating}"
allure.attach(
    details_text,
    name="Product Details",
    attachment_type=allure.attachment_type.TEXT
)
```

### Test Metadata
Always include on test methods:
```python
@allure.title("User can filter products by price range")
@allure.description("""
    1. Navigate to product listing
    2. Apply price filter $50-$100
    3. Verify all results within range
""")
@allure.severity(allure.severity_level.CRITICAL)
def test_price_filter(self, page: Page):
    ...
```

---

## Logging Best Practices

### Log Levels
Use appropriate levels via Loguru:
```python
from core.utils.logger import log

log.info("User navigated to checkout page")          # Major actions
log.debug(f"Waiting for element: {selector}")        # Debugging details
log.warning("Cookie banner not found, continuing")   # Non-fatal issues
log.error(f"Failed to extract price from: {text}")   # Errors before exception
```

### Log Format
- Use f-strings for dynamic values
- Log at the START of major actions
- Include context (page name, element, data)

```python
@allure.step("Complete checkout for order: {order_id}")
def complete_checkout(self, order_id: str) -> 'CheckoutActions':
    log.info(f"Starting checkout for order: {order_id}")
    self.checkout_page.fill_shipping_info()
    log.info("Shipping info filled")
    self.checkout_page.submit_order()
    log.info(f"Order {order_id} submitted successfully")
    return self
```

---

## Code Style Conventions

### Naming Conventions
| Type | Convention | Example |
|------|-----------|---------|
| Test files | `test_<feature>.py` | `test_google_shopping.py` |
| Page objects | `<page>_page.py` | `google_search_page.py` |
| Actions | `<domain>_actions.py` | `shopping_actions.py` |
| Test classes | `Test<Feature>` | `TestGoogleShopping` |
| Page classes | `<Page>Page` | `GoogleSearchPage` |
| Action classes | `<Domain>Actions` | `ShoppingActions` |
| Locator classes | `<Page>Locators` | `GoogleSearchLocators` |
| Test methods | `test_<scenario>` | `test_samsung_s24_price_check` |
| Page methods | `<verb>_<noun>` | `click_submit`, `get_product_title` |
| Variables | `snake_case` | `product_count`, `search_results` |
| Constants | `UPPER_SNAKE_CASE` | `SEARCH_INPUT`, `MAX_TIMEOUT` |

### Method Chaining
Always return `self` from page objects and actions:
```python
def click_submit(self) -> 'LoginPage':
    self.submit_button.click()
    return self

def fill_username(self, username: str) -> 'LoginPage':
    self.username_input.fill(username)
    return self
```

### Type Hints
Use for all method parameters and returns:
```python
def search_product(self, query: str, filters: dict[str, str] | None = None) -> 'SearchPage':
    ...

def get_product_count(self) -> int:
    ...
```

### Docstrings
Include for all public methods:
```python
def filter_by_price(self, min_price: float, max_price: float) -> 'ProductListingPage':
    """
    Apply price range filter to product listings.

    Args:
        min_price: Minimum price threshold
        max_price: Maximum price threshold

    Returns:
        Self for method chaining
    """
    ...
```

---

## Test Data Management

### YAML Structure
Store test data in `team_*/test_data/<feature>.yaml`:
```yaml
products:
  samsung_s24_ultra:
    search_term: "Samsung Galaxy S24 Ultra"
    expected_keywords:
      - "Samsung"
      - "S24"
      - "Ultra"
    min_price: 800.0
    max_price: 1500.0
```

### Data Loader Pattern
Use singleton pattern with caching:
```python
from dataclasses import dataclass
import yaml

@dataclass
class ProductData:
    search_term: str
    expected_keywords: list[str]
    min_price: float
    max_price: float

_product_cache: dict[str, ProductData] | None = None

def load_product_data(product_key: str) -> ProductData:
    """Load product data from YAML with caching."""
    global _product_cache
    if _product_cache is None:
        with open("team_alpha/test_data/products.yaml") as f:
            data = yaml.safe_load(f)
        _product_cache = {
            key: ProductData(**value)
            for key, value in data["products"].items()
        }
    return _product_cache[product_key]
```

---

## Configuration

### Environment Variables
Store in `.env` file (git-ignored):
```
HEADLESS=true
BROWSER=chromium
RECORD_VIDEO=false
WEB_BASE_URL=https://example.com
API_BASE_URL=https://api.example.com
```

### Config Singleton
Access via `Config()` class:
```python
from core.config import Config

config = Config()
base_url = config.web_base_url
is_headless = config.headless
```

---

## DO NOT

❌ **Hardcode locators** in page objects (use centralized locator classes)
❌ **Create page methods without** `@allure.step()` decorator
❌ **Forget to return** `self` from page/action methods
❌ **Use bare assertions** without descriptive messages
❌ **Add explicit waits** when auto-waiting is sufficient
❌ **Use time.sleep()** (use `page.wait_for_timeout()` if necessary)
❌ **Create new files** for utilities that belong in `core/utils/`
❌ **Mix test logic in page objects** (use Action classes)
❌ **Ignore CAPTCHA/bot detection** (always check and raise exceptions)
❌ **Skip logging** major actions in page/action methods

---

## Quick Reference

### Creating a New Page Object
```python
from core.base.page_base import BasePage
from playwright.sync_api import Page
from team_alpha.locators.locators import NewPageLocators
import allure
from core.utils.logger import log

class NewPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "https://..."
        self.element = page.locator(NewPageLocators.ELEMENT)

    @allure.step("Perform action on element")
    def perform_action(self) -> 'NewPage':
        """Perform action description."""
        log.info("Performing action")
        self.element.click()
        return self
```

### Creating a New Action Class
```python
from playwright.sync_api import Page
import allure

class NewActions:
    """Orchestrate multi-page workflow."""

    def __init__(self, page: Page, data_loader=None):
        self.page = page
        self.page1 = Page1(page)
        self.page2 = Page2(page)
        self.data_loader = data_loader
        self._context = None

    @allure.step("Execute workflow step")
    def execute_step(self) -> 'NewActions':
        self.page1.do_something()
        self.page2.do_something_else()
        return self
```

### Creating a New Test
```python
import pytest
import allure
from playwright.sync_api import Page

@pytest.mark.team_alpha
@pytest.mark.ui
@allure.feature("Feature Name")
class TestNewFeature:

    @pytest.mark.smoke
    @allure.title("Test scenario title")
    @allure.severity(allure.severity_level.NORMAL)
    def test_scenario(self, page: Page):
        """Test description."""
        actions = FeatureActions(page, load_data)
        (actions
            .step_one()
            .step_two()
            .verify_result())
```

---

**END OF WEB TESTING INSTRUCTIONS**
