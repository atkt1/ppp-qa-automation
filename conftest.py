"""
Root conftest.py for the QA automation framework.

This ensures fixtures from core are available to all test modules.
"""

# Import fixtures from core/conftest.py to make them globally available
from core.conftest import (
    api_request_context,
    browser_context_args,
    browser_type_launch_args,
    page,
    pytest_runtest_makereport,
    take_screenshot,
    test_logging,
)

__all__ = [
    "api_request_context",
    "browser_context_args",
    "browser_type_launch_args",
    "page",
    "pytest_runtest_makereport",
    "take_screenshot",
    "test_logging",
]
