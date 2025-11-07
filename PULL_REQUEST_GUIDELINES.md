# Pull Request / Merge Request Guidelines

## 📋 PR Checklist

Before submitting your PR, ensure ALL items below are checked:

### 🔧 Code Quality & Formatting

- [ ] **Black formatting applied**: Run `make format` or `poetry run black .`
- [ ] **isort imports organized**: Imports sorted correctly (included in `make format`)
- [ ] **Ruff linting passed**: Run `make lint` with zero errors
- [ ] **Type hints added**: All functions have proper type annotations
- [ ] **Docstrings present**: All public methods/classes documented
- [ ] **No commented-out code**: Remove dead code before submitting
- [ ] **Python 3.9+ compatible**: No `|` type unions, no `match/case` statements

### ✅ Testing Requirements

- [ ] **All tests passing**: Run `make test-all` successfully
- [ ] **New tests added**: New features include corresponding tests
- [ ] **Test independence verified**: Tests pass when run in isolation and in parallel
- [ ] **Appropriate markers used**: `@pytest.mark.smoke`, `@pytest.mark.api`, etc.
- [ ] **No hardcoded data**: Test data in YAML files or fixtures
- [ ] **Allure annotations added**: `@allure.feature()`, `@allure.story()`, `@allure.title()`

### 📁 Project Structure Compliance

- [ ] **Locators centralized**: All selectors in `team_name/locators/locators.py`
- [ ] **Page objects extend BasePage**: Proper inheritance used
- [ ] **API clients extend BaseApiClient**: Proper inheritance used
- [ ] **Method chaining implemented**: Page methods return `self`
- [ ] **Use `open()` not `navigate()`**: Page-specific `open()` method implemented
- [ ] **Files in correct directories**: Follow team_alpha structure
- [ ] **Proper imports/exports**: Updated `__init__.py` files

### 🔒 Security & Configuration

- [ ] **No secrets committed**: `.env` file never included in commits
- [ ] **No hardcoded credentials**: Use environment variables via `core.config`
- [ ] **No API keys in code**: All sensitive data in `.env`
- [ ] **`.gitignore` updated**: New file types added if needed
- [ ] **Secrets not in logs**: No sensitive data in print/log statements

### 📝 Documentation

- [ ] **README.md updated**: If adding major features
- [ ] **QUICK_REFERENCE.md updated**: If adding common commands
- [ ] **Inline comments added**: Complex logic explained
- [ ] **CLAUDE.md updated**: If changing architecture or conventions
- [ ] **Docstrings include examples**: Complex functions have usage examples

### 🧪 YAML & Data Validation

- [ ] **YAML syntax valid**: Run `poetry run python -c "import yaml; yaml.safe_load(open('path/to/file.yaml'))"`
- [ ] **Dataclasses match YAML**: Type-safe data models updated
- [ ] **No duplicate keys**: YAML files validated for duplicates
- [ ] **Consistent formatting**: 2-space indentation in YAML files

---

## 🎯 PR Description Template

```markdown
## Summary
Brief description of what this PR does (2-3 sentences)

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Refactoring (code improvement without functionality change)
- [ ] Documentation update
- [ ] Configuration/CI change

## Changes Made
- Bullet point list of specific changes
- What was added/modified/removed
- Why these changes were necessary

## Testing Performed
- [ ] All existing tests pass
- [ ] Added X new tests covering:
  - Specific scenario 1
  - Specific scenario 2
- [ ] Manually tested: [describe manual testing if applicable]
- [ ] Tested in parallel mode: `make test-parallel`

## Screenshots/Videos (if UI changes)
[Add screenshots or video recordings for UI-related changes]

## Related Issues
Closes #123
Related to #456

## Additional Notes
Any additional context, dependencies, or breaking changes reviewers should know about
```

---

## 🔍 Code Review Checklist for Reviewers

### Architecture & Design
- [ ] Follows existing patterns (POM, base classes, utilities)
- [ ] No code duplication (uses core utilities)
- [ ] Single Responsibility Principle followed
- [ ] Proper separation of concerns (locators, data, logic)
- [ ] No tight coupling between teams

### Code Quality
- [ ] Code is readable and self-documenting
- [ ] Variable/function names are descriptive
- [ ] No magic numbers/strings (use constants or config)
- [ ] Error handling is appropriate
- [ ] No unnecessary complexity

### Testing
- [ ] Tests are meaningful and test behavior, not implementation
- [ ] Tests follow AAA pattern (Arrange, Act, Assert)
- [ ] No flaky tests (deterministic, no race conditions)
- [ ] Test data is realistic and representative
- [ ] Edge cases are covered

### Performance
- [ ] No unnecessary waits or sleeps
- [ ] Efficient use of locators (no repeated lookups)
- [ ] Data loading uses singleton pattern
- [ ] No memory leaks (proper cleanup in fixtures)

---

## 🚨 Automated Validation Commands

Run these commands before submitting your PR:

```bash
# 1. Format code
make format

# 2. Lint code
make lint

# 3. Run all tests
make test-all

# 4. Run tests in parallel (catch race conditions)
make test-parallel

# 5. Validate YAML files
make validate-yaml  # If this target exists, otherwise:
poetry run python -c "import yaml, sys; [yaml.safe_load(open(f)) for f in sys.argv[1:]]" team_alpha/test_data/*.yaml

# 6. Type check (if using mypy)
# poetry run mypy core/ team_alpha/
```

---

## 📏 Coding Standards

### 1. Type Hints
**Required** for all functions, methods, and class attributes:

```python
# ✅ Good
def search(self, query: str) -> 'GoogleSearchPage':
    self.search_input.fill(query)
    return self

# ❌ Bad
def search(self, query):
    self.search_input.fill(query)
    return self
```

**Python 3.9 Compatibility**:
```python
# ✅ Good (Python 3.9+)
from typing import Union, Optional, List, Dict
def process(data: Union[str, int]) -> Optional[List[Dict[str, str]]]:
    pass

# ❌ Bad (Python 3.10+ only)
def process(data: str | int) -> list[dict[str, str]] | None:
    pass
```

### 2. Docstrings
**Required** for all public classes and methods:

```python
def extract_price_from_text(text: str) -> Optional[float]:
    """
    Extract price value from text containing currency symbols.

    Args:
        text: Text containing price (e.g., "$1,234.56" or "£999.99")

    Returns:
        Float price value or None if no valid price found

    Examples:
        >>> extract_price_from_text("Price: $1,234.56")
        1234.56
        >>> extract_price_from_text("No price here")
        None
    """
```

### 3. Method Chaining in Page Objects
**Always return `self`** for fluent interface:

```python
# ✅ Good
class GoogleSearchPage(BasePage):
    def open(self) -> 'GoogleSearchPage':
        self.navigate(self.url)
        return self

    def search(self, query: str) -> 'GoogleSearchPage':
        self.search_input.fill(query)
        return self

# Usage: search_page.open().search("test").click_shopping_tab()
```

### 4. Locators
**Centralized in single file** per team:

```python
# ✅ Good - team_alpha/locators/locators.py
class GoogleSearchLocators:
    SEARCH_INPUT = "textarea[name='q']"
    SEARCH_BUTTON = "input[value='Google Search']"

class GoogleShoppingLocators:
    PRODUCT_CARD = ".sh-dgr__gr-auto"
    PRODUCT_PRICE = ".a8Pemb"

# ❌ Bad - scattered throughout page objects
class GoogleSearchPage:
    def search(self, query):
        self.page.locator("textarea[name='q']").fill(query)  # Don't do this
```

### 5. Test Structure
**Follow AAA pattern** (Arrange, Act, Assert):

```python
@pytest.mark.team_alpha
@pytest.mark.ui
@pytest.mark.smoke
@allure.feature("Google Shopping")
@allure.story("Product Price Validation")
class TestGoogleShopping:

    def test_samsung_price_check(self, page: Page):
        """Verify Samsung S24 Ultra price is displayed correctly."""
        # Arrange
        search_page = GoogleSearchPage(page)
        product_data = load_product_data("samsung_s24_ultra")

        # Act
        search_page.open().search(product_data.search_term).click_shopping_tab()
        shopping_page = GoogleShoppingPage(page)
        price = shopping_page.get_first_product_price()

        # Assert
        assert "$" in price, f"Expected price to contain $, got: {price}"
        price_value = extract_price_from_text(price)
        assert price_value >= product_data.expected_min_price
```

### 6. YAML Data Files
**Consistent formatting**:

```yaml
# ✅ Good - 2-space indentation, consistent structure
products:
  samsung_s24_ultra:
    search_term: "Samsung S24 Ultra"
    expected_min_price: 800
    expected_max_price: 1500

  iphone_15_pro:
    search_term: "iPhone 15 Pro"
    expected_min_price: 999
    expected_max_price: 1599

# ❌ Bad - inconsistent indentation, mixed styles
products:
    samsung_s24_ultra:
      search_term: "Samsung S24 Ultra"
      expected_min_price: 800
  iphone_15_pro:
        search_term: "iPhone 15 Pro"
```

### 7. Imports Organization (isort)
**Automatic with `make format`**, but should follow:

```python
# 1. Standard library
import os
from typing import Optional, Union, List

# 2. Third-party
import pytest
import allure
from playwright.sync_api import Page, Locator

# 3. Local imports
from core.base.page_base import BasePage
from core.utils.string_utils import extract_price_from_text
from team_alpha.locators.locators import GoogleSearchLocators
```

---

## 🔄 Git Workflow

### Branch Naming
```bash
# Features
feature/add-firefox-support
feature/team-beta-implementation

# Bug fixes
bugfix/fix-captcha-handling
bugfix/correct-price-extraction

# Refactoring
refactor/extract-common-utilities
refactor/improve-data-loader

# Documentation
docs/update-architecture-guide
docs/add-pr-guidelines
```

### Commit Messages
```bash
# ✅ Good - clear, specific, follows convention
git commit -m "feat: add Firefox browser support for parallel testing"
git commit -m "fix: correct price extraction regex for non-USD currencies"
git commit -m "docs: update QUICK_REFERENCE with new Makefile targets"
git commit -m "refactor: extract retry logic to wait_utils module"
git commit -m "test: add edge case tests for empty shopping results"

# ❌ Bad - vague, no context
git commit -m "fixed stuff"
git commit -m "updates"
git commit -m "wip"
```

**Commit Message Format**:
```
<type>: <subject>

[optional body]

[optional footer]
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

---

## 🚫 Common Pitfalls to Avoid

### 1. Committing Secrets
```python
# ❌ NEVER do this
API_KEY = "abc123xyz789"
username = "admin@example.com"

# ✅ Always use environment variables
from core.config import Config
api_key = Config().get("API_KEY")
```

### 2. Duplicating Base Class Methods
```python
# ❌ Bad - duplicating BasePage functionality
class GoogleSearchPage:
    def navigate_to_page(self, url: str):
        self.page.goto(url)  # Already in BasePage!

# ✅ Good - use inherited methods
class GoogleSearchPage(BasePage):
    def open(self) -> 'GoogleSearchPage':
        self.navigate(self.url)  # Use parent's method
        return self
```

### 3. Test Dependencies
```python
# ❌ Bad - test depends on another test
def test_create_user():
    global user_id
    user_id = create_user()

def test_update_user():
    update_user(user_id)  # Fails if test_create_user didn't run

# ✅ Good - tests are independent
@pytest.fixture
def created_user():
    user_id = create_user()
    yield user_id
    cleanup_user(user_id)

def test_update_user(created_user):
    update_user(created_user)
```

### 4. Hardcoded Waits
```python
# ❌ Bad - arbitrary waits
import time
time.sleep(5)  # Why 5? What are we waiting for?

# ✅ Good - explicit waits with conditions
from core.utils.wait_utils import wait_with_retry
wait_with_retry(
    lambda: self.page.locator(selector).is_visible(),
    timeout=10,
    error_message="Element not visible"
)
```

### 5. Ignoring Linter Warnings
```python
# ❌ Bad - suppressing without reason
# type: ignore
# noqa

# ✅ Good - fix the issue or document why it's suppressed
# type: ignore[union-attr]  # Playwright returns Page | None in edge cases
```

---

## 🏆 PR Size Guidelines

### Ideal PR Size
- **Lines changed**: 100-400 lines
- **Files changed**: 1-10 files
- **Review time**: 15-30 minutes

### When to Split PRs
Split into multiple PRs if:
- Adding multiple unrelated features
- Refactoring + new features (separate refactoring first)
- Changes span multiple teams
- PR diff exceeds 1000 lines

### Example of Well-Scoped PRs
```
Instead of:
❌ "Add Team Beta implementation, refactor core utilities, update docs" (2000 lines)

Split into:
✅ PR 1: "refactor: extract common utilities from team_alpha to core" (300 lines)
✅ PR 2: "feat: implement Team Beta page objects and tests" (400 lines)
✅ PR 3: "docs: add Team Beta documentation and examples" (150 lines)
```

---

## 🎓 CI/CD Pipeline Expectations

Your PR must pass all CI/CD checks:

### Automated Checks (GitLab CI)
1. **Linting**: `make lint` (Ruff)
2. **Formatting**: `make format --check` (Black + isort)
3. **Tests**: `make test-all` (all test suites)
4. **Type checking**: `mypy` (if configured)
5. **Security**: `bandit` scan (if configured)
6. **Coverage**: Minimum 80% code coverage (if configured)

### Manual Checks (Reviewer)
1. Code review by at least 1 team member
2. Architecture compliance verification
3. Documentation completeness check
4. Security review for sensitive changes

---

## 📞 Getting Help

**Before Submitting PR**:
1. Review [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
2. Check [PROJECT_GUIDE.md](PROJECT_GUIDE.md)
3. Run all validation commands above

**During Review**:
- Respond to all review comments
- Mark conversations as resolved when addressed
- Re-request review after making changes

**Questions?**
- Ask in team chat before submitting
- Reference specific documentation files
- Include context in PR description

---

## ✅ Final Checklist Before Clicking "Create PR"

```markdown
- [ ] All automated checks passing locally
- [ ] PR description filled out completely
- [ ] Self-review completed (review your own diff)
- [ ] Screenshots added (if UI changes)
- [ ] Documentation updated
- [ ] No .env or secrets committed
- [ ] Tests added for new functionality
- [ ] Appropriate reviewers assigned
- [ ] Related issues linked
```

---

**Remember**: Quality over speed. A well-tested, well-documented PR saves time in the long run!

Last Updated: 2025-11-06
