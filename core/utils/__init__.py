"""
Core Utilities Package

Provides reusable utility functions for all teams.
"""

from core.utils.element_utils import (
    handle_optional_dialog,
    safe_click,
    safe_extract_attribute,
    safe_extract_text,
    try_multiple_locators,
)
from core.utils.string_utils import (
    extract_number_from_text,
    extract_price_from_text,
    normalize_whitespace,
    remove_special_characters,
    sanitize_text,
    truncate_text,
)
from core.utils.wait_utils import (
    retry_on_exception,
    wait_for_condition,
    wait_with_retry,
)

__all__ = [
    # String utilities
    "extract_price_from_text",
    "extract_number_from_text",
    "sanitize_text",
    "truncate_text",
    "normalize_whitespace",
    "remove_special_characters",
    # Wait utilities
    "wait_with_retry",
    "retry_on_exception",
    "wait_for_condition",
    # Element utilities
    "handle_optional_dialog",
    "safe_click",
    "safe_extract_text",
    "safe_extract_attribute",
    "try_multiple_locators",
]
