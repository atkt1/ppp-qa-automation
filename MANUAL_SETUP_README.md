# Manual Setup Guide - Overview

**Complete guide for manually recreating the QA Test Automation Framework in a secure/air-gapped environment**

---

## 📚 Documentation Structure

This manual setup guide is split into two parts for easier navigation:

### Part 1: [MANUAL_SETUP_GUIDE.md](MANUAL_SETUP_GUIDE.md)
- **Phase 1**: Project Foundation (3 files)
  - .gitignore, pyproject.toml, .env
- **Phase 2**: Core Framework (14 files total including Phase 1)
  - core/ package structure
  - Base classes (BasePage, BaseApiClient)
  - Generic YAML data loader
  - Utility functions (string, wait, element)
  - **Checkpoint 1** at 9 files
  - **Checkpoint 2** at 14 files

### Part 2: [MANUAL_SETUP_GUIDE_PART2.md](MANUAL_SETUP_GUIDE_PART2.md)
- **Phase 3**: Team Alpha Structure (34 files total)
  - Page Objects
  - API Clients
  - Locators
  - Test Data
  - Tests (API and Web UI)
- **Phase 4**: Configuration & Final Setup (43 files total)
  - pytest.ini
  - Makefile
  - core/conftest.py
  - **Checkpoint 3** - Final verification
- **Phase 5**: Verification & First Run

---

## 🎯 Quick Start

### Option 1: Follow the Manual Guide
1. Read [MANUAL_SETUP_GUIDE.md](MANUAL_SETUP_GUIDE.md) - Start here
2. Complete Phases 1 & 2 (Core framework)
3. Continue with [MANUAL_SETUP_GUIDE_PART2.md](MANUAL_SETUP_GUIDE_PART2.md)
4. Complete Phases 3-5 (Team implementation)

### Option 2: Mixed Approach (Recommended for Secure Environments)
1. **Type manually**: Configuration files (small, environment-specific)
   - .env
   - pytest.ini
   - pyproject.toml
   - Makefile

2. **Copy from temporary access**: Large utility files
   - core/utils/string_utils.py (391 lines)
   - core/utils/wait_utils.py (389 lines)
   - core/utils/element_utils.py (487 lines)
   - Test files (examples and patterns)

3. **Type carefully**: Core framework files (well-documented in guide)
   - Base classes
   - Config and logger
   - Page objects
   - API clients

---

## 📊 Progress Tracking

| Phase | Files | Status | Checkpoint |
|-------|-------|--------|------------|
| Phase 1: Foundation | 3 | ⬜ | - |
| Phase 2: Core Framework | 14 total | ⬜ | Checkpoint 1 (9), Checkpoint 2 (14) |
| Phase 3: Team Alpha | 34 total | ⬜ | - |
| Phase 4: Configuration | 43 total | ⬜ | Checkpoint 3 |
| Phase 5: Verification | - | ⬜ | Final |

---

## 🔍 File Summary

### Must Type (Critical Files - Small)
- `.gitignore` (107 lines) - Essential for git
- `.env` (24 lines) - Environment configuration
- `pyproject.toml` (28 lines) - Dependencies
- `pytest.ini` (32 lines) - Test configuration
- `Makefile` (70 lines) - Command shortcuts

**Total: ~261 lines**

### Should Type (Core Framework - Medium)
- `core/config.py` (60 lines)
- `core/logger.py` (20 lines)
- `core/base/page_base.py` (91 lines)
- `core/base/api_client.py` (193 lines)
- `core/data/yaml_loader.py` (288 lines)
- `core/conftest.py` (50 lines)

**Total: ~702 lines**

### Recommended to Copy (Large Utilities)
- `core/utils/string_utils.py` (391 lines)
- `core/utils/wait_utils.py` (389 lines)
- `core/utils/element_utils.py` (487 lines)

**Total: ~1,267 lines**

### Can Type or Copy (Team Implementation)
- Page objects (~250 lines)
- API clients (~180 lines)
- Locators (~80 lines)
- Test data (~100 lines)
- Tests (~350 lines)

**Total: ~960 lines**

---

## ⚡ Time Estimates

| Task | Manual Typing | Copy & Verify | Notes |
|------|---------------|---------------|-------|
| Phase 1 | 20 min | 5 min | Small config files |
| Phase 2 Core | 2 hours | 30 min | Base classes, medium size |
| Phase 2 Utils | 4 hours | 15 min | Large files, recommend copying |
| Phase 3 | 3 hours | 45 min | Page objects and tests |
| Phase 4 | 30 min | 10 min | Final configuration |
| **Total** | **~10 hours** | **~2 hours** | With breaks and verification |

---

## ✅ Verification Commands

### After Phase 1
```bash
ls -la  # Should show .gitignore, .env, pyproject.toml
poetry --version
```

### After Phase 2 - Checkpoint 1
```bash
python -c "from core.config import config; from core.base import BasePage, BaseApiClient; print('Core framework OK')"
```

### After Phase 2 - Checkpoint 2
```bash
python -c "from core.data import BaseYamlDataLoader; from core.utils import extract_price_from_text, wait_with_retry, handle_optional_dialog; print('All utilities OK')"
```

### After Phase 3
```bash
python -c "from team_alpha.pages import GoogleSearchPage; from team_alpha.api_clients import ReqResApiClient; print('Team Alpha OK')"
```

### After Phase 4 - Final
```bash
poetry install
poetry run playwright install chromium
poetry run pytest --collect-only  # Should show 12 tests
```

---

## 🎓 Learning Path

If you're new to the framework, use this opportunity to:

1. **Understand base classes** - Type them manually to learn the patterns
2. **Learn utilities** - Copy these, but read through to understand available helpers
3. **Study tests** - Review test examples to learn test writing patterns
4. **Customize** - Adapt for your team's needs

---

## 🆘 Troubleshooting

### "Module not found" errors
- Check pyproject.toml `packages` setting
- Run `poetry install --no-cache`
- Verify Python path includes project root

### "pytest: command not found"
- Use `poetry run pytest` instead of `pytest`
- Or activate virtual environment: `poetry shell`

### Browser download fails
- Requires internet connection for Playwright browsers
- Alternative: Copy browsers from another machine
- Location: `~/.cache/ms-playwright/`

### Test collection fails
- Check `pytest.ini` exists and is valid
- Verify `conftest.py` files in correct locations
- Run `poetry run pytest --collect-only -v` for details

---

## 📞 Support

For questions about the framework:

1. **Read documentation first**:
   - [PROJECT_GUIDE.md](PROJECT_GUIDE.md) - Comprehensive explanation
   - [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Common patterns
   - [ARCHITECTURE.md](ARCHITECTURE.md) - Design and structure

2. **Check examples**:
   - Look at existing tests in `team_alpha/tests/`
   - Review page objects for patterns
   - Study API client implementations

3. **Verify setup**:
   - Run verification commands at each checkpoint
   - Check logs in `logs/` directory
   - Review pytest output for details

---

## 🚀 Next Steps After Setup

Once you've completed the manual setup:

1. **Customize for your environment**:
   - Update URLs in `.env`
   - Modify browser settings in `core/conftest.py`
   - Adjust timeouts in test data

2. **Add your tests**:
   - Follow Team Alpha pattern
   - Create new page objects for your app
   - Write API clients for your services

3. **Set up CI/CD**:
   - Create `.gitlab-ci.yml` or GitHub Actions
   - Configure test execution pipeline
   - Set up Allure report publishing

4. **Expand framework**:
   - Add Team Beta, Gamma, etc.
   - Create shared utilities
   - Build test data factories

---

## 📈 Success Metrics

You'll know the setup is successful when:

- ✅ All verification commands pass
- ✅ `poetry run pytest --collect-only` shows 12 tests
- ✅ Smoke tests run successfully
- ✅ Allure report generates
- ✅ No import errors
- ✅ Screenshots/videos save properly
- ✅ Logs are created in `logs/` directory

---

## 🎯 Manual Setup Workflow

```
Start
  ↓
Read MANUAL_SETUP_GUIDE.md
  ↓
Create Phase 1 (Foundation)
  ↓
Verify with commands
  ↓
Create Phase 2 (Core)
  ↓
✓ Checkpoint 1 (9 files)
  ↓
Copy or type utilities
  ↓
✓ Checkpoint 2 (14 files)
  ↓
Read MANUAL_SETUP_GUIDE_PART2.md
  ↓
Create Phase 3 (Team Alpha)
  ↓
Create Phase 4 (Configuration)
  ↓
✓ Checkpoint 3 (43 files)
  ↓
Run Phase 5 (Verification)
  ↓
Success! 🎉
```

---

**Good luck with your manual setup! Take breaks, verify frequently, and don't hesitate to use the copy approach for large files.**

**Estimated total time:** 2-10 hours depending on your approach.

---

*Last updated: 2025-10-17*
*Framework version: 1.0.0*
