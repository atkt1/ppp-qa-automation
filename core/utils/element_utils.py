"""
Element Interaction Utilities

Common patterns for interacting with web elements:
- Safe element operations with fallbacks
- Handling optional dialogs/popups
- Multiple locator strategies
- Text and attribute extraction

Usage:
    from core.utils import handle_optional_dialog, safe_extract_text

    # Handle cookie consent
    handle_optional_dialog(page, "button:has-text('Accept')")

    # Safe text extraction
    text = safe_extract_text(element, default="Not found")
"""

from typing import Optional, List, Any, Union
from playwright.sync_api import Page, Locator, TimeoutError as PlaywrightTimeoutError
from core.logger import log


def handle_optional_dialog(
    page: Page,
    locator: Union[str, Locator],
    action: str = "click",
    timeout: int = 2000,
    log_action: bool = True
) -> bool:
    """
    Handle optional dialogs like cookie consent, popups, notifications.

    Common pattern for dismissing dialogs that may or may not appear.
    Does not fail if dialog is not present.

    Args:
        page: Playwright Page object
        locator: Locator string or Locator object for the dialog element
        action: Action to perform - "click", "dismiss", or "none"
        timeout: Wait time for dialog in milliseconds
        log_action: If True, log when dialog is handled

    Returns:
        True if dialog was found and handled, False otherwise

    Examples:
        >>> # Handle cookie consent
        >>> handle_optional_dialog(
        ...     page,
        ...     "button:has-text('Accept all')"
        ... )

        >>> # Just check if dialog exists without clicking
        >>> dialog_present = handle_optional_dialog(
        ...     page,
        ...     "#modal",
        ...     action="none"
        ... )

        >>> # Handle with custom timeout
        >>> handle_optional_dialog(
        ...     page,
        ...     ".notification-close",
        ...     timeout=5000
        ... )
    """
    try:
        # Get locator object if string was provided
        if isinstance(locator, str):
            element = page.locator(locator)
        else:
            element = locator

        # Check if element is visible
        if element.is_visible(timeout=timeout):
            if action == "click":
                element.click()
                if log_action:
                    log.info(f"Handled optional dialog: clicked {locator}")
            elif action == "dismiss":
                # Try common dismiss methods
                element.press("Escape")
                if log_action:
                    log.info(f"Handled optional dialog: dismissed {locator}")
            elif action == "none":
                if log_action:
                    log.info(f"Optional dialog detected: {locator}")

            return True

    except (PlaywrightTimeoutError, Exception) as e:
        log.debug(
            f"Optional dialog not found or could not be handled: {locator} ({type(e).__name__})")

    return False


def safe_click(
    locator: Locator,
    timeout: int = 3000,
    force: bool = False,
    retry_count: int = 1
) -> bool:
    """
    Safely click an element with error handling.

    Args:
        locator: Playwright Locator object
        timeout: Wait time in milliseconds
        force: If True, force the click even if element is not visible
        retry_count: Number of retry attempts

    Returns:
        True if click succeeded, False otherwise

    Examples:
        >>> # Basic safe click
        >>> safe_click(page.locator("button"))

        >>> # Force click with retries
        >>> safe_click(
        ...     page.locator("#submit"),
        ...     force=True,
        ...     retry_count=3
        ... )
    """
    for attempt in range(1, retry_count + 1):
        try:
            if attempt > 1:
                log.debug(f"Click retry attempt {attempt}/{retry_count}")

            locator.click(timeout=timeout, force=force)
            return True

        except Exception as e:
            if attempt == retry_count:
                log.warning(
                    f"Failed to click element after {retry_count} attempts: {type(e).__name__}")
                return False

            log.debug(
                f"Click attempt {attempt} failed: {type(e).__name__}, retrying...")

    return False


def safe_extract_text(
    locator: Locator,
    default: str = "",
    timeout: int = 3000,
    trim: bool = True
) -> str:
    """
    Safely extract text from element with fallback.

    Args:
        locator: Playwright Locator object
        default: Default value if extraction fails
        timeout: Wait time in milliseconds
        trim: If True, trim whitespace from text

    Returns:
        Extracted text or default value

    Examples:
        >>> # Extract with default
        >>> text = safe_extract_text(
        ...     page.locator(".price"),
        ...     default="Price not available"
        ... )

        >>> # Extract without trimming
        >>> raw_text = safe_extract_text(
        ...     page.locator("pre"),
        ...     trim=False
        ... )
    """
    try:
        if locator.is_visible(timeout=timeout):
            text = locator.inner_text()
            if trim and text:
                text = text.strip()
            return text
    except Exception as e:
        log.debug(f"Failed to extract text: {type(e).__name__}")

    return default


def safe_extract_attribute(
    locator: Locator,
    attribute: str,
    default: str = "",
    timeout: int = 3000
) -> str:
    """
    Safely extract attribute value from element.

    Args:
        locator: Playwright Locator object
        attribute: Attribute name to extract
        default: Default value if extraction fails
        timeout: Wait time in milliseconds

    Returns:
        Attribute value or default

    Examples:
        >>> # Get href attribute
        >>> url = safe_extract_attribute(
        ...     page.locator("a"),
        ...     "href"
        ... )

        >>> # Get data attribute
        >>> product_id = safe_extract_attribute(
        ...     page.locator(".product"),
        ...     "data-id",
        ...     default="unknown"
        ... )
    """
    try:
        if locator.is_visible(timeout=timeout):
            value = locator.get_attribute(attribute)
            if value is not None:
                return value
    except Exception as e:
        log.debug(
            f"Failed to extract attribute '{attribute}': {type(e).__name__}")

    return default


def try_multiple_locators(
    page: Page,
    locators: List[str],
    timeout: int = 3000,
    return_first: bool = True
) -> Union[Optional[Locator], List[Locator]]:
    """
    Try multiple locators and return the first visible one or all matches.

    Useful when page structure varies or elements can be found with multiple selectors.
    Common pattern for handling different page layouts.

    Args:
        page: Playwright Page object
        locators: List of locator strings to try
        timeout: Wait time per locator in milliseconds
        return_first: If True, return first match; if False, return all matches

    Returns:
        First visible Locator, list of Locators, or None

    Examples:
        >>> # Find element with fallback selectors
        >>> price_element = try_multiple_locators(
        ...     page,
        ...     [
        ...         "span.price",
        ...         "div.product-price",
        ...         "span:has-text('$')"
        ...     ]
        ... )

        >>> # Get all matching elements
        >>> buttons = try_multiple_locators(
        ...     page,
        ...     ["button.primary", "input[type='submit']"],
        ...     return_first=False
        ... )
    """
    found_locators = []

    for locator_str in locators:
        try:
            locator = page.locator(locator_str)
            if locator.is_visible(timeout=timeout):
                log.debug(f"Found element with locator: {locator_str}")

                if return_first:
                    return locator

                found_locators.append(locator)

        except Exception as e:
            log.debug(f"Locator '{locator_str}' not found: {type(e).__name__}")
            continue

    if return_first:
        log.warning("None of the provided locators found a visible element")
        return None

    if not found_locators:
        log.warning("None of the provided locators found visible elements")

    return found_locators if found_locators else None


def wait_for_element_count(
    locator: Locator,
    expected_count: int,
    timeout: int = 10000,
    operator: str = "equal"
) -> bool:
    """
    Wait for element count to match condition.

    Args:
        locator: Playwright Locator object
        expected_count: Expected number of elements
        timeout: Wait time in milliseconds
        operator: Comparison operator - "equal", "greater", "less", "min", "max"

    Returns:
        True if condition met, False otherwise

    Examples:
        >>> # Wait for at least 5 items
        >>> wait_for_element_count(
        ...     page.locator(".item"),
        ...     expected_count=5,
        ...     operator="min"
        ... )

        >>> # Wait for exactly 3 tabs
        >>> wait_for_element_count(
        ...     page.locator(".tab"),
        ...     expected_count=3,
        ...     operator="equal"
        ... )
    """
    import time
    start_time = time.time()
    elapsed = 0

    while elapsed < (timeout / 1000):
        try:
            current_count = locator.count()

            condition_met = False
            if operator == "equal":
                condition_met = current_count == expected_count
            elif operator in ("greater", "more"):
                condition_met = current_count > expected_count
            elif operator in ("less", "fewer"):
                condition_met = current_count < expected_count
            elif operator in ("min", "atleast"):
                condition_met = current_count >= expected_count
            elif operator in ("max", "atmost"):
                condition_met = current_count <= expected_count

            if condition_met:
                log.debug(
                    f"Element count condition met: {current_count} {operator} {expected_count}")
                return True

        except Exception as e:
            log.debug(f"Error checking element count: {type(e).__name__}")

        time.sleep(0.5)
        elapsed = time.time() - start_time

    log.warning(f"Element count condition not met within {timeout}ms")
    return False


def safe_fill(
    locator: Locator,
    text: str,
    clear_first: bool = True,
    timeout: int = 3000
) -> bool:
    """
    Safely fill input field with text.

    Args:
        locator: Playwright Locator object for input element
        text: Text to fill
        clear_first: If True, clear field before filling
        timeout: Wait time in milliseconds

    Returns:
        True if fill succeeded, False otherwise

    Examples:
        >>> # Fill with clearing
        >>> safe_fill(page.locator("#email"), "user@example.com")

        >>> # Append without clearing
        >>> safe_fill(
        ...     page.locator("#search"),
        ...     " additional text",
        ...     clear_first=False
        ... )
    """
    try:
        if locator.is_visible(timeout=timeout):
            if clear_first:
                locator.clear()

            locator.fill(text)
            log.debug(f"Successfully filled input with: {text}")
            return True

    except Exception as e:
        log.warning(f"Failed to fill input: {type(e).__name__}")

    return False


def is_element_in_viewport(locator: Locator) -> bool:
    """
    Check if element is currently in the viewport.

    Args:
        locator: Playwright Locator object

    Returns:
        True if element is in viewport

    Examples:
        >>> if not is_element_in_viewport(page.locator("#footer")):
        ...     page.locator("#footer").scroll_into_view_if_needed()
    """
    try:
        # Use evaluate to check if element is in viewport
        return locator.evaluate("""
            element => {
                const rect = element.getBoundingClientRect();
                return (
                    rect.top >= 0 &&
                    rect.left >= 0 &&
                    rect.bottom <= window.innerHeight &&
                    rect.right <= window.innerWidth
                );
            }
        """)
    except Exception as e:
        log.debug(f"Error checking if element in viewport: {type(e).__name__}")
        return False


def get_element_info(locator: Locator) -> dict:
    """
    Get comprehensive information about an element for debugging.

    Args:
        locator: Playwright Locator object

    Returns:
        Dictionary with element information

    Examples:
        >>> info = get_element_info(page.locator("#submit-button"))
        >>> print(f"Element visible: {info['visible']}")
        >>> print(f"Element text: {info['text']}")
    """
    info = {
        "visible": False,
        "enabled": False,
        "text": "",
        "tag": "",
        "classes": [],
        "attributes": {}
    }

    try:
        info["visible"] = locator.is_visible(timeout=1000)
        if info["visible"]:
            info["enabled"] = locator.is_enabled()
            info["text"] = locator.inner_text()

            # Get tag name and classes
            info["tag"] = locator.evaluate("el => el.tagName.toLowerCase()")
            class_list = locator.get_attribute("class")
            if class_list:
                info["classes"] = class_list.split()

            # Get common attributes
            for attr in ["id", "name", "type", "href", "value"]:
                value = locator.get_attribute(attr)
                if value:
                    info["attributes"][attr] = value

    except Exception as e:
        log.debug(f"Error getting element info: {type(e).__name__}")

    return info
