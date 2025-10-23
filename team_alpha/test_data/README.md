# Test Data Management

This directory contains test data files and utilities for Team Alpha tests.

## Structure

```
test_data/
├── __init__.py                 # Package exports
├── data_loader.py              # YAML data loader with data classes
├── google_shopping.yaml        # Test data for Google Shopping tests
└── README.md                   # This file
```

## Usage Examples

### Basic Usage - Load Single Product

```python
from team_alpha.test_data import load_product_data

def test_product_search():
    # Load product data from YAML
    product_data = load_product_data("samsung_s24_ultra")

    # Use in test
    search_page.search(product_data.search_term)
    assert min_price >= product_data.min_price
```

### Load Configuration

```python
from team_alpha.test_data import get_result_config, get_test_config

def test_results():
    config = get_result_config()
    assert product_count >= config.minimum_results

    test_config = get_test_config()
    page.wait_for_timeout(test_config.wait_for_results * 1000)
```

### Parametrized Testing - Test Multiple Products

```python
import pytest
from team_alpha.test_data import get_all_products

# Get all products for parametrization
products = get_all_products()

@pytest.mark.parametrize("product_key,product_data", products.items())
def test_all_products(product_key, product_data):
    """Test searches for all products defined in YAML."""
    search_page.search(product_data.search_term)

    # Verify expected keywords appear in results
    for keyword in product_data.expected_keywords:
        assert keyword in page.content()
```

### List Available Products

```python
from team_alpha.test_data import list_available_products

# Get list of product keys
available = list_available_products()
print(available)  # ['samsung_s24_ultra', 'iphone_15_pro', 'pixel_8_pro']
```

## Adding New Test Data

### 1. Add to YAML File

Edit `google_shopping.yaml`:

```yaml
products:
  macbook_pro_m3:
    search_term: "macbook pro m3"
    expected_keywords:
      - "MacBook"
      - "Pro"
      - "M3"
    min_price: 1500
    max_price: 3000
    description: "Apple MacBook Pro with M3 chip"
```

### 2. Use in Tests

```python
from team_alpha.test_data import load_product_data

def test_macbook_search():
    data = load_product_data("macbook_pro_m3")
    search_page.search(data.search_term)
```

## Data Classes

### ProductData

```python
@dataclass
class ProductData:
    search_term: str              # Search query
    expected_keywords: List[str]  # Expected keywords in results
    min_price: float              # Minimum price
    max_price: float              # Maximum price
    description: str              # Product description
```

### ResultCountConfig

```python
@dataclass
class ResultCountConfig:
    minimum_results: int          # Min expected results
    maximum_results: int          # Max expected results
```

### TestConfig

```python
@dataclass
class TestConfig:
    timeout: int                  # Test timeout in seconds
    retry_attempts: int           # Number of retries
    wait_for_results: int         # Wait time for results
```

## Benefits

- ✅ **No hardcoded data** - All test data in YAML files
- ✅ **Type safety** - Data classes with type hints
- ✅ **Reusability** - Share data across multiple tests
- ✅ **Easy maintenance** - Update YAML without touching code
- ✅ **Validation** - Data class validation catches errors early
- ✅ **IDE support** - Full autocomplete and type checking
- ✅ **Documentation** - Self-documenting with clear structure

## File Format

YAML files should follow this structure:

```yaml
# Product test data
products:
  product_key:
    search_term: "search query"
    expected_keywords:
      - "keyword1"
      - "keyword2"
    min_price: 100
    max_price: 500
    description: "Product description"

# Configuration
result_counts:
  minimum_results: 3
  maximum_results: 100

config:
  timeout: 30
  retry_attempts: 3
  wait_for_results: 5
```
