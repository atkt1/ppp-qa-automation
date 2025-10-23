"""
Team Alpha Locators

This module contains ALL locators for Team Alpha's web tests.
Each page has its own class for organization.
All locator classes are in this single file for easy maintenance.

Usage:
    from team_alpha.locators import GoogleSearchLocators, GoogleShoppingLocators

    # Use in page objects
    search_input = page.locator(GoogleSearchLocators.SEARCH_INPUT)
    product_price = page.locator(GoogleShoppingLocators.PRODUCT_PRICE)
"""


class GoogleSearchLocators:
    """
    Locators for Google Search Page elements.

    Usage:
        from team_alpha.locators import GoogleSearchLocators
        search_input = page.locator(GoogleSearchLocators.SEARCH_INPUT)
    """

    # Search Input Elements
    SEARCH_INPUT = 'textarea[name="q"], input[name="q"]'
    SEARCH_BUTTON = 'button[type="submit"]'
    SEARCH_VOICE_BUTTON = 'div[aria-label*="Search by voice"]'
    SEARCH_IMAGE_BUTTON = 'div[aria-label*="Search by image"]'

    # Navigation Tabs
    ALL_TAB = 'a[role="tab"]:has-text("All")'
    IMAGES_TAB = 'a[href*="tbm=isch"]'
    VIDEOS_TAB = 'a[href*="tbm=vid"]'
    SHOPPING_TAB = 'a[href*="tbm=shop"]'
    NEWS_TAB = 'a[href*="tbm=nws"]'
    MAPS_TAB = 'a[href*="maps"]'
    BOOKS_TAB = 'a[href*="tbm=bks"]'
    FLIGHTS_TAB = 'a[href*="tbm=flm"]'

    # Search Suggestions
    SUGGESTIONS_CONTAINER = 'div[role="presentation"]'
    SUGGESTION_ITEM = 'li[role="presentation"]'
    SUGGESTION_TEXT = 'div[role="option"]'

    # Cookie Consent (GDPR)
    COOKIE_CONSENT_DIALOG = 'div[role="dialog"]'
    COOKIE_ACCEPT_ALL = 'button:has-text("Accept all"), button:has-text("I agree")'
    COOKIE_REJECT_ALL = 'button:has-text("Reject all")'
    COOKIE_CUSTOMIZE = 'button:has-text("Customize")'

    # Page Elements
    GOOGLE_LOGO = 'img[alt*="Google"]'
    SEARCH_RESULTS_CONTAINER = '#search'
    RESULT_STATS = '#result-stats'

    # Error/CAPTCHA
    CAPTCHA_CONTAINER = 'div[id*="captcha"]'
    ERROR_MESSAGE = 'div[id*="error"]'


class GoogleShoppingLocators:
    """
    Locators for Google Shopping Page elements.

    Usage:
        from team_alpha.locators import GoogleShoppingLocators
        product_items = page.locator(GoogleShoppingLocators.PRODUCT_ITEMS)
    """

    # Product Listing Elements
    PRODUCT_ITEMS = 'div[data-merchant-id], div.sh-dgr__content'
    PRODUCT_ITEM_GRID = 'div.sh-dgr__grid-result'
    PRODUCT_CARD = 'div[data-docid]'

    # Product Details
    PRODUCT_TITLE = 'h3, h4, div[role="heading"]'
    PRODUCT_PRICE = (
        'span[aria-label*="$"], '
        'span:has-text("$"), '
        'div.a8Pemb, '
        'span.HRLxBb'
    )
    PRODUCT_IMAGE = 'img[src*="encrypted"], img[src*="gstatic"]'
    PRODUCT_RATING = 'span[role="img"][aria-label*="stars"]'
    PRODUCT_REVIEWS = 'span.NrDZNb, span:has-text("reviews")'
    PRODUCT_MERCHANT = 'div.aULzUe, span.IuHnof'
    PRODUCT_SHIPPING = 'span:has-text("shipping"), span:has-text("delivery")'

    # Product Actions
    PRODUCT_LINK = 'a[href*="shopping/product"]'
    COMPARE_PRICES = 'span:has-text("Compare prices")'
    VIEW_DETAILS = 'a:has-text("View details")'

    # Filters
    FILTERS_CONTAINER = 'div[aria-label="Filters"], div.hdtb-mn-hd'
    FILTER_PRICE = 'button:has-text("Price"), div[aria-label*="Price"]'
    FILTER_BRAND = 'button:has-text("Brand"), div[aria-label*="Brand"]'
    FILTER_CONDITION = 'button:has-text("Condition")'
    FILTER_RETAILER = 'button:has-text("Retailer"), div[aria-label*="Retailer"]'
    FILTER_SHIPPING = 'button:has-text("Shipping")'
    FILTER_COLOR = 'button:has-text("Color")'
    FILTER_SIZE = 'button:has-text("Size")'

    # Filter Options
    FILTER_OPTION = 'div[role="menuitem"], span[role="checkbox"]'
    FILTER_APPLY = 'button:has-text("Apply")'
    FILTER_CLEAR = 'button:has-text("Clear"), a:has-text("Clear")'
    ACTIVE_FILTERS = 'div.EIZ8Dd, div[role="button"][aria-label*="Remove"]'

    # Sorting
    SORT_BY_DROPDOWN = 'button[aria-label="Sort by"], select[aria-label*="Sort"]'
    SORT_RELEVANCE = 'div[role="menuitem"]:has-text("Relevance")'
    SORT_PRICE_LOW = 'div[role="menuitem"]:has-text("Price: Low to high")'
    SORT_PRICE_HIGH = 'div[role="menuitem"]:has-text("Price: High to low")'
    SORT_RATING = 'div[role="menuitem"]:has-text("Rating")'

    # Pagination
    PAGINATION_CONTAINER = 'div[role="navigation"]'
    NEXT_PAGE = 'a#pnnext, button:has-text("Next")'
    PREV_PAGE = 'a#pnprev, button:has-text("Previous")'
    PAGE_NUMBER = 'td.cur, span[aria-current="page"]'

    # Search Refinement
    SEARCH_QUERY = 'input[name="q"]'
    REFINE_SEARCH = 'button:has-text("Refine")'
    RELATED_SEARCHES = 'div.card-section:has-text("Related searches")'

    # Product Comparison
    COMPARE_BAR = 'div[aria-label*="Compare"]'
    COMPARE_CHECKBOX = 'input[type="checkbox"][aria-label*="Compare"]'
    COMPARE_BUTTON = 'button:has-text("Compare")'
    COMPARE_COUNT = 'span:has-text("items to compare")'

    # Empty State
    NO_RESULTS = 'div:has-text("No results found")'
    NO_RESULTS_MESSAGE = 'div.mnr-c'

    # Loading States
    LOADING_SPINNER = 'div[role="progressbar"]'
    LOADING_PLACEHOLDER = 'div.sh-dgr__placeholder'
