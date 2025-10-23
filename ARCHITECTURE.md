# Framework Architecture

**Visual representation of the test automation framework structure and data flow**

---

## 🏛️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Test Execution Layer                      │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  API Tests  │  │  Web Tests   │  │ Integration  │       │
│  │             │  │              │  │    Tests     │       │
│  └─────────────┘  └──────────────┘  └──────────────┘       │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                   Business Logic Layer                       │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ API Clients │  │ Page Objects │  │   Fixtures   │       │
│  │             │  │    (POM)     │  │              │       │
│  └─────────────┘  └──────────────┘  └──────────────┘       │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                      Data Layer                              │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  Locators   │  │  Test Data   │  │ Configuration│       │
│  │   (CSS/     │  │    (YAML)    │  │   (.env)     │       │
│  │   XPath)    │  │              │  │              │       │
│  └─────────────┘  └──────────────┘  └──────────────┘       │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                    Core Framework Layer                      │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │Base Classes │  │  Utilities   │  │   Logger     │       │
│  │(BasePage,   │  │  (String,    │  │   (Loguru)   │       │
│  │ BaseAPI)    │  │  Wait, etc)  │  │              │       │
│  └─────────────┘  └──────────────┘  └──────────────┘       │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│              Test Infrastructure Layer                       │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Playwright  │  │    pytest    │  │   Allure     │       │
│  │  (Browser   │  │  (Test       │  │  (Reporting) │       │
│  │  Automation)│  │  Framework)  │  │              │       │
│  └─────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

---

## 📂 Directory Structure Visualization

```
ppMonoRepo/
│
├── 🔧 Configuration Layer
│   ├── .env ──────────────────────► Environment variables
│   ├── pytest.ini ────────────────► Test framework config
│   ├── pyproject.toml ────────────► Dependencies
│   └── Makefile ──────────────────► Command shortcuts
│
├── 🎯 Core Framework (Reusable)
│   └── core/
│       ├── config.py ─────────────► Singleton configuration
│       ├── logger.py ─────────────► Centralized logging
│       ├── conftest.py ───────────► Global fixtures
│       │
│       ├── base/ ─────────────────► Base classes
│       │   ├── page_base.py ──────► BasePage (for all pages)
│       │   └── api_client.py ─────► BaseApiClient (for APIs)
│       │
│       ├── data/ ─────────────────► Data management
│       │   └── yaml_loader.py ────► Generic YAML loader
│       │
│       └── utils/ ────────────────► Utility functions
│           ├── string_utils.py ───► Text processing
│           ├── wait_utils.py ─────► Retry & wait logic
│           └── element_utils.py ──► Element helpers
│
└── 👥 Team Implementation (team_alpha, team_beta, team_gamma)
    └── team_alpha/
        ├── conftest.py ───────────► Team fixtures
        │
        ├── locators/ ─────────────► Centralized selectors
        │   └── locators.py ───────► All page locators
        │
        ├── pages/ ────────────────► Page Object Model
        │   ├── page1.py
        │   └── page2.py
        │
        ├── api_clients/ ──────────► API implementations
        │   └── api_client.py
        │
        ├── test_data/ ────────────► Test data management
        │   ├── data_loader.py ────► Team's data loader
        │   └── data.yaml ─────────► YAML test data
        │
        └── tests/ ────────────────► Test cases
            ├── api/
            ├── web/
            └── integration/
```

---

## 🔄 Test Execution Flow

### Web UI Test Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Test Starts                                               │
│    test_google_shopping.py::test_price_check                │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Load Test Data                                            │
│    data = load_product_data("samsung_s24_ultra")            │
│    ├─► YAML file: google_shopping.yaml                      │
│    └─► Returns: ProductData(search_term="...", price=...)   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Initialize Page Objects                                   │
│    search_page = GoogleSearchPage(page)                     │
│    shopping_page = GoogleShoppingPage(page)                 │
│    ├─► Inherits from BasePage                               │
│    └─► Loads locators from GoogleSearchLocators             │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Execute Test Steps                                        │
│    search_page.navigate()                                   │
│    ├─► Playwright: page.goto("https://www.google.com")      │
│    └─► Logging: log.info("Navigating to Google")            │
│                                                              │
│    search_page.search(data.search_term)                     │
│    ├─► Handle cookie consent (optional dialog)              │
│    ├─► Playwright: page.fill(), page.press("Enter")         │
│    └─► Wait for results                                     │
│                                                              │
│    search_page.click_shopping_tab()                         │
│    └─► Playwright: shopping_tab.click()                     │
│                                                              │
│    price = shopping_page.get_first_product_price()          │
│    ├─► Try multiple locators (fallback strategy)            │
│    ├─► Extract price using regex utility                    │
│    └─► Return: "$999.99"                                    │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Assertions                                                │
│    assert "$" in price                                       │
│    assert price >= data.min_price                           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. Reporting & Cleanup                                       │
│    ├─► Allure: Attach screenshots, logs                     │
│    ├─► Video: Save recording if enabled                     │
│    ├─► Logs: Write to logs/test_run_{date}.log              │
│    └─► Screenshot: On failure → screenshots/                │
└─────────────────────────────────────────────────────────────┘
```

### API Test Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Test Starts                                               │
│    test_reqres_api.py::test_get_users                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Initialize API Client                                     │
│    client = ReqResApiClient(api_request_context)            │
│    ├─► Inherits from BaseApiClient                          │
│    ├─► API context from fixture (with auth headers)         │
│    └─► Base URL: https://reqres.in                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Make API Request                                          │
│    response = client.get_users(page=2)                      │
│    ├─► BaseApiClient: self.get("/api/users?page=2")         │
│    ├─► Playwright: api_context.get(endpoint, headers)       │
│    ├─► Logging: log.info("GET /api/users?page=2")           │
│    └─► Returns: APIResponse object                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Validate Response                                         │
│    assert response.ok                                        │
│    body = response.json()                                    │
│    assert body["page"] == 2                                  │
│    assert len(body["data"]) > 0                              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Reporting                                                 │
│    ├─► Allure: Attach request/response                      │
│    ├─► Logs: Write API details to logs/                     │
│    └─► Status: Pass/Fail                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔗 Component Interactions

### Page Object Flow

```
Test File
   │
   ├─► Creates Page Object
   │      │
   │      ├─► Inherits from BasePage
   │      │      │
   │      │      └─► Provides common methods:
   │      │            - navigate()
   │      │            - wait_for_element()
   │      │            - take_screenshot()
   │      │            - etc.
   │      │
   │      ├─► Loads Locators
   │      │      │
   │      │      └─► From locators.py:
   │      │            GoogleSearchLocators.SEARCH_INPUT
   │      │
   │      └─► Uses Utilities
   │             │
   │             └─► From core.utils:
   │                   - handle_optional_dialog()
   │                   - safe_extract_text()
   │                   - etc.
   │
   └─► Calls Page Methods
          │
          └─► Playwright Actions:
                - page.click()
                - page.fill()
                - page.locator()
```

### Data Loading Flow

```
Test File
   │
   ├─► Calls: load_product_data("samsung")
   │
   ├─► TeamAlphaDataLoader (Singleton)
   │      │
   │      ├─► Inherits: BaseYamlDataLoader
   │      │      │
   │      │      └─► Provides:
   │      │            - get_section()
   │      │            - get_section_item()
   │      │            - Caching
   │      │            - Error handling
   │      │
   │      ├─► Loads: google_shopping.yaml
   │      │      │
   │      │      └─► YAML structure:
   │      │            products:
   │      │              samsung:
   │      │                search_term: "..."
   │      │                min_price: 800
   │      │
   │      └─► Returns: ProductData (dataclass)
   │             │
   │             └─► Type-safe data:
   │                   - search_term: str
   │                   - min_price: float
   │                   - expected_keywords: List[str]
   │
   └─► Test uses: data.search_term, data.min_price
```

### Configuration Flow

```
Application Start
   │
   ├─► Loads .env file
   │      │
   │      └─► Variables:
   │            API_BASE_URL=https://reqres.in
   │            HEADLESS=false
   │            RECORD_VIDEO=true
   │
   ├─► Config Singleton (core/config.py)
   │      │
   │      ├─► Reads environment variables
   │      ├─► Converts types (string → bool)
   │      ├─► Provides defaults
   │      │
   │      └─► Accessible anywhere:
   │            from core.config import config
   │            config.api_base_url
   │            config.headless
   │
   └─► Used by:
          ├─► Fixtures (browser launch args)
          ├─► API clients (base URL)
          ├─► Loggers (config paths)
          └─► Tests (conditional logic)
```

---

## 🎨 Design Pattern Implementation

### Singleton Pattern

```python
# core/config.py
class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

# Usage: Always same instance
config1 = Config()
config2 = Config()
# config1 is config2 → True
```

### Page Object Model (POM)

```python
# Structure
BasePage (core/base/page_base.py)
    ↑
    │ inherits
    │
GoogleSearchPage (team_alpha/pages/google_search_page.py)
    ↑
    │ uses
    │
GoogleSearchLocators (team_alpha/locators/locators.py)

# Benefits
- Separation of concerns
- Reusability
- Maintainability
- Single source of truth for locators
```

### Repository Pattern

```python
# Data Layer
YAML File (google_shopping.yaml)
    ↓ loaded by
BaseYamlDataLoader (core/data/yaml_loader.py)
    ↓ extended by
TeamAlphaDataLoader (team_alpha/test_data/data_loader.py)
    ↓ used by
Tests (team_alpha/tests/)

# Benefits
- Centralized data access
- Type safety with data classes
- Easy to change data source
- Caching for performance
```

### Factory Pattern

```python
# Base Classes
BasePage          → Creates concrete page objects
BaseApiClient     → Creates concrete API clients
BaseYamlDataLoader → Creates concrete data loaders

# Each team creates their own implementations
team_alpha → GoogleSearchPage (from BasePage)
team_beta  → MyPage (from BasePage)
```

---

## 🚀 Execution Pipeline

### Local Execution

```
Developer runs: make test-web
   │
   ├─► Makefile
   │      │
   │      └─► poetry run pytest team_alpha/tests/web/ -v
   │
   ├─► pytest
   │      │
   │      ├─► Discovers tests
   │      ├─► Loads fixtures from conftest.py files
   │      ├─► Sets up browser/API contexts
   │      │
   │      └─► Runs tests
   │             │
   │             ├─► Executes test methods
   │             ├─► Captures logs (Loguru)
   │             ├─► Takes screenshots on failure
   │             ├─► Records videos if enabled
   │             │
   │             └─► Generates Allure results
   │
   └─► Results
          │
          ├─► Console output (pytest -v)
          ├─► Logs: logs/test_run_{date}.log
          ├─► Screenshots: screenshots/
          ├─► Videos: videos/
          └─► Allure: allure-results/
```

### CI/CD Execution (GitLab)

```
Git push
   │
   ├─► GitLab CI triggered (.gitlab-ci.yml)
   │
   ├─► Stage 1: Install
   │      │
   │      ├─► poetry install
   │      └─► poetry run playwright install
   │
   ├─► Stage 2: Test
   │      │
   │      ├─► make test-all
   │      ├─► HEADLESS=true (CI mode)
   │      ├─► RECORD_VIDEO=false (save space)
   │      │
   │      └─► Generates artifacts:
   │            - allure-results/
   │            - logs/
   │            - screenshots/
   │
   └─► Stage 3: Report
          │
          ├─► Allure report generation
          ├─► Upload artifacts
          └─► Notification (Slack/Email)
```

---

## 📊 Data Flow Diagram

```
┌──────────────┐
│  .env File   │
│              │
│ API_BASE_URL │
│ HEADLESS     │
│ BROWSER      │
└──────┬───────┘
       │
       ▼
┌──────────────┐       ┌──────────────┐
│Config Object │──────►│ Core Fixtures│
│  (Singleton) │       │  (conftest)  │
└──────┬───────┘       └──────┬───────┘
       │                      │
       │                      ▼
       │              ┌──────────────┐
       │              │Browser Setup │
       │              │API Context   │
       │              └──────┬───────┘
       │                      │
       ▼                      ▼
┌──────────────┐       ┌──────────────┐
│  Test Data   │       │  Page Objects│
│  (YAML)      │◄──────│  API Clients │
│              │       │              │
└──────┬───────┘       └──────┬───────┘
       │                      │
       └───────────┬──────────┘
                   │
                   ▼
           ┌──────────────┐
           │  Test Cases  │
           │              │
           └──────┬───────┘
                  │
                  ▼
         ┌────────────────┐
         │   Test Results │
         │                │
         │ - Logs         │
         │ - Screenshots  │
         │ - Videos       │
         │ - Allure       │
         └────────────────┘
```

---

## 🔐 Security & Best Practices

### Credentials Management

```
❌ Bad: Hardcoded
username = "admin"
password = "admin123"

✅ Good: Environment Variables
username = os.getenv("TEST_USERNAME")
password = os.getenv("TEST_PASSWORD")

✅ Better: .env File
# .env (gitignored)
TEST_USERNAME=admin
TEST_PASSWORD=admin123

✅ Best: Secrets Manager (Production)
- AWS Secrets Manager
- HashiCorp Vault
- Azure Key Vault
```

### Test Isolation

```
Each test should:
├── ✅ Be independent
├── ✅ Have own data
├── ✅ Clean up after itself
└── ✅ Not depend on execution order

Achieved through:
├── Function-scoped fixtures
├── Separate test data per test
└── Proper teardown
```

---

## 📈 Scalability Design

### Multi-Team Support

```
Current Teams:
├── team_alpha (Active)
│   ├── 9 API tests
│   ├── 3 Web tests
│   └── Full implementation
│
├── team_beta (Placeholder)
│   └── Ready for onboarding
│
└── team_gamma (Placeholder)
    └── Ready for onboarding

Each team:
├── Independent test suite
├── Own fixtures
├── Own test data
├── Own page objects
└── Shares core framework
```

### Parallel Execution

```
Sequential (slow):
Test 1 → Test 2 → Test 3 → Test 4
Total: 40 seconds

Parallel (fast):
Test 1 ┐
Test 2 ├─► Running simultaneously
Test 3 │
Test 4 ┘
Total: 10 seconds

Enable with:
pytest -n auto  # Use all CPU cores
```

---

**Architecture Documentation v1.0** | Last updated: 2025-10-17
