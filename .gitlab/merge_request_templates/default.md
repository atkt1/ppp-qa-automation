## Summary
<!-- Brief description of what this MR does (2-3 sentences) -->


## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Refactoring (code improvement without functionality change)
- [ ] Documentation update
- [ ] Configuration/CI change

## Changes Made
<!-- Bullet point list of specific changes -->
-
-
-

## Testing Performed
- [ ] All existing tests pass (`make test-all`)
- [ ] Ran tests in parallel mode (`make test-parallel`)
- [ ] Code formatted (`make format`)
- [ ] Linting passed (`make lint`)
- [ ] Added X new tests covering:
  -
  -
- [ ] Manually tested:

## Screenshots/Videos
<!-- Add screenshots or video recordings for UI-related changes -->


## Pre-Submission Checklist
### Code Quality
- [ ] Black formatting applied (`make format`)
- [ ] Ruff linting passed (`make lint`)
- [ ] Type hints added to all functions
- [ ] Docstrings present for public methods
- [ ] Python 3.9+ compatible (no `|` unions, no `match/case`)

### Testing
- [ ] All tests passing
- [ ] New tests added for new features
- [ ] Test independence verified
- [ ] Appropriate pytest markers used

### Architecture
- [ ] Locators centralized in `locators/locators.py`
- [ ] Page objects extend `BasePage`
- [ ] Method chaining implemented (`return self`)
- [ ] Used `open()` not `navigate()` in page objects

### Security
- [ ] No secrets committed (`.env` excluded)
- [ ] No hardcoded credentials
- [ ] No API keys in code

### Documentation
- [ ] README.md updated (if needed)
- [ ] Inline comments added for complex logic
- [ ] CLAUDE.md updated (if architecture changed)

### YAML & Data
- [ ] YAML syntax valid
- [ ] Dataclasses match YAML structure
- [ ] 2-space indentation in YAML

## Related Issues
<!-- Link related issues -->
Closes #
Related to #

## Additional Notes
<!-- Any additional context, dependencies, or breaking changes -->


---
**Reviewer Note**: Please verify all checklist items before approval. See [PULL_REQUEST_GUIDELINES.md](../PULL_REQUEST_GUIDELINES.md) for detailed review criteria.
