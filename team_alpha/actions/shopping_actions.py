"""
Shopping Actions - Business workflows for Google Shopping tests.

This module provides high-level actions that orchestrate multiple page objects
to implement complete user journeys and business workflows.
"""

import allure
from playwright.sync_api import Page

from core.logger import log
from core.utils import extract_price_from_text
from team_alpha.pages.google_search_page import GoogleSearchPage
from team_alpha.pages.google_shopping_page import GoogleShoppingPage
from team_alpha.test_data import get_result_config, load_product_data


class ShoppingActions:
    """
    Action class for Google Shopping workflows.

    Orchestrates GoogleSearchPage and GoogleShoppingPage to implement
    complete business workflows. Provides fluent interface for test composition.

    Example:
        actions = ShoppingActions(page, load_product_data)
        (actions
         .search_for_product("samsung_s24_ultra")
         .verify_search_results(min_count=3)
         .verify_product_contains_keywords(["Samsung", "S24"]))
    """

    def __init__(self, page: Page, data_loader=None):
        """
        Initialize shopping actions with page objects.

        Args:
            page: Playwright Page object
            data_loader: Function to load product data (defaults to load_product_data)
        """
        self.page = page
        self.search_page = GoogleSearchPage(page)
        self.shopping_page = GoogleShoppingPage(page)
        self.data_loader = data_loader or load_product_data
        self.result_config = get_result_config()

        # Store context for chained operations
        self._current_product_data = None
        self._last_product_details = None

    @allure.step("Navigate to Google homepage")
    def navigate_to_google(self):
        """
        Navigate to Google homepage.

        Returns:
            self: For method chaining
        """
        log.info("Action: Navigate to Google homepage")
        self.search_page.open()
        return self

    @allure.step("Search for product: {product_key}")
    def search_for_product(self, product_key: str):
        """
        Complete product search workflow.

        This action orchestrates:
        1. Load product data from test data
        2. Navigate to Google
        3. Perform search
        4. Navigate to Shopping tab

        Args:
            product_key: Product identifier in test data (e.g., "samsung_s24_ultra")

        Returns:
            self: For method chaining
        """
        log.info(f"Action: Search for product '{product_key}'")

        # Load test data
        self._current_product_data = self.data_loader(product_key)

        # Orchestrate page objects
        self.search_page.open()
        self.search_page.search(self._current_product_data.search_term)
        self.search_page.verify_search_results_displayed()
        self.search_page.click_shopping_tab()
        self.shopping_page.verify_shopping_results_displayed()

        # Attach to report
        allure.attach(
            f"Search term: {self._current_product_data.search_term}\n" f"Description: {self._current_product_data.description}",
            name="Product Search Details",
            attachment_type=allure.attachment_type.TEXT,
        )

        return self

    @allure.step("Search for product with term: {search_term}")
    def search_for_product_by_term(self, search_term: str):
        """
        Search for product using direct search term (without test data).

        Args:
            search_term: Direct search query

        Returns:
            self: For method chaining
        """
        log.info(f"Action: Search for product with term '{search_term}'")

        self.search_page.open()
        self.search_page.search(search_term)
        self.search_page.verify_search_results_displayed()
        self.search_page.click_shopping_tab()
        self.shopping_page.verify_shopping_results_displayed()

        return self

    @allure.step("Verify at least {min_count} search results are displayed")
    def verify_search_results(self, min_count: int = None):
        """
        Verify minimum number of product results.

        Args:
            min_count: Minimum expected product count (defaults to config value)

        Returns:
            self: For method chaining

        Raises:
            AssertionError: If product count is below minimum
        """
        if min_count is None:
            min_count = self.result_config.minimum_results

        log.info(f"Action: Verify at least {min_count} search results")

        product_count = self.shopping_page.get_product_count()

        # Attach to report
        allure.attach(
            str(product_count),
            name="Product Count",
            attachment_type=allure.attachment_type.TEXT,
        )

        log.info(f"Found {product_count} product listings")

        assert product_count >= min_count, f"Expected at least {min_count} products, found {product_count}"

        return self

    @allure.step("Verify product titles contain keywords: {keywords}")
    def verify_product_contains_keywords(self, keywords: list):
        """
        Verify first product title contains expected keywords.

        Args:
            keywords: List of keywords to check (case-insensitive)

        Returns:
            self: For method chaining

        Raises:
            AssertionError: If any keyword is not found in title
        """
        log.info(f"Action: Verify product contains keywords {keywords}")

        details = self.shopping_page.get_first_product_details()
        self._last_product_details = details
        title = details.get("title", "")

        # Check each keyword
        missing_keywords = []
        for keyword in keywords:
            if keyword.lower() not in title.lower():
                missing_keywords.append(keyword)

        # Attach to report
        allure.attach(
            f"Product Title: {title}\n"
            f"Expected Keywords: {', '.join(keywords)}\n"
            f"Missing Keywords: {', '.join(missing_keywords) if missing_keywords else 'None'}",
            name="Keyword Verification",
            attachment_type=allure.attachment_type.TEXT,
        )

        assert not missing_keywords, f"Keywords {missing_keywords} not found in product title: '{title}'"

        return self

    @allure.step("Extract and verify price is present")
    def extract_and_verify_price(self):
        """
        Extract first product price and verify it's valid.

        Returns:
            self: For method chaining

        Raises:
            AssertionError: If price extraction fails
        """
        log.info("Action: Extract and verify price")

        price = self.shopping_page.get_first_product_price()

        # Attach to report
        allure.attach(
            price,
            name="Extracted Price",
            attachment_type=allure.attachment_type.TEXT,
        )

        log.info(f"Extracted price: {price}")

        assert price != "Price not found", "Failed to extract price from first listing"
        assert "$" in price, f"Price format unexpected: {price}"

        return self

    @allure.step("Get complete product details")
    def get_product_details(self):
        """
        Extract complete product details (title, price, etc.).

        Returns:
            self: For method chaining
        """
        log.info("Action: Get product details")

        details = self.shopping_page.get_first_product_details()
        self._last_product_details = details

        # Attach to report
        details_text = f"Title: {details['title']}\nPrice: {details['price']}"
        allure.attach(
            details_text,
            name="Product Details",
            attachment_type=allure.attachment_type.TEXT,
        )

        log.info(f"Product details: Title='{details['title']}', Price='{details['price']}'")

        return self

    @allure.step("Verify product details are valid")
    def verify_product_details_valid(self):
        """
        Verify that extracted product details are valid.

        Returns:
            self: For method chaining

        Raises:
            AssertionError: If details are invalid
        """
        log.info("Action: Verify product details are valid")

        if not self._last_product_details:
            self._last_product_details = self.shopping_page.get_first_product_details()

        assert self._last_product_details["price"] != "Price not found", "Failed to extract price"
        assert self._last_product_details["title"], "Failed to extract title"

        return self

    @allure.step("Filter by price range ${min_price} - ${max_price}")
    def filter_by_price_range(self, min_price: int, max_price: int):
        """
        Apply price range filter (placeholder for future implementation).

        Note: This is a placeholder for demonstration. Google Shopping's
        filter UI varies and would require additional locators.

        Args:
            min_price: Minimum price
            max_price: Maximum price

        Returns:
            self: For method chaining
        """
        log.info(f"Action: Filter by price range ${min_price} - ${max_price}")

        # Attach to report
        allure.attach(
            f"Min Price: ${min_price}\nMax Price: ${max_price}",
            name="Price Range Filter",
            attachment_type=allure.attachment_type.TEXT,
        )

        # TODO: Implement actual filtering logic when locators are available
        log.warning("Price filtering not yet implemented - placeholder action")

        return self

    @allure.step("Complete product search and validation workflow")
    def complete_product_search_workflow(self, product_key: str, min_results: int = None):
        """
        Execute complete product search workflow with all validations.

        This is a high-level workflow that combines multiple actions:
        1. Search for product
        2. Verify results count
        3. Extract product details
        4. Verify details are valid

        Args:
            product_key: Product identifier in test data
            min_results: Minimum expected results (defaults to config)

        Returns:
            self: For method chaining
        """
        log.info(f"Action: Complete product search workflow for '{product_key}'")

        return (
            self.search_for_product(product_key)
            .verify_search_results(min_results)
            .get_product_details()
            .verify_product_details_valid()
        )
