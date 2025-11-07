import allure
from playwright.sync_api import Locator, Page

from core.base.page_base import BasePage
from core.logger import log
from core.utils import extract_price_from_text, safe_extract_text, try_multiple_locators
from team_alpha.locators import GoogleShoppingLocators


class GoogleShoppingPage(BasePage):
    """
    Page Object Model for Google Shopping Results Page.

    Handles interactions with shopping listings and price extraction.
    Uses centralized locators from GoogleShoppingLocators class.
    """

    def __init__(self, page: Page):
        super().__init__(page)

        # Initialize locators from centralized locator class
        self.product_items: Locator = page.locator(GoogleShoppingLocators.PRODUCT_ITEMS)
        self.product_cards: Locator = page.locator(GoogleShoppingLocators.PRODUCT_CARD)
        self.product_title: Locator = page.locator(GoogleShoppingLocators.PRODUCT_TITLE)
        self.product_price: Locator = page.locator(GoogleShoppingLocators.PRODUCT_PRICE)

    @allure.step("Get price of first product listing")
    def get_first_product_price(self) -> str:
        """
        Extract the price from the first product listing.

        Returns:
            Price as a string (e.g., "$999.99")
        """
        log.info("Extracting price from first product listing")

        # Wait for shopping results to load
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(2000)  # Give page time to render

        # Try multiple locators using utility function
        price_locators = [
            GoogleShoppingLocators.PRODUCT_PRICE,
            'span:has-text("$")',
            "div.a8Pemb",
        ]

        price_element = try_multiple_locators(self.page, price_locators, timeout=5000, return_first=True)

        if price_element:
            price = safe_extract_text(price_element.first, default="")
            if price:
                log.info(f"Found price: {price}")
                return price

        # Last resort - extract price from page content using regex utility
        try:
            all_text = self.page.content()
            price = extract_price_from_text(all_text, currency_symbol="$")
            if price:
                log.info(f"Found price using regex pattern: {price}")
                return price
        except Exception as e:
            log.error(f"Failed to extract price: {e}")

        log.error("Could not find any price on the page")
        return "Price not found"

    @allure.step("Get details of first product listing")
    def get_first_product_details(self) -> dict:
        """
        Get comprehensive details of the first product.

        Returns:
            Dictionary with product details (title, price, seller)
        """
        log.info("Extracting first product details")

        details = {"title": "", "price": "", "seller": ""}

        try:
            # Get price
            details["price"] = self.get_first_product_price()

            # Try to get product title using safe extraction utility
            title_locator = self.page.locator('h3, h4, [role="heading"]').first
            details["title"] = safe_extract_text(title_locator, default="", timeout=3000)
            if details["title"]:
                log.info(f"Product title: {details['title']}")

        except Exception as e:
            log.warning(f"Error extracting product details: {e}")

        return details

    @allure.step("Verify shopping results are displayed")
    def verify_shopping_results_displayed(self):
        """Verify that shopping results are visible."""
        log.info("Verifying shopping results are displayed")

        # Check URL contains shopping parameter
        self.page.wait_for_url("*tbm=shop*", timeout=10000)
        log.info("Shopping results page verified")

    @allure.step("Get count of product listings")
    def get_product_count(self) -> int:
        """
        Get the number of product listings on the page.

        Returns:
            Number of products found
        """
        try:
            count = self.product_cards.count()
            log.info(f"Found {count} product listings")
            return count
        except Exception as e:
            log.warning(f"Could not count products: {e}")
            return 0
