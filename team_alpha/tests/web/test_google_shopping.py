import allure
import pytest
from playwright.sync_api import Page

from team_alpha.actions import ShoppingActions
from team_alpha.test_data import load_product_data


@pytest.mark.team_alpha
@pytest.mark.ui
@allure.feature("Google Shopping")
@allure.story("Product Search and Price Extraction")
class TestGoogleShopping:
    """
    Test suite for Google Shopping functionality using Action Composition.

    Tests use ShoppingActions class to compose high-level business workflows
    from reusable actions. This provides better readability and maintainability
    while preserving detailed Allure reporting.
    """

    @pytest.mark.smoke
    @allure.title("Search for Samsung S24 Ultra and Get Price")
    @allure.description("Search for Samsung S24 Ultra on Google Shopping and extract the first listing price")
    @allure.severity(allure.severity_level.NORMAL)
    def test_samsung_s24_ultra_price_check(self, page: Page):
        """
        Test to search for Samsung S24 Ultra and get the price from first listing.

        Uses action composition to create a fluent, readable test while
        maintaining detailed Allure step reporting.
        """
        actions = ShoppingActions(page, load_product_data)

        # Compose test from reusable actions with fluent interface
        (actions.search_for_product("samsung_s24_ultra").extract_and_verify_price())

    @allure.title("Get Samsung S24 Ultra Product Details")
    @allure.description("Extract complete product details including title and price")
    @allure.severity(allure.severity_level.NORMAL)
    def test_samsung_s24_ultra_product_details(self, page: Page):
        """
        Test to get complete product details for Samsung S24 Ultra.

        Demonstrates action composition for complex workflows.
        """
        actions = ShoppingActions(page, load_product_data)

        (actions.search_for_product("samsung_s24_ultra").get_product_details().verify_product_details_valid())

    @allure.title("Verify Multiple Shopping Results Displayed")
    @allure.description("Check that multiple product listings are displayed")
    @allure.severity(allure.severity_level.MINOR)
    def test_multiple_shopping_results(self, page: Page):
        """
        Test to verify multiple shopping results are displayed.

        Shows how action composition simplifies result validation.
        """
        actions = ShoppingActions(page, load_product_data)

        (actions.search_for_product("samsung_s24_ultra").verify_search_results())

    @allure.title("Search and Verify Product Contains Keywords")
    @allure.description("Verify product search results contain expected keywords")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_and_verify_keywords(self, page: Page):
        """
        Test searching and verifying product contains expected keywords.

        Demonstrates composing multiple validation actions.
        """
        actions = ShoppingActions(page, load_product_data)

        (
            actions.search_for_product("samsung_s24_ultra")
            .verify_search_results(min_count=3)
            .verify_product_contains_keywords(["Samsung", "S24"])
        )

    @allure.title("Complete Product Search Workflow")
    @allure.description("Execute complete end-to-end product search workflow")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_complete_product_search_workflow(self, page: Page):
        """
        Comprehensive test demonstrating complete product search workflow.

        This test showcases how action composition enables complex,
        multi-step workflows while maintaining clarity.
        """
        actions = ShoppingActions(page, load_product_data)

        # Use high-level workflow action
        actions.complete_product_search_workflow("samsung_s24_ultra", min_results=5)
