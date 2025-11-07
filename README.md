# QA Test Automation Framework

**A scalable, multi-team test automation framework built with Python, Playwright, and pytest**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Playwright](https://img.shields.io/badge/Playwright-1.48+-green.svg)](https://playwright.dev)
[![pytest](https://img.shields.io/badge/pytest-7.4+-red.svg)](https://pytest.org)

---

## 🎯 Overview

This framework provides a complete solution for web UI and API test automation, designed to support multiple teams working independently while sharing common infrastructure.

### Key Features

✅ **Multi-Team Support** - Independent test suites for different teams
✅ **Web & API Testing** - Comprehensive coverage for both UI and API
✅ **Page Object Model** - Maintainable UI test structure
✅ **YAML Test Data** - Type-safe data management
✅ **Parallel Execution** - Fast test runs with pytest-xdist
✅ **Rich Reporting** - Allure reports with screenshots and videos
✅ **CI/CD Ready** - GitLab CI integration included

---

## 🚀 Quick Start

### Mac/Linux
```bash
# 1. Install dependencies
make install

# 2. Run tests (Team Alpha)
make test-all

# 3. View reports
make allure-serve
```

### Windows (or Cross-Platform)
```bash
# 1. Install dependencies
poetry install
poetry run playwright install chromium

# 2. Run tests (Team Alpha)
poetry run alpha-test-all

# 3. View reports
make allure-serve  # If make available, or manually run allure
```

---

## 🖥️ Cross-Platform Commands

This framework supports **two methods** for running commands:

| Task | Makefile (Mac/Linux) | Poetry Scripts (Windows/All) |
|------|---------------------|------------------------------|
| Format code | `make format` | `poetry run format` |
| Run Team Alpha tests | `make test-all` | `poetry run alpha-test-all` |
| Run Team Beta tests | N/A | `poetry run beta-test-all` |
| Install hooks | `make install-hooks` | `poetry run install-hooks` |
| PR ready check | `make pr-ready` | `poetry run pr-ready` |
| List commands | `make help` | `poetry run list-commands` |

**Both methods do the same thing** - Poetry scripts are provided for Windows users who don't have `make` installed.

### Team-Specific Commands

The framework now supports **explicit team-prefixed commands** to run tests for specific teams:

```bash
# Team Alpha
poetry run alpha-test-all         # Run all tests for Team Alpha
poetry run alpha-test-api         # Run API tests for Team Alpha
poetry run alpha-test-web         # Run web tests for Team Alpha

# Team Beta
poetry run beta-test-all          # Run all tests for Team Beta
poetry run beta-test-api          # Run API tests for Team Beta
poetry run beta-test-web          # Run web tests for Team Beta

# Team Gamma
poetry run gamma-test-all         # Run all tests for Team Gamma
poetry run gamma-test-api         # Run API tests for Team Gamma
poetry run gamma-test-web         # Run web tests for Team Gamma
```

**Available Team-Specific Commands:**
- `{team}-test-all` - Run all tests for the team
- `{team}-test-api` - Run API tests only
- `{team}-test-web` - Run web tests (headless)
- `{team}-test-web-headed` - Run web tests with visible browser
- `{team}-test-smoke` - Run smoke tests only
- `{team}-test-api-parallel` - Run API tests in parallel
- `{team}-test-web-parallel` - Run web tests in parallel
- `{team}-test-smoke-parallel` - Run smoke tests in parallel

To see all available commands, run:
```bash
poetry run list-commands
```

---

## 📚 Documentation

This project includes comprehensive documentation:

| Document | Purpose | Audience |
|----------|---------|----------|
| **[PROJECT_GUIDE.md](./PROJECT_GUIDE.md)** | Complete project guide with detailed explanations of every component | All users |
| **[QUICK_REFERENCE.md](./QUICK_REFERENCE.md)** | Fast lookup for common tasks, code patterns, and commands | Daily users |
| **[ARCHITECTURE.md](./ARCHITECTURE.md)** | Visual architecture diagrams and data flow explanations | Architects & developers |
| **[CONTRIBUTING.md](./CONTRIBUTING.md)** | How to contribute, coding standards, and development workflow | Contributors |
| **[PULL_REQUEST_GUIDELINES.md](./PULL_REQUEST_GUIDELINES.md)** | Detailed PR requirements, checklist, and review standards | Contributors & reviewers |
| **[README.md](./README.md)** | This file - overview and quick start | New users |

### Where to Start?

- **New to the project?** → Start with [PROJECT_GUIDE.md](./PROJECT_GUIDE.md)
- **Need quick answers?** → Check [QUICK_REFERENCE.md](./QUICK_REFERENCE.md)
- **Understanding design?** → Read [ARCHITECTURE.md](./ARCHITECTURE.md)
- **Contributing code?** → Read [CONTRIBUTING.md](./CONTRIBUTING.md)
- **Submitting a PR?** → Follow [PULL_REQUEST_GUIDELINES.md](./PULL_REQUEST_GUIDELINES.md)
- **Writing tests?** → See examples in `team_alpha/tests/`

---

## 📁 Project Structure

```
ppMonoRepo/
├── core/                   # Core framework (reusable)
│   ├── base/              # Base classes
│   ├── data/              # Data management utilities
│   └── utils/             # Utility functions
│
├── team_alpha/            # Team Alpha implementation
│   ├── locators/          # Centralized selectors
│   ├── pages/             # Page Object Models
│   ├── api_clients/       # API clients
│   ├── test_data/         # Test data (YAML)
│   └── tests/             # Test cases
│       ├── api/           # API tests (9 tests)
│       └── web/           # Web tests (3 tests)
│
├── team_beta/             # Placeholder for Team Beta
├── team_gamma/            # Placeholder for Team Gamma
│
└── 📄 Documentation
    ├── PROJECT_GUIDE.md   # Complete guide
    ├── QUICK_REFERENCE.md # Quick lookup
    └── ARCHITECTURE.md    # Architecture diagrams
```

---

## 🧪 Running Tests

### Using Makefile (Recommended)

```bash
make test-all          # Run all tests
make test-api          # API tests only
make test-web          # Web tests only
make test-smoke        # Smoke tests
make allure-serve      # Generate and view report
```

### Using pytest Directly

```bash
# All tests
poetry run pytest

# Specific team
poetry run pytest team_alpha/

# By marker
poetry run pytest -m smoke
poetry run pytest -m "api and team_alpha"

# Parallel execution
poetry run pytest -n auto

# With different browser
BROWSER=firefox poetry run pytest
```

### Environment Control

```bash
# Headless mode
HEADLESS=true poetry run pytest

# Video recording
RECORD_VIDEO=true poetry run pytest

# Different environment
ENV=staging poetry run pytest
```

---

## 🎨 Example Test

### Web UI Test
```python
@pytest.mark.smoke
@allure.feature("Google Shopping")
def test_product_search(page):
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

### API Test
```python
@pytest.mark.api
@allure.feature("User API")
def test_get_users(api_request_context):
    # Initialize API client
    client = ReqResApiClient(api_request_context)

    # Make request
    response = client.get_users(page=2)

    # Verify
    assert response.ok
    body = response.json()
    assert body["page"] == 2
```

---

## 🏗️ Architecture Highlights

### Layered Architecture
```
Tests → Page Objects/API Clients → Core Framework → Playwright/pytest
```

### Design Patterns
- **Page Object Model (POM)** - Separation of test logic and page structure
- **Singleton Pattern** - Configuration, data loaders
- **Factory Pattern** - Base classes for extension
- **Repository Pattern** - YAML data management

### Key Components
- **BasePage** - Common page operations
- **BaseApiClient** - HTTP methods with logging
- **BaseYamlDataLoader** - Generic YAML loading
- **Core Utilities** - String, wait, element helpers

---

## 🔧 Technology Stack

| Category | Technology |
|----------|-----------|
| **Language** | Python 3.9+ |
| **Browser Automation** | Playwright |
| **Test Framework** | pytest |
| **Dependency Management** | Poetry |
| **Reporting** | Allure |
| **Logging** | Loguru |
| **Test Data** | YAML with PyYAML |
| **CI/CD** | GitLab CI |

---

## 📊 Test Coverage

### Team Alpha (Reference Implementation)

| Test Type | Count | Location |
|-----------|-------|----------|
| **API Tests** | 9 | `team_alpha/tests/api/` |
| **Web Tests** | 3 | `team_alpha/tests/web/` |
| **Total** | **12** | - |

### Test Categories
- ✅ User CRUD operations
- ✅ Authentication flows
- ✅ E-commerce product search
- ✅ Price extraction and validation

---

## 🛠️ Configuration

### Environment Variables (.env)

```env
# Environment
ENV=local

# URLs
WEB_BASE_URL=https://www.google.com
API_BASE_URL=https://reqres.in

# Authentication
API_AUTH_TOKEN=reqres-free-v1

# Browser Settings
HEADLESS=false
BROWSER=chromium
RECORD_VIDEO=true

# Execution
PYTEST_WORKERS=auto
```

---

## 📈 Adding New Tests

### 1. Create Page Object
```python
# team_alpha/pages/my_page.py
from core.base.page_base import BasePage

class MyPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def my_action(self):
        # Implementation
        pass
```

### 2. Add Locators
```python
# team_alpha/locators/locators.py
class MyPageLocators:
    BUTTON = '#submit-button'
    INPUT = 'input[name="username"]'
```

### 3. Create Test Data
```yaml
# team_alpha/test_data/my_data.yaml
test_cases:
  case1:
    input: "test"
    expected: "success"
```

### 4. Write Test
```python
# team_alpha/tests/web/test_my_feature.py
@pytest.mark.team_alpha
def test_my_feature(page):
    my_page = MyPage(page)
    my_page.my_action()
    assert True
```

---

## 🆕 Onboarding New Teams

1. **Copy Structure**
   ```bash
   cp -r team_alpha team_beta
   ```

2. **Update Conftest**
   - Modify `team_beta/conftest.py`
   - Add team-specific fixtures

3. **Create Tests**
   - Add page objects
   - Create locators
   - Write test data
   - Implement tests

4. **Update Configuration**
   - Add markers to `pytest.ini`
   - Add commands to `Makefile`
   - Update CI/CD pipeline

See [PROJECT_GUIDE.md](./PROJECT_GUIDE.md#adding-new-teams) for detailed steps.

---

## 📊 Reporting

### Allure Reports

```bash
# Generate and open
make allure-serve

# Generate only
make allure-report

# View existing
cd allure-report && python -m http.server 8000
```

### Report Features
- ✅ Test execution timeline
- ✅ Screenshots on failure
- ✅ Video recordings
- ✅ Step-by-step execution
- ✅ Historical trends
- ✅ Test categorization

---

## 🐛 Debugging

### Enable Playwright Inspector
```bash
PWDEBUG=1 poetry run pytest tests/test_file.py
```

### View Logs
```bash
tail -f logs/test_run_$(date +%Y-%m-%d).log
```

### Pause Execution
```python
page.pause()  # Opens Playwright Inspector
```

---

## 🤝 Contributing

### Code Style
- Follow PEP 8
- Use type hints
- Add docstrings
- Write descriptive test names

### Best Practices
- Keep tests independent
- Use fixtures for setup
- Centralize locators
- Use YAML for test data
- Add Allure annotations

### Before Committing
```bash
# Run tests
make test-all

# Check logs
tail logs/test_run_*.log

# Generate report
make allure-report
```

---

## 📞 Support

### Documentation
1. **[PROJECT_GUIDE.md](./PROJECT_GUIDE.md)** - Comprehensive guide
2. **[QUICK_REFERENCE.md](./QUICK_REFERENCE.md)** - Quick answers
3. **[ARCHITECTURE.md](./ARCHITECTURE.md)** - Design details
4. Inline code documentation (docstrings)

### Resources
- [Playwright Python Docs](https://playwright.dev/python/)
- [pytest Documentation](https://docs.pytest.org/)
- [Allure Documentation](https://docs.qameta.io/allure/)
- [Poetry Documentation](https://python-poetry.org/docs/)

---

## 📋 Current Status

### ✅ Implemented
- Core framework with base classes
- Reusable utilities (string, wait, element)
- Generic YAML data loader
- Team Alpha with 12 tests (9 API + 3 Web)
- Allure reporting
- Video recording
- Parallel execution
- CI/CD pipeline
- Comprehensive documentation

### 🚧 Placeholder
- Team Beta (ready for onboarding)
- Team Gamma (ready for onboarding)

### 📈 Metrics
- **Total Tests**: 12
- **Test Success Rate**: 100% (excluding Google CAPTCHA)
- **Code Coverage**: Core framework
- **Documentation**: 4 comprehensive guides

---

## 📄 License

Internal use only - [Company Name]

---

## 🙏 Acknowledgments

Built with:
- [Playwright](https://playwright.dev/) - Browser automation
- [pytest](https://pytest.org/) - Test framework
- [Allure](https://docs.qameta.io/allure/) - Test reporting
- [Poetry](https://python-poetry.org/) - Dependency management
- [Loguru](https://loguru.readthedocs.io/) - Logging

---

**Last Updated**: 2025-10-17 | **Version**: 1.0.0

**Need Help?** Check [PROJECT_GUIDE.md](./PROJECT_GUIDE.md) for detailed information.
