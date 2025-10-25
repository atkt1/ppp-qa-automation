# Claude AI - Project Context

**QA Test Automation Framework** - Multi-team test automation using Python, Playwright, and pytest

---

## 🎯 Project Overview

This is a **scalable, production-ready QA test automation framework** designed to support multiple teams working independently while sharing common infrastructure. The framework follows industry best practices with Page Object Model, data-driven testing, and comprehensive reporting.

### Current Status
- ✅ Core framework fully implemented (~3,500 lines of code)
- ✅ Team Alpha implementation complete (12 tests: 9 API + 3 Web)
- ✅ Comprehensive documentation (14 markdown files)
- ✅ Git repository initialized and pushed to GitHub
- ✅ CI/CD pipeline configured (GitLab CI)
- ✅ Parallel testing enabled with pytest-xdist
- 🚧 Team Beta & Gamma - placeholders for future teams

### Technology Stack
- **Language**: Python 3.9+
- **Web Automation**: Playwright 1.48+
- **Test Framework**: pytest 7.4+
- **Dependency Management**: Poetry
- **Reporting**: Allure Reports
- **Logging**: Loguru
- **Data Management**: YAML + dataclasses
- **CI/CD**: GitLab CI

---

## 📁 Project Structure

```
ppMonoRepo/
├── core/                      # Reusable framework components
│   ├── base/                  # Base classes (BasePage, BaseApiClient)
│   ├── data/                  # Generic YAML data loader
│   ├── utils/                 # Utilities (string, wait, element helpers)
│   ├── config.py              # Configuration singleton
│   ├── logger.py              # Loguru logging setup
│   └── conftest.py            # Core pytest fixtures
│
├── team_alpha/                # Team Alpha implementation
│   ├── locators/              # Centralized CSS/XPath selectors
│   │   └── locators.py        # GoogleSearchLocators, GoogleShoppingLocators
│   ├── pages/                 # Page Object Models
│   │   ├── google_search_page.py
│   │   └── google_shopping_page.py
│   ├── api_clients/           # API client implementations
│   │   └── reqres_api_client.py
│   ├── test_data/             # Test data management
│   │   ├── google_shopping.yaml
│   │   └── data_loader.py
│   └── tests/
│       ├── api/               # 9 API tests (ReqRes API)
│       └── web/               # 3 Web tests (Google Shopping)
│
├── team_beta/                 # Placeholder for Team Beta
├── team_gamma/                # Placeholder for Team Gamma
│
├── .env                       # Environment configuration (NOT in git)
├── pytest.ini                 # Pytest configuration
├── pyproject.toml             # Poetry dependencies
├── Makefile                   # Common commands
└── .gitlab-ci.yml             # CI/CD pipeline

Documentation:
├── README.md                  # Project overview & quick start
├── PROJECT_GUIDE.md           # Complete guide (all components explained)
├── QUICK_REFERENCE.md         # Fast lookup for daily use
├── ARCHITECTURE.md            # Visual architecture diagrams
├── PARALLEL_TESTING_GUIDE.md  # Parallel execution guide
├── MANUAL_SETUP_GUIDE.md      # Manual setup for secure environments
└── GIT_SETUP_GUIDE.md         # Git initialization guide
```

---

## 🧠 Key Architectural Decisions

### 1. Multi-Team Architecture
- Each team has isolated test suites sharing core framework
- Teams can work independently without conflicts
- Common utilities prevent code duplication

### 2. Page Object Model (POM)
- Separation of test logic from page interactions
- Centralized locators in single file per team
- Reusable page methods with method chaining

### 3. Generic Base Classes
- `BasePage`: Common page operations (navigate, click, wait, etc.)
- `BaseApiClient`: REST API operations (GET, POST, PUT, DELETE, PATCH)
- `BaseYamlDataLoader`: Singleton data loader with caching

### 4. Utility-First Approach
Core utilities used throughout:
- **String utilities**: `extract_price_from_text()`, `sanitize_text()`, etc.
- **Wait utilities**: `wait_with_retry()`, `retry_on_exception()`, etc.
- **Element utilities**: `handle_optional_dialog()`, `safe_extract_text()`, etc.

### 5. Type Safety
- Type hints throughout codebase
- Dataclasses for test data models
- Python 3.9+ compatible (Union[] instead of | operator)

---

## 🎓 Framework Patterns & Best Practices

### Page Object Pattern
```python
# Correct implementation
class GoogleSearchPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "https://www.google.com"
        self.search_input = page.locator(GoogleSearchLocators.SEARCH_INPUT)

    def open(self):
        """Open this specific page."""
        self.navigate(self.url)  # Uses parent's generic navigate()
        return self

    def search(self, query: str):
        """Page-specific action."""
        self.search_input.fill(query)
        return self  # Method chaining
```

### Data-Driven Testing
```python
# Test data in YAML
products:
  samsung_s24_ultra:
    search_term: "Samsung S24 Ultra"
    expected_min_price: 800

# Loaded via type-safe data classes
product = load_product_data("samsung_s24_ultra")
```

### Test Structure
```python
@pytest.mark.team_alpha
@pytest.mark.ui
@allure.feature("Google Shopping")
class TestGoogleShopping:
    @pytest.mark.smoke
    def test_price_check(self, page: Page):
        # Arrange
        search_page = GoogleSearchPage(page)

        # Act
        (search_page
            .open()
            .search("Samsung S24 Ultra")
            .click_shopping_tab())

        # Assert
        price = shopping_page.get_first_product_price()
        assert "$" in price
```

---

## 🔧 Common Operations

### Running Tests
```bash
# All tests
make test-all

# Specific type
make test-api          # API tests
make test-web          # Web UI tests
make test-smoke        # Smoke tests

# Parallel execution
make test-parallel     # Auto-detect CPU cores
make test-parallel-4   # 4 workers

# Single test
make test-one TEST=team_alpha/tests/web/test_google_shopping.py::TestGoogleShopping::test_samsung_s24_ultra_price_check

# Headed mode (visible browser)
make test-web-headed

# Slow motion (for debugging)
poetry run pytest --headed --slowmo 1000 team_alpha/tests/web/

# Debug mode (Playwright Inspector)
PWDEBUG=1 poetry run pytest team_alpha/tests/web/test_google_shopping.py
```

### Code Quality
```bash
make format            # Format with black + isort
make lint              # Lint with ruff
```

### Reporting
```bash
make allure-serve      # Generate and open Allure report
make allure-report     # Generate HTML report
```

---

## 🚨 Important Conventions

### 1. Method Naming
- **`open()`**: Opens a specific page (page-specific)
- **`navigate(url)`**: Generic navigation (inherited from BasePage)
- Use `open()` in page objects, not `navigate()` (avoid signature conflicts)

### 2. Locators
- All locators in `team_name/locators/locators.py`
- One file per team with multiple classes
- Class per page: `GoogleSearchLocators`, `GoogleShoppingLocators`

### 3. Test Data
- YAML files in `team_name/test_data/`
- Type-safe loading via dataclasses
- Singleton pattern for efficiency

### 4. Git Practices
- `.env` file is NEVER committed (contains secrets)
- Use meaningful commit messages
- Branch naming: `feature/description`, `bugfix/description`

### 5. Windows Compatibility
- Use `Union[Type1, Type2]` instead of `Type1 | Type2` (Python 3.9 compat)
- Handle Path objects explicitly in constructors
- Test on both platforms when possible

---

## 📝 Common Tasks Guide

### Adding a New Test
1. Create test file in `team_alpha/tests/web/` or `team_alpha/tests/api/`
2. Use appropriate markers: `@pytest.mark.team_alpha`, `@pytest.mark.ui`
3. Follow existing test patterns
4. Add test data to YAML if needed

### Adding a New Page Object
1. Create file in `team_alpha/pages/`
2. Extend `BasePage`
3. Add locators to `team_alpha/locators/locators.py`
4. Implement `open()` method
5. Use method chaining (`return self`)
6. Import and export in `__init__.py`

### Adding Utility Functions
1. Add to appropriate file in `core/utils/`
2. Export in `core/utils/__init__.py`
3. Use type hints
4. Add docstrings with examples
5. Make reusable for all teams

### Creating New Team
1. Copy `team_alpha/` structure
2. Rename to `team_beta/`
3. Update imports and class names
4. Create team-specific fixtures in `conftest.py`
5. Add to `pytest.ini` testpaths

---

## ⚠️ Known Issues & Workarounds

### 1. Google CAPTCHA Detection
**Issue**: Google may show CAPTCHA during automated testing
**Workaround**:
- Run tests less frequently
- Use different network/VPN
- Tests handle this gracefully with clear error messages

### 2. Playwright Browser Downloads
**Issue**: Corporate firewalls may block browser downloads
**Solution**:
- Configure proxy: `export HTTPS_PROXY=http://proxy:8080`
- Or copy browsers manually from `~/.cache/ms-playwright/`

### 3. Poetry in Virtual Environment
**Setup**: Poetry is installed in a venv, not globally
**Usage**: Activate company venv first, then use Poetry normally

### 4. Windows Path Issues
**Issue**: `__init__` with Path on Windows
**Fix**: Use `BaseYamlDataLoader.__init__(self, path)` instead of `super().__init__(path)`

---

## 🎯 Design Principles Followed

1. **DRY (Don't Repeat Yourself)**: Common code in `core/`, not duplicated
2. **SOLID Principles**: Single responsibility, open/closed, Liskov substitution
3. **Separation of Concerns**: Data, logic, and tests are separate
4. **Fail Fast**: Early validation and clear error messages
5. **Type Safety**: Type hints throughout for IDE support
6. **Documentation**: Every component documented
7. **Testability**: Small, focused, independent tests
8. **Maintainability**: Clear structure, consistent naming

---

## 🔍 Key Files to Understand

### Core Framework
- `core/base/page_base.py` - Base for all page objects
- `core/base/api_client.py` - Base for API clients
- `core/data/yaml_loader.py` - Generic data loader (singleton pattern)
- `core/utils/element_utils.py` - Playwright helpers
- `core/config.py` - Configuration management

### Team Alpha
- `team_alpha/pages/google_search_page.py` - Example page object
- `team_alpha/locators/locators.py` - Centralized locators
- `team_alpha/test_data/data_loader.py` - Team-specific data loader
- `team_alpha/tests/web/test_google_shopping.py` - Example web tests
- `team_alpha/tests/api/test_reqres_users.py` - Example API tests

### Configuration
- `pytest.ini` - Pytest settings, markers, logging
- `pyproject.toml` - Dependencies and tool configurations
- `.env` - Environment variables (NOT in git)
- `Makefile` - Common commands
- `.gitlab-ci.yml` - CI/CD pipeline

---

## 💡 When Helping with This Project

### Things to Remember
1. **Never commit `.env` file** - it contains secrets
2. **Use `open()` not `navigate()` in page objects** - avoid method conflicts
3. **Test independence** - tests should run in any order
4. **Type hints** - use `Union[]` for Python 3.9 compatibility
5. **Method chaining** - return `self` from page methods
6. **Documentation** - update relevant .md files when changing structure

### Preferred Solutions
- ✅ Extend existing base classes
- ✅ Use existing utilities before creating new ones
- ✅ Follow team_alpha patterns for consistency
- ✅ Add type hints and docstrings
- ✅ Update documentation when adding features

### Avoid
- ❌ Duplicating code across teams
- ❌ Hardcoding URLs/credentials (use .env)
- ❌ Creating dependencies between tests
- ❌ Using Python 3.10+ syntax (|, match/case)
- ❌ Committing sensitive data

---

## 📊 Test Coverage

**Current Status** (as of last run):
- **Total Tests**: 12
  - API Tests: 9 (ReqRes CRUD operations)
  - Web Tests: 3 (Google Shopping price extraction)
- **Test Execution**: ~30 seconds (sequential), ~10 seconds (parallel)
- **Pass Rate**: 100% (when Google CAPTCHA doesn't trigger)

**Markers**:
- `@pytest.mark.smoke` - Critical tests (3 tests)
- `@pytest.mark.team_alpha` - Team Alpha tests (12 tests)
- `@pytest.mark.api` - API tests (9 tests)
- `@pytest.mark.ui` - UI tests (3 tests)

---

## 🚀 Future Enhancements Planned

- [ ] Team Beta implementation (example: different application)
- [ ] Team Gamma implementation (example: mobile testing)
- [ ] Screenshot comparison testing
- [ ] Database validation utilities
- [ ] Performance testing integration
- [ ] Visual regression testing
- [ ] Docker containerization
- [ ] GitHub Actions CI/CD
- [ ] Test data factories with Faker
- [ ] Cross-browser testing (Firefox, Safari)

---

## 📞 Getting Help

**Documentation Priority**:
1. Check [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for common tasks
2. Read [PROJECT_GUIDE.md](PROJECT_GUIDE.md) for detailed explanations
3. Review [ARCHITECTURE.md](ARCHITECTURE.md) for design understanding
4. Look at existing tests in `team_alpha/tests/` for examples

**For Specific Topics**:
- Parallel testing → [PARALLEL_TESTING_GUIDE.md](PARALLEL_TESTING_GUIDE.md)
- Manual setup → [MANUAL_SETUP_GUIDE.md](MANUAL_SETUP_GUIDE.md)
- Git workflow → [GIT_SETUP_GUIDE.md](GIT_SETUP_GUIDE.md)

---

## 🎓 Learning Resources

**Framework Concepts**:
- [Playwright Documentation](https://playwright.dev/python/)
- [pytest Documentation](https://docs.pytest.org/)
- [Page Object Model Pattern](https://playwright.dev/python/docs/pom)
- [Allure Reports](https://docs.qameta.io/allure/)

**Project-Specific**:
- All documentation in root directory (14 .md files)
- Code examples in `team_alpha/`
- Test patterns in `team_alpha/tests/`

---

## 🏆 Success Criteria

This project is considered successful when:
- ✅ Tests are reliable and maintainable
- ✅ New team members can onboard quickly using documentation
- ✅ Adding new tests is straightforward
- ✅ Tests run fast (parallel execution)
- ✅ Reports are clear and actionable
- ✅ CI/CD pipeline is stable
- ✅ Multiple teams can work independently

---

**Last Updated**: 2025-10-23
**Project Version**: 0.1.0
**Python Version**: 3.9+
**Framework Status**: Production-Ready
**Total LOC**: ~3,500 lines
