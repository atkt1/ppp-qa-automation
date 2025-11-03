"""
Team Alpha Locators Package

This package provides centralized locator management for Team Alpha.
All locators are defined in a single locators.py file and exported here.

Usage:
    # Import specific locator classes
    from team_alpha.locators import GoogleSearchLocators
    from team_alpha.locators import GoogleShoppingLocators

    # Import multiple classes at once
    from team_alpha.locators import GoogleSearchLocators, GoogleShoppingLocators

    # Import all (if needed)
    from team_alpha.locators import *

    # Use in page objects
    search_input = page.locator(GoogleSearchLocators.SEARCH_INPUT)
    product_price = page.locator(GoogleShoppingLocators.PRODUCT_PRICE)

Helper Functions:
    list_locator_classes() - Returns list of all available locator class names
    get_locators(locator_class) - Returns all locator constants from a class
"""

# Import all locator classes from the single locators.py file
from team_alpha.locators.locators import GoogleSearchLocators, GoogleShoppingLocators

# Define what gets exported when using "from team_alpha.locators import *"
__all__ = [
    "GoogleSearchLocators",
    "GoogleShoppingLocators",
]


def list_locator_classes():
    """
    Returns a list of all available locator classes.

    Returns:
        List of locator class names

    Example:
        >>> from team_alpha.locators import list_locator_classes
        >>> classes = list_locator_classes()
        >>> print(classes)
        ['GoogleSearchLocators', 'GoogleShoppingLocators']
    """
    return __all__


def get_locators(locator_class):
    """
    Get all locator constants from a locator class.

    Args:
        locator_class: The locator class to extract constants from

    Returns:
        Dictionary of locator name to selector string

    Example:
        >>> from team_alpha.locators import GoogleSearchLocators, get_locators
        >>> locators = get_locators(GoogleSearchLocators)
        >>> print(locators['SEARCH_INPUT'])
        'textarea[name="q"], input[name="q"]'
    """
    return {name: value for name, value in vars(locator_class).items() if not name.startswith("_") and isinstance(value, str)}
