# Google Shopping Test - Samsung S24 Ultra Price Check

## 📋 Overview

This test demonstrates automated price checking on Google Shopping for the Samsung S24 Ultra.

## 🎯 Test Objective

- Navigate to Google
- Search for "Samsung S24 Ultra"
- Click on Shopping tab
- Extract the price from the first product listing

## 📁 Files Created

### Page Objects

1. **`team_alpha/pages/google_search_page.py`**
   - Handles Google search functionality
   - Methods: `open()`, `search()`, `click_shopping_tab()`

2. **`team_alpha/pages/google_shopping_page.py`**
   - Handles shopping results page
   - Methods: `get_first_product_price()`, `get_first_product_details()`

### Test File

3. **`team_alpha/tests/web/test_google_shopping.py`**
   - Contains 3 test cases:
     - `test_samsung_s24_ultra_price_check` - Main price extraction test
     - `test_samsung_s24_ultra_product_details` - Get full product details
     - `test_multiple_shopping_results` - Verify multiple listings

## 🚀 How to Run

### Run the main price check test:
```bash
make test-one-headed TEST=team_alpha/tests/web/test_google_shopping.py::TestGoogleShopping::test_samsung_s24_ultra_price_check
```

### Run all Google shopping tests:
```bash
make test-one-headed TEST=team_alpha/tests/web/test_google_shopping.py
```

### Run without visible browser (headless):
```bash
make test-one TEST=team_alpha/tests/web/test_google_shopping.py::TestGoogleShopping::test_samsung_s24_ultra_price_check
```

## ⚠️ Important Notes

### Google CAPTCHA Detection

Google may show a CAPTCHA page when it detects automated traffic. This is expected behavior and shows:
- `https://www.google.com/sorry/index...`

**Solutions if CAPTCHA appears:**
1. **Add delays**: Run tests less frequently
2. **Use different IP**: Change network/VPN
3. **User agent**: The test already uses a regular browser user-agent
4. **Manual intervention**: Run with `--headed` and solve CAPTCHA manually

### Selectors May Change

Google frequently updates its page structure. If price extraction fails:
1. The page object includes multiple fallback selectors
2. Includes regex pattern matching as last resort
3. Check `google_shopping_page.py` and update selectors if needed

## 📊 Test Output

When successful, the test will print:
```
============================================================
Samsung S24 Ultra - First Listing Price: $899.99
============================================================
```

The price is also attached to the Allure report.

## 🔍 Test Markers

- `@pytest.mark.team_alpha` - Team Alpha tests
- `@pytest.mark.ui` - UI/Web tests
- `@pytest.mark.smoke` - Smoke test suite
- `@allure.feature("Google Shopping")` - Allure reporting
- `@allure.story("Product Search and Price Extraction")` - Allure story

## 🛠️ Customization

### Search for a different product:
Edit the test file and change the search query:
```python
search_page.search("iPhone 15 Pro")  # Instead of "samsung s24 ultra"
```

### Extract from different listing:
Modify `google_shopping_page.py`:
```python
# Change from .first to .nth(1) for second listing
self.first_product_price: Locator = page.locator('span.a8Pemb').nth(1)
```

## 📝 Example Test Flow

```python
# 1. Initialize page objects
search_page = GoogleSearchPage(page)
shopping_page = GoogleShoppingPage(page)

# 2. Navigate and search
search_page.open()
search_page.search("samsung s24 ultra")

# 3. Go to shopping
search_page.click_shopping_tab()

# 4. Extract price
price = shopping_page.get_first_product_price()
print(f"Price: {price}")
```

## ✅ Success Criteria

- ✅ Test navigates to Google
- ✅ Search query is entered
- ✅ Shopping tab is clicked
- ✅ Price is extracted from first listing
- ✅ Price contains "$" symbol
- ✅ Test passes assertions

## 🐛 Troubleshooting

### Test fails with CAPTCHA
**Error**: `Google CAPTCHA detected`  
**Solution**: Wait a few minutes and retry, or use a different network

### Price not found
**Error**: `Price not found`  
**Solution**: Google may have changed selectors. Update `google_shopping_page.py` with new selectors

### Shopping tab not found
**Error**: `Element not found`  
**Solution**: Google may have changed the layout. Check if Shopping results are available for your query

## 📚 Related Files

- [LoginPage](../pages/login_page.py) - Example of another page object
- [DashboardPage](../pages/dashboard_page.py) - More complex page object example
- [Test Patterns](../../../../test_patterns.md) - General testing patterns

---

**Created**: October 16, 2025  
**Test Type**: Web UI Automation  
**Framework**: Playwright + Pytest  
**Page Object Pattern**: Implemented
