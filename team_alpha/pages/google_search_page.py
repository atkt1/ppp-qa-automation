import allure
from playwright.sync_api import Locator, Page

from core.base.page_base import BasePage
from core.logger import log
from core.utils import handle_optional_dialog
from team_alpha.locators import GoogleSearchLocators


class GoogleSearchPage(BasePage):
    """
    Page Object Model for Google Search Page.

    Handles search functionality and navigation to different tabs.
    Uses centralized locators from GoogleSearchLocators class.
    """

    def __init__(self, page: Page):
        super().__init__(page)

        # Store page URL for easy access
        self.url = "https://www.google.com"

        # Initialize locators from centralized locator class
        self.search_input: Locator = page.locator(GoogleSearchLocators.SEARCH_INPUT)
        self.search_button: Locator = page.locator(GoogleSearchLocators.SEARCH_BUTTON)
        self.shopping_tab: Locator = page.locator(GoogleSearchLocators.SHOPPING_TAB)
        self.all_tab: Locator = page.locator(GoogleSearchLocators.ALL_TAB)

    @allure.step("Open Google homepage")
    def open(self):
        """
        Open Google homepage.

        Uses the parent's navigate() method with stored URL.

        Returns:
            self: For method chaining
        """
        log.info("Opening Google Search page")
        self.navigate(self.url)  # Use parent's navigate() method
        self.wait_for_load_state("domcontentloaded")
        return self

    @allure.step("Search for: {query}")
    def search(self, query: str):
        """
        Perform a search on Google.

        Args:
            query: Search query string

        Returns:
            self: For method chaining
        """
        log.info(f"Searching for: {query}")

        # Handle cookie consent if present using utility
        handle_optional_dialog(
            self.page,
            GoogleSearchLocators.COOKIE_ACCEPT_ALL,
            action="click",
            timeout=2000,
        )

        # Perform search
        self.search_input.click()
        self.search_input.fill(query)
        self.search_input.press("Enter")

        # Wait for results
        self.page.wait_for_load_state("domcontentloaded")
        log.info("Search completed")
        return self

    @allure.step("Click on Shopping tab")
    def click_shopping_tab(self):
        """
        Click on the Shopping tab in search results.

        Returns:
            self: For method chaining
        """
        log.info("Clicking Shopping tab")
        self.shopping_tab.click()
        self.page.wait_for_load_state("domcontentloaded")
        log.info("Navigated to Shopping results")
        return self

    @allure.step("Verify search results are displayed")
    def verify_search_results_displayed(self):
        """
        Verify that search results are visible.

        Returns:
            self: For method chaining

        Raises:
            Exception: If CAPTCHA is detected
            AssertionError: If not on Google domain
        """
        # Check if we're on a results page or CAPTCHA page
        current_url = self.page.url

        if "sorry/index" in current_url:
            log.warning("Google CAPTCHA detected - automated traffic blocked")
            raise Exception(
                "Google CAPTCHA detected. This is expected for automated tests. Try running with slower timing or different IP."
            )

        # Check if we're on a results page
        assert "google.com" in current_url, f"Not on Google domain: {current_url}"
        log.info("Search results page verified")
        return self
