# Parallel Testing Guide

Complete guide to running tests in parallel using pytest-xdist.

---

## 🚀 Quick Start

```bash
# Run all tests in parallel (auto-detect CPU cores)
make test-parallel

# Run web tests in parallel
make test-web-parallel

# Run API tests in parallel
make test-api-parallel

# Run smoke tests in parallel
make test-smoke-parallel
```

---

## 📋 Available Makefile Commands

| Command | Description | Workers |
|---------|-------------|---------|
| `make test-parallel` | Run all tests in parallel | Auto (CPU cores) |
| `make test-parallel-4` | Run all tests with 4 workers | 4 |
| `make test-api-parallel` | Run API tests in parallel | Auto |
| `make test-web-parallel` | Run web tests in parallel | Auto |
| `make test-smoke-parallel` | Run smoke tests in parallel | Auto |

---

## 🔧 Direct pytest-xdist Usage

### Basic Parallel Execution

```bash
# Auto-detect number of CPU cores
poetry run pytest -n auto

# Use specific number of workers
poetry run pytest -n 2    # 2 workers
poetry run pytest -n 4    # 4 workers
poetry run pytest -n 8    # 8 workers

# Verbose output
poetry run pytest -v -n auto
```

### Parallel Execution by Test Type

```bash
# API tests in parallel
poetry run pytest team_alpha/tests/api/ -v -n auto

# Web tests in parallel
poetry run pytest team_alpha/tests/web/ -v -n auto

# Specific test file
poetry run pytest team_alpha/tests/api/test_reqres_users.py -v -n 4

# By marker
poetry run pytest -m smoke -v -n auto
poetry run pytest -m "api and not slow" -v -n 4
```

### Distribution Strategies

pytest-xdist offers different strategies for distributing tests:

```bash
# Load (default): Distribute tests evenly across workers
poetry run pytest -n auto --dist load

# Load Scope: Keep tests from same class/module together
poetry run pytest -n auto --dist loadscope

# Load File: Keep tests from same file together
poetry run pytest -n auto --dist loadfile

# Load Group: Use custom grouping (requires @pytest.mark.xdist_group)
poetry run pytest -n auto --dist loadgroup
```

**When to use which:**

- **`--dist load`** (Default): Best for independent tests spread across multiple files
- **`--dist loadscope`**: Best when tests in same class share setup/teardown
- **`--dist loadfile`**: Best when tests in same file have dependencies
- **`--dist loadgroup`**: Best when you manually group related tests

---

## ⚡ Performance Comparison

### Example Test Suite (12 tests)

| Mode | Time | Speed Improvement |
|------|------|-------------------|
| Sequential (`pytest`) | 120s | Baseline |
| 2 Workers (`-n 2`) | 65s | 1.8x faster |
| 4 Workers (`-n 4`) | 35s | 3.4x faster |
| Auto Workers (`-n auto`) | 30s | 4x faster |

**Note:** Actual performance depends on:
- Number of CPU cores
- Test execution time
- I/O vs CPU bound tests
- Browser startup overhead (for UI tests)

---

## 🎯 Best Practices

### 1. When to Use Parallel Execution

✅ **Good candidates for parallel:**
- API tests (fast, independent)
- Unit tests (isolated, quick)
- Large test suites (100+ tests)
- CI/CD pipelines (time-critical)
- Regression test suites

❌ **Not good for parallel:**
- Tests with shared state/database
- Tests that depend on each other
- Tests with file system locks
- Debugging failing tests
- Very fast test suites (<10s total)

### 2. Ensure Test Independence

```python
# ❌ BAD: Tests share state
class TestUser:
    user_id = None

    def test_create_user(self):
        self.user_id = create_user()  # Fails in parallel!

    def test_delete_user(self):
        delete_user(self.user_id)  # user_id may be None!

# ✅ GOOD: Tests are independent
class TestUser:

    @pytest.fixture
    def user(self):
        user_id = create_user()
        yield user_id
        delete_user(user_id)

    def test_create_user(self, user):
        assert user is not None

    def test_delete_user(self, user):
        result = delete_user(user)
        assert result.success
```

### 3. Browser Context Isolation

Playwright automatically handles browser context isolation in parallel:

```python
# Each worker gets its own browser context
def test_parallel_safe(page: Page):
    page.goto("https://example.com")
    # This runs isolated in its own browser context
```

### 4. Environment Variables

Set per-worker environment variables if needed:

```python
# conftest.py
import os
import pytest

@pytest.fixture(scope="session", autouse=True)
def set_worker_id(worker_id):
    """Set unique ID for each parallel worker."""
    if worker_id != "master":
        os.environ["WORKER_ID"] = worker_id
```

---

## 📊 Monitoring Parallel Execution

### Live Output

```bash
# Show test names as they execute
poetry run pytest -v -n auto

# Show stdout/stderr (careful: interleaved output!)
poetry run pytest -v -n auto -s

# Show duration of slowest tests
poetry run pytest -v -n auto --durations=10
```

### Allure Reports

Parallel execution works seamlessly with Allure:

```bash
# Run tests in parallel and generate report
make test-parallel
make allure-serve
```

Each worker's results are merged into a single Allure report.

---

## 🛠️ Advanced Configuration

### Custom Worker Count Based on Test Type

```bash
# More workers for fast API tests
poetry run pytest team_alpha/tests/api/ -n 8

# Fewer workers for slow UI tests (avoid browser overhead)
poetry run pytest team_alpha/tests/web/ -n 2
```

### Grouping Related Tests

Use `@pytest.mark.xdist_group` to keep related tests on same worker:

```python
import pytest

@pytest.mark.xdist_group(name="database_tests")
class TestDatabase:
    """These tests run on the same worker."""

    def test_create_record(self):
        pass

    def test_read_record(self):
        pass

@pytest.mark.xdist_group(name="database_tests")
def test_update_record():
    """This also runs with the class above."""
    pass
```

Then run:
```bash
poetry run pytest -n auto --dist loadgroup
```

### Retry Failed Tests in Parallel

Combine with pytest-rerunfailures:

```bash
# Retry failed tests up to 2 times, running in parallel
poetry run pytest -n auto --reruns 2 --reruns-delay 1
```

---

## 🐛 Troubleshooting

### Issue 1: "Address already in use"

**Symptom:** Tests fail with port conflicts
```
OSError: [Errno 48] Address already in use
```

**Solution:** Use dynamic ports or worker-specific ports
```python
import os

def get_test_port():
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", "master")
    base_port = 8000
    worker_num = 0 if worker_id == "master" else int(worker_id.replace("gw", ""))
    return base_port + worker_num
```

### Issue 2: Tests pass individually but fail in parallel

**Symptom:** `pytest test.py` passes, but `pytest -n auto test.py` fails

**Causes:**
1. Shared state between tests
2. File system race conditions
3. Database conflicts

**Solution:**
```python
# Use unique identifiers per worker
import os
import pytest

@pytest.fixture
def unique_test_file(tmp_path, worker_id):
    """Create unique file per worker."""
    if worker_id == "master":
        file_path = tmp_path / "test_data.json"
    else:
        file_path = tmp_path / f"test_data_{worker_id}.json"
    return file_path
```

### Issue 3: Slower than sequential execution

**Symptom:** Parallel execution takes longer than sequential

**Causes:**
1. Too many workers (overhead exceeds benefit)
2. Tests are very fast already
3. Tests are I/O bound (waiting for network)

**Solution:**
```bash
# Reduce number of workers
poetry run pytest -n 2  # Instead of -n auto

# Profile test duration first
poetry run pytest --durations=20

# Use parallel only for slow tests
poetry run pytest -m "not slow"  # Run fast tests sequentially
poetry run pytest -m slow -n auto  # Parallel for slow tests only
```

### Issue 4: Interleaved console output

**Symptom:** Print statements from different tests are mixed

**Solution:**
```bash
# Don't use -s flag with parallel execution
poetry run pytest -n auto  # Good

poetry run pytest -n auto -s  # Bad: output will be mixed

# Or reduce workers
poetry run pytest -n 2 -s  # Less mixing with fewer workers
```

---

## 📈 Optimizing for CI/CD

### GitLab CI Example

```yaml
test-parallel:
  stage: test
  script:
    - poetry install
    - poetry run playwright install chromium
    - poetry run pytest -n auto --maxfail=5
  artifacts:
    when: always
    paths:
      - allure-results/
    expire_in: 1 week
```

### GitHub Actions Example

```yaml
- name: Run tests in parallel
  run: |
    poetry install
    poetry run playwright install chromium
    poetry run pytest -n auto --maxfail=5
```

### Optimization Tips for CI

```bash
# Stop after 5 failures to save CI time
poetry run pytest -n auto --maxfail=5

# Skip slow tests in CI
poetry run pytest -n auto -m "not slow"

# Use specific worker count (CI may have limited cores)
poetry run pytest -n 2
```

---

## 📝 Configuration Reference

### Enable Parallel by Default (pytest.ini)

To run tests in parallel by default, uncomment in `pytest.ini`:

```ini
[pytest]
addopts =
    -n auto                    # Enable parallel execution
    --dist loadscope           # Distribution strategy
```

Then simply run:
```bash
poetry run pytest  # Runs in parallel automatically
```

### Disable Parallel for Specific Tests

```python
import pytest

@pytest.mark.xdist_group(name="serial")
class TestMustRunSerially:
    """These tests won't run in parallel."""
    pass
```

---

## 🎓 Learning Resources

### Check Available Workers

```bash
# See how many workers pytest-xdist will use
poetry run pytest --collect-only -n auto | grep "gw"
```

### Test Distribution Visualization

```bash
# Show which worker runs which test
poetry run pytest -n 4 -v | grep -E "gw[0-9]"
```

**Example output:**
```
[gw0] PASSED team_alpha/tests/api/test_reqres_users.py::TestReqResUsers::test_get_users
[gw1] PASSED team_alpha/tests/api/test_reqres_users.py::TestReqResUsers::test_create_user
[gw2] PASSED team_alpha/tests/web/test_google_shopping.py::TestGoogleShopping::test_samsung_price
[gw3] PASSED team_alpha/tests/api/test_reqres_users.py::TestReqResUsers::test_update_user
```

---

## ✅ Quick Reference

| Task | Command |
|------|---------|
| Parallel with auto workers | `poetry run pytest -n auto` |
| Parallel with 4 workers | `poetry run pytest -n 4` |
| API tests parallel | `make test-api-parallel` |
| Web tests parallel | `make test-web-parallel` |
| Smoke tests parallel | `make test-smoke-parallel` |
| Show test duration | `poetry run pytest -n auto --durations=10` |
| Stop after 5 failures | `poetry run pytest -n auto --maxfail=5` |
| Keep tests together | `poetry run pytest -n auto --dist loadscope` |

---

## 🚦 Decision Tree: Should I Use Parallel?

```
Is your test suite > 20 tests?
  ├─ No  → Run sequential (pytest)
  └─ Yes → Are tests independent?
      ├─ No  → Fix test dependencies first
      └─ Yes → Is total time > 30 seconds?
          ├─ No  → Parallel may not help much
          └─ Yes → Use parallel! (pytest -n auto)
              └─ Profile and adjust worker count
```

---

**Created:** 2025-10-17
**Framework:** Playwright + Pytest + pytest-xdist
**Version:** 1.0.0
