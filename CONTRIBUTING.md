# Contributing to QA Automation Framework

Thank you for contributing! This document provides quick guidelines for contributing to this project.

## 🚀 Quick Start

### Before You Start
1. Read [PULL_REQUEST_GUIDELINES.md](PULL_REQUEST_GUIDELINES.md) for detailed PR requirements
2. Review [ARCHITECTURE.md](ARCHITECTURE.md) to understand the project structure
3. Check [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for common commands

### Development Setup
```bash
# Install dependencies
make install                    # Mac/Linux
poetry run python -m poetry install  # Windows alternative

# Install pre-commit hooks (optional but recommended)
make install-hooks              # Mac/Linux
poetry run install-hooks        # Windows/Cross-platform

# Verify setup
make test-all                   # Mac/Linux
poetry run alpha-test-all       # Windows/Cross-platform
```

### 🖥️ Cross-Platform Commands

This project supports **two methods** for running commands:

**Method 1: Makefile** (Mac/Linux, requires `make`)
```bash
make format
make test-all
make pr-ready
```

**Method 2: Poetry Scripts** (Windows/Mac/Linux, no `make` required)
```bash
poetry run format
poetry run alpha-test-all  # Or beta-test-all, gamma-test-all
poetry run pr-ready
```

Both methods do the same thing - choose what works for your platform!

#### Team-Specific Commands

Poetry scripts also support **team-prefixed commands** for running tests for specific teams:

```bash
# Team Alpha
poetry run alpha-test-all         # Run all tests for Team Alpha
poetry run alpha-test-api         # Run API tests only
poetry run alpha-test-web         # Run web tests (headless)

# Team Beta
poetry run beta-test-all          # Run all tests for Team Beta
poetry run beta-test-api          # Run API tests only
poetry run beta-test-web         # Run web tests (headless)

# Team Gamma
poetry run gamma-test-all         # Run all tests for Team Gamma
poetry run gamma-test-api          # Run API tests only
poetry run gamma-test-web         # Run web tests (headless)
```

Available team-specific commands: `{team}-test-all`, `{team}-test-api`, `{team}-test-web`, `{team}-test-web-headed`, `{team}-test-smoke`, `{team}-test-api-parallel`, `{team}-test-web-parallel`, `{team}-test-smoke-parallel`

To see all available commands: `poetry run list-commands`

## 📋 Before Submitting a PR

### Run All Checks

**Using Makefile (Mac/Linux):**
```bash
make pr-ready         # Comprehensive PR check (format + tests)

# Or run individual checks:
make format           # Format code (isort → black → ruff → validate-yaml)
make lint             # Check for linting issues
make validate-yaml    # Validate YAML files
make test-all         # Run all tests
```

**Using Poetry Scripts (Windows/Mac/Linux):**
```bash
poetry run pr-ready           # Comprehensive PR check (format + tests)

# Or run individual checks:
poetry run format             # Format code (isort → black → ruff → validate-yaml)
poetry run lint               # Check for linting issues
poetry run validate-yaml      # Validate YAML files
poetry run alpha-test-all     # Run all tests for Team Alpha
poetry run list-commands      # List all available commands
```

### Pre-Commit Hooks (Optional but Recommended)
Install pre-commit hooks to automatically run checks before each commit:

**Using Makefile:**
```bash
make install-hooks
```

**Using Poetry Scripts (recommended for Windows):**
```bash
poetry run install-hooks
```

This will automatically check on every commit:
- Import sorting (isort)
- Code formatting (Black)
- Linting with auto-fix (Ruff)
- YAML validation (syntax, duplicates, indentation)
- Security checks (detect private keys, large files)
- File hygiene (trailing whitespace, end-of-file)

## ✅ PR Checklist

### Must Have
- [ ] Code formatted with Black and isort
- [ ] All linting issues resolved
- [ ] All tests passing
- [ ] New tests added for new features
- [ ] Type hints on all functions
- [ ] Docstrings for public methods

### Architecture Compliance
- [ ] Page objects extend `BasePage`
- [ ] API clients extend `BaseApiClient`
- [ ] Locators centralized in `locators/locators.py`
- [ ] Method chaining implemented (`return self`)
- [ ] Test data in YAML files

### Security
- [ ] No `.env` file committed
- [ ] No hardcoded credentials or API keys
- [ ] No secrets in logs or print statements

### Documentation
- [ ] README updated (if needed)
- [ ] Inline comments for complex logic
- [ ] CLAUDE.md updated (if architecture changed)

## 🎯 Coding Standards

### Type Hints (Required)
```python
# ✅ Good
def search(self, query: str) -> 'GoogleSearchPage':
    return self

# ❌ Bad
def search(self, query):
    return self
```

### Python 3.9+ Compatibility
```python
# ✅ Good (Python 3.9+)
from typing import Union, Optional
def process(data: Union[str, int]) -> Optional[str]:
    pass

# ❌ Bad (Python 3.10+ only)
def process(data: str | int) -> str | None:
    pass
```

### Docstrings (Required)
```python
def extract_price_from_text(text: str) -> Optional[float]:
    """
    Extract price value from text containing currency symbols.

    Args:
        text: Text containing price (e.g., "$1,234.56")

    Returns:
        Float price value or None if no valid price found

    Examples:
        >>> extract_price_from_text("Price: $1,234.56")
        1234.56
    """
```

### Page Object Pattern
```python
class GoogleSearchPage(BasePage):
    """Google search page object."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "https://www.google.com"
        self.search_input = page.locator(GoogleSearchLocators.SEARCH_INPUT)

    def open(self) -> 'GoogleSearchPage':
        """Open Google search page."""
        self.navigate(self.url)
        return self

    def search(self, query: str) -> 'GoogleSearchPage':
        """Perform search with given query."""
        self.search_input.fill(query)
        return self
```

## 🔄 Git Workflow

### Branch Naming
```bash
feature/add-firefox-support      # New features
bugfix/fix-captcha-handling      # Bug fixes
refactor/improve-data-loader     # Refactoring
docs/update-architecture-guide   # Documentation
```

### Commit Messages
```bash
# Good
git commit -m "feat: add Firefox browser support"
git commit -m "fix: correct price extraction for non-USD"
git commit -m "docs: update PR guidelines"
git commit -m "test: add edge cases for empty results"

# Bad
git commit -m "fixed stuff"
git commit -m "updates"
git commit -m "wip"
```

**Format**: `<type>: <description>`

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## 🧪 Testing Guidelines

### Test Structure (AAA Pattern)
```python
@pytest.mark.team_alpha
@pytest.mark.ui
@allure.feature("Google Shopping")
class TestGoogleShopping:

    @pytest.mark.smoke
    def test_samsung_price_check(self, page: Page):
        """Verify Samsung S24 Ultra price is displayed correctly."""
        # Arrange
        search_page = GoogleSearchPage(page)
        product_data = load_product_data("samsung_s24_ultra")

        # Act
        search_page.open().search(product_data.search_term)

        # Assert
        assert "$" in shopping_page.get_first_product_price()
```

### Test Independence
- Tests must run in any order
- No dependencies between tests
- Use fixtures for setup/teardown
- Clean up test data after execution

### Test Markers
Use appropriate pytest markers:
- `@pytest.mark.smoke` - Critical tests
- `@pytest.mark.api` - API tests
- `@pytest.mark.ui` - UI tests
- `@pytest.mark.team_alpha` - Team-specific tests

## 📁 Project Structure

```
ppMonoRepo/
├── core/                  # Shared framework components
│   ├── base/             # Base classes (BasePage, BaseApiClient)
│   ├── utils/            # Utilities (string, wait, element)
│   └── config.py         # Configuration management
│
├── team_alpha/           # Team implementation
│   ├── locators/         # Centralized selectors
│   ├── pages/            # Page Object Models
│   ├── api_clients/      # API clients
│   ├── test_data/        # YAML test data
│   └── tests/            # Test suites
│
├── scripts/              # Utility scripts
│   └── validate_yaml.py  # Custom YAML validation
│
├── .pre-commit-config.yaml  # Pre-commit hooks configuration
└── .env                     # Environment config (NEVER commit!)
```

## 🚨 Common Pitfalls to Avoid

### 1. Don't Commit Secrets
```python
# ❌ NEVER
API_KEY = "abc123"

# ✅ ALWAYS
from core.config import Config
api_key = Config().get("API_KEY")
```

### 2. Don't Duplicate Base Class Methods
```python
# ❌ Bad
class MyPage:
    def navigate_to(self, url):
        self.page.goto(url)  # Already in BasePage!

# ✅ Good
class MyPage(BasePage):
    def open(self):
        self.navigate(self.url)  # Use inherited method
        return self
```

### 3. Don't Create Test Dependencies
```python
# ❌ Bad
def test_create_user():
    global user_id
    user_id = create_user()

def test_update_user():
    update_user(user_id)  # Depends on previous test!

# ✅ Good
@pytest.fixture
def created_user():
    user_id = create_user()
    yield user_id
    cleanup_user(user_id)

def test_update_user(created_user):
    update_user(created_user)
```

### 4. Don't Use Hardcoded Waits
```python
# ❌ Bad
import time
time.sleep(5)

# ✅ Good
from core.utils.wait_utils import wait_with_retry
wait_with_retry(
    lambda: element.is_visible(),
    timeout=10
)
```

### 5. Keep Tool Versions Synchronized

**CRITICAL**: Tool versions must match between `pyproject.toml` and `.pre-commit-config.yaml`!

```toml
# ❌ Bad - Mismatched versions cause formatting inconsistencies
# pyproject.toml
[tool.poetry.group.dev.dependencies]
black = "^23.7.0"      # ← Old version

# .pre-commit-config.yaml
- repo: https://github.com/psf/black
  rev: 24.1.1          # ← New version (different formatting rules!)
```

```toml
# ✅ Good - Synchronized versions
# pyproject.toml
[tool.poetry.group.dev.dependencies]
black = "^24.1.1"
ruff = "^0.1.14"
isort = "^5.13.2"

# .pre-commit-config.yaml
- repo: https://github.com/psf/black
  rev: 24.1.1          # ← Same version!
- repo: https://github.com/astral-sh/ruff-pre-commit
  rev: v0.1.14
- repo: https://github.com/pycqa/isort
  rev: 5.13.2
```

**Why This Matters:**
- Different versions = different formatting rules
- Code formatted locally may fail pre-commit hooks
- Leads to frustrating "but I just formatted it!" moments

**When Updating Tools:**
1. Update **both files at once**
2. Run `poetry lock && poetry install`
3. Run `poetry run format` to reformat with new versions
4. Reinstall hooks: `poetry run install-hooks`
5. Commit the reformatted code

**Quick Check:**
```bash
# Update pre-commit hook versions
poetry run pre-commit autoupdate

# Then manually sync pyproject.toml to match
# Review changes before committing
```

## 📞 Getting Help

### Documentation
1. [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Common commands
2. [PROJECT_GUIDE.md](PROJECT_GUIDE.md) - Detailed explanations
3. [ARCHITECTURE.md](ARCHITECTURE.md) - Design understanding
4. [PULL_REQUEST_GUIDELINES.md](PULL_REQUEST_GUIDELINES.md) - PR requirements

### Ask Questions
- Check existing issues first
- Provide context and examples
- Include error messages and logs
- Mention what you've already tried

## 🎯 Ready to Contribute?

1. **Pick an issue** or create one for new features
2. **Create a branch** following naming conventions
3. **Implement changes** following coding standards
4. **Run checks**: `make pr-ready`
5. **Commit** with meaningful messages
6. **Push** and create PR using the template
7. **Respond** to review feedback promptly

## 🏆 Code Review Standards

All PRs require:
- ✅ At least 1 approving review
- ✅ All CI/CD checks passing
- ✅ No merge conflicts
- ✅ PR template filled out completely
- ✅ Documentation updated (if needed)

## 📝 Additional Resources

- [Playwright Documentation](https://playwright.dev/python/)
- [pytest Documentation](https://docs.pytest.org/)
- [Page Object Model Pattern](https://playwright.dev/python/docs/pom)
- [Black Code Style](https://black.readthedocs.io/)
- [Ruff Linter](https://docs.astral.sh/ruff/)

---

**Thank you for contributing!** Your efforts help make this framework better for everyone.

Questions? See [PULL_REQUEST_GUIDELINES.md](PULL_REQUEST_GUIDELINES.md) or ask in team chat.
