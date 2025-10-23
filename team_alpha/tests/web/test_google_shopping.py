import allure
import pytest
from playwright.sync_api import Page
from team_alpha.pages.google_search_page import GoogleSearchPage
from team_alpha.pages.google_shopping_page import GoogleShoppingPage
from team_alpha.test_data import load_product_data, get_result_config


@pytest.mark.team_alpha
@pytest.mark.ui
@allure.feature("Google Shopping")
@allure.story("Product Search and Price Extraction")
class TestGoogleShopping:
    """
    Test suite for Google Shopping functionality.
    
    Tests cover searching for products and extracting pricing information.
    """
    
    @pytest.mark.smoke
    @allure.title("Search for Samsung S24 Ultra and Get Price")
    @allure.description("Search for Samsung S24 Ultra on Google Shopping and extract the first listing price")
    @allure.severity(allure.severity_level.NORMAL)
    def test_samsung_s24_ultra_price_check(self, page: Page):
        """
        Test to search for Samsung S24 Ultra and get the price from first listing.

        Steps:
        1. Navigate to Google
        2. Search for product from test data
        3. Click on Shopping tab
        4. Extract price from first listing
        """
        # Load test data from YAML
        product_data = load_product_data("samsung_s24_ultra")

        with allure.step("Initialize page objects"):
            search_page = GoogleSearchPage(page)
            shopping_page = GoogleShoppingPage(page)

        with allure.step("Navigate to Google homepage"):
            search_page.open()

        with allure.step(f"Search for '{product_data.search_term}'"):
            search_page.search(product_data.search_term)

        with allure.step("Verify search results are displayed"):
            search_page.verify_search_results_displayed()

        with allure.step("Click on Shopping tab"):
            search_page.click_shopping_tab()

        with allure.step("Verify shopping results are displayed"):
            shopping_page.verify_shopping_results_displayed()

        with allure.step("Extract price from first product listing"):
            price = shopping_page.get_first_product_price()

            # Attach price to Allure report
            allure.attach(
                price,
                name="First Product Price",
                attachment_type=allure.attachment_type.TEXT
            )

            print(f"\n{'='*60}")
            print(f"{product_data.description} - First Listing Price: {price}")
            print(f"{'='*60}\n")

        with allure.step("Verify price was extracted"):
            assert price != "Price not found", "Failed to extract price from first listing"
            assert "$" in price, f"Price format unexpected: {price}"
    
    @allure.title("Get Samsung S24 Ultra Product Details")
    @allure.description("Extract complete product details including title and price")
    @allure.severity(allure.severity_level.NORMAL)
    def test_samsung_s24_ultra_product_details(self, page: Page):
        """
        Test to get complete product details for Samsung S24 Ultra.
        """
        # Load test data from YAML
        product_data = load_product_data("samsung_s24_ultra")

        with allure.step("Initialize page objects"):
            search_page = GoogleSearchPage(page)
            shopping_page = GoogleShoppingPage(page)

        with allure.step("Navigate to Google and search"):
            search_page.open()
            search_page.search(product_data.search_term)
            search_page.click_shopping_tab()

        with allure.step("Get product details"):
            details = shopping_page.get_first_product_details()

            # Attach details to report
            details_text = f"Title: {details['title']}\nPrice: {details['price']}"
            allure.attach(
                details_text,
                name="Product Details",
                attachment_type=allure.attachment_type.TEXT
            )

            print(f"\n{'='*60}")
            print(f"Product Details:")
            print(f"  Title: {details['title']}")
            print(f"  Price: {details['price']}")
            print(f"{'='*60}\n")

        with allure.step("Verify details were extracted"):
            assert details['price'] != "Price not found", "Failed to extract price"
    
    @allure.title("Verify Multiple Shopping Results Displayed")
    @allure.description("Check that multiple product listings are displayed")
    @allure.severity(allure.severity_level.MINOR)
    def test_multiple_shopping_results(self, page: Page):
        """
        Test to verify multiple shopping results are displayed.
        """
        # Load test data from YAML
        product_data = load_product_data("samsung_s24_ultra")
        result_config = get_result_config()

        with allure.step("Initialize page objects"):
            search_page = GoogleSearchPage(page)
            shopping_page = GoogleShoppingPage(page)

        with allure.step("Navigate and search"):
            search_page.open()
            search_page.search(product_data.search_term)
            search_page.click_shopping_tab()

        with allure.step("Count product listings"):
            product_count = shopping_page.get_product_count()

            allure.attach(
                str(product_count),
                name="Product Count",
                attachment_type=allure.attachment_type.TEXT
            )

            print(f"\nFound {product_count} product listings\n")

        with allure.step("Verify multiple results exist"):
            assert product_count >= result_config.minimum_results, \
                f"Expected at least {result_config.minimum_results} products, found {product_count}"
