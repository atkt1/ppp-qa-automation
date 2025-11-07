"""
String and Text Processing Utilities

Common string operations for test automation:
- Price and number extraction
- Text cleaning and normalization
- Pattern matching and parsing

Usage:
    from core.utils import extract_price_from_text, sanitize_text

    price = extract_price_from_text(page_content)
    clean_text = sanitize_text(raw_text)
"""

import re
from typing import List, Optional, Union

from core.logger import log


def extract_price_from_text(text: str, currency_symbol: str = "$", return_as_float: bool = False) -> Union[str, float, None]:
    """
    Extract price from text using regex pattern.

    Supports formats:
    - $999
    - $999.99
    - $1,299.99
    - 999.99 (without symbol if currency_symbol="")

    Args:
        text: Text containing price
        currency_symbol: Currency symbol to look for (default: "$")
        return_as_float: If True, return as float instead of string

    Returns:
        Price as string (e.g., "$999.99") or float (e.g., 999.99) or None

    Examples:
        >>> extract_price_from_text("Product costs $1,299.99")
        '$1,299.99'
        >>> extract_price_from_text("$1,299.99", return_as_float=True)
        1299.99
        >>> extract_price_from_text("Price: 999.99", currency_symbol="")
        '999.99'
    """
    if not text:
        log.warning("Empty text provided for price extraction")
        return None

    try:
        # Build regex pattern based on currency symbol
        if currency_symbol:
            # Escape special regex characters in currency symbol
            escaped_symbol = re.escape(currency_symbol)
            pattern = rf"{escaped_symbol}[\d,]+(?:\.\d{{2}})?"
        else:
            # No currency symbol, just match numbers
            pattern = r"[\d,]+(?:\.\d{2})?"

        matches = re.findall(pattern, text)

        if matches:
            price_str = matches[0]
            log.debug(f"Extracted price: {price_str}")

            if return_as_float:
                # Remove currency symbol and commas, convert to float
                clean_price = re.sub(r"[^\d.]", "", price_str)
                return float(clean_price)

            return price_str

    except Exception as e:
        log.error(f"Error extracting price from text: {e}")

    log.warning(f"No price found in text: {text[:100]}...")
    return None


def extract_number_from_text(text: str, pattern: str = r"\d+", return_all: bool = False) -> Union[int, List[int], None]:
    """
    Extract numbers from text.

    Args:
        text: Text containing numbers
        pattern: Regex pattern for number format (default: one or more digits)
        return_all: If True, return list of all matches; if False, return first match

    Returns:
        Single number or list of numbers, or None

    Examples:
        >>> extract_number_from_text("Found 42 items")
        42
        >>> extract_number_from_text("Showing 1-10 of 100 results", return_all=True)
        [1, 10, 100]
    """
    if not text:
        return None

    try:
        matches = re.findall(pattern, text)

        if matches:
            if return_all:
                return [int(m) for m in matches]
            return int(matches[0])

    except Exception as e:
        log.error(f"Error extracting number from text: {e}")

    return None


def sanitize_text(text: str) -> str:
    """
    Remove extra whitespace and normalize text.

    Operations:
    - Strip leading/trailing whitespace
    - Replace multiple spaces with single space
    - Replace tabs and newlines with space
    - Normalize unicode characters

    Args:
        text: Text to sanitize

    Returns:
        Sanitized text

    Examples:
        >>> sanitize_text("  Hello   World  \\n  ")
        'Hello World'
        >>> sanitize_text("Multiple\\t\\tspaces")
        'Multiple spaces'
    """
    if not text:
        return ""

    # Replace tabs and newlines with spaces
    text = text.replace("\t", " ").replace("\n", " ").replace("\r", " ")

    # Replace multiple spaces with single space
    text = " ".join(text.split())

    return text.strip()


def normalize_whitespace(text: str) -> str:
    """
    Normalize all whitespace to single spaces.

    Similar to sanitize_text but more aggressive.

    Args:
        text: Text to normalize

    Returns:
        Text with normalized whitespace

    Examples:
        >>> normalize_whitespace("Hello\\n\\n  World")
        'Hello World'
    """
    if not text:
        return ""

    # Remove all types of whitespace and replace with single space
    return " ".join(text.split())


def truncate_text(text: str, max_length: int = 100, suffix: str = "...", word_boundary: bool = True) -> str:
    """
    Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: String to append when truncated
        word_boundary: If True, truncate at word boundary

    Returns:
        Truncated text

    Examples:
        >>> truncate_text("This is a long sentence", max_length=10)
        'This is...'
        >>> truncate_text("This is a long sentence", max_length=10, word_boundary=False)
        'This is a...'
    """
    if not text or len(text) <= max_length:
        return text

    # Calculate available length for text (excluding suffix)
    available_length = max_length - len(suffix)

    if available_length <= 0:
        return suffix[:max_length]

    truncated = text[:available_length]

    # Try to truncate at word boundary
    if word_boundary:
        last_space = truncated.rfind(" ")
        if last_space > 0:
            truncated = truncated[:last_space]

    return truncated + suffix


def remove_special_characters(text: str, keep_spaces: bool = True, keep_chars: str = "") -> str:
    """
    Remove special characters from text, keeping only alphanumeric.

    Args:
        text: Text to clean
        keep_spaces: If True, keep spaces
        keep_chars: Additional characters to keep (e.g., "-_")

    Returns:
        Cleaned text

    Examples:
        >>> remove_special_characters("Hello, World!")
        'Hello World'
        >>> remove_special_characters("user@example.com", keep_chars="@.")
        'user@example.com'
    """
    if not text:
        return ""

    # Build pattern of characters to keep
    pattern = r"[^a-zA-Z0-9"

    if keep_spaces:
        pattern += r"\s"

    if keep_chars:
        # Escape special regex characters
        escaped_chars = re.escape(keep_chars)
        pattern += escaped_chars

    pattern += "]"

    # Remove characters not in the keep pattern
    cleaned = re.sub(pattern, "", text)

    return cleaned


def extract_email_from_text(text: str) -> Optional[str]:
    """
    Extract email address from text.

    Args:
        text: Text containing email

    Returns:
        Email address or None

    Examples:
        >>> extract_email_from_text("Contact: user@example.com")
        'user@example.com'
    """
    if not text:
        return None

    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    matches = re.findall(pattern, text)

    if matches:
        return matches[0]

    return None


def extract_url_from_text(text: str) -> Optional[str]:
    """
    Extract URL from text.

    Args:
        text: Text containing URL

    Returns:
        URL or None

    Examples:
        >>> extract_url_from_text("Visit https://example.com")
        'https://example.com'
    """
    if not text:
        return None

    pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    matches = re.findall(pattern, text)

    if matches:
        return matches[0]

    return None


def clean_currency(price_str: str) -> float:
    """
    Clean currency string and convert to float.

    Removes currency symbols, commas, and other formatting.

    Args:
        price_str: Price string (e.g., "$1,299.99", "€ 1.299,99")

    Returns:
        Price as float

    Examples:
        >>> clean_currency("$1,299.99")
        1299.99
        >>> clean_currency("€ 1.299,99")
        1299.99

    Raises:
        ValueError: If string cannot be converted to number
    """
    if not price_str:
        raise ValueError("Empty price string")

    # Remove all non-numeric characters except decimal points and commas
    cleaned = re.sub(r"[^\d.,]", "", price_str)

    # Handle European format (1.299,99) vs US format (1,299.99)
    # If comma is after period, it's likely European format
    if "," in cleaned and "." in cleaned:
        if cleaned.rindex(",") > cleaned.rindex("."):
            # European format: replace period with nothing, comma with period
            cleaned = cleaned.replace(".", "").replace(",", ".")
        else:
            # US format: just remove commas
            cleaned = cleaned.replace(",", "")
    elif "," in cleaned:
        # Only comma - could be decimal separator (European) or thousands (US)
        # If there are 2 digits after comma, likely decimal
        if len(cleaned.split(",")[-1]) == 2:
            cleaned = cleaned.replace(",", ".")
        else:
            cleaned = cleaned.replace(",", "")

    try:
        return float(cleaned)
    except ValueError as e:
        raise ValueError(f"Cannot convert '{price_str}' to float: {e}")


def format_currency(amount: float, currency_symbol: str = "$", decimals: int = 2) -> str:
    """
    Format number as currency string.

    Args:
        amount: Amount to format
        currency_symbol: Currency symbol to use
        decimals: Number of decimal places

    Returns:
        Formatted currency string

    Examples:
        >>> format_currency(1299.99)
        '$1,299.99'
        >>> format_currency(1299.99, currency_symbol="€")
        '€1,299.99'
    """
    formatted = f"{amount:,.{decimals}f}"
    return f"{currency_symbol}{formatted}"
