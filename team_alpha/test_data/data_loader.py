"""
Test Data Loader for Team Alpha

This module provides utilities for loading test data from YAML files.
Uses the generic BaseYamlDataLoader with type-safe data classes.

Usage:
    from team_alpha.test_data import load_product_data, get_all_products

    # Load specific product data
    samsung_data = load_product_data("samsung_s24_ultra")
    search_page.search(samsung_data.search_term)

    # Get all products for parametrized testing
    products = get_all_products()
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from core.data import BaseYamlDataLoader


@dataclass
class ProductData:
    """
    Data class representing product test data.

    Attributes:
        search_term: The search query to use
        expected_keywords: List of keywords expected in results
        min_price: Minimum expected price
        max_price: Maximum expected price
        description: Product description for documentation
    """

    search_term: str
    expected_keywords: List[str]
    min_price: float
    max_price: float
    description: str


@dataclass
class ResultCountConfig:
    """Configuration for expected result counts."""

    minimum_results: int
    maximum_results: int


@dataclass
class TestConfig:
    """General test configuration settings."""

    timeout: int
    retry_attempts: int
    wait_for_results: int


class TeamAlphaDataLoader(BaseYamlDataLoader):
    """
    Team Alpha specific data loader.

    Extends BaseYamlDataLoader with Team Alpha's data structures.
    """

    def __init__(self):
        """Initialize with Team Alpha's YAML file."""
        yaml_file = Path(__file__).parent / "google_shopping.yaml"
        super().__init__(yaml_file)

    def get_product(self, product_key: str) -> ProductData:
        """
        Get product data by key.

        Args:
            product_key: The product identifier (e.g., 'samsung_s24_ultra')

        Returns:
            ProductData object with product information

        Raises:
            KeyError: If product_key is not found in test data
        """
        product = self.get_section_item("products", product_key)
        return ProductData(**product)

    def get_all_products(self) -> Dict[str, ProductData]:
        """
        Get all products as a dictionary.

        Returns:
            Dictionary mapping product keys to ProductData objects
        """
        all_products = self.get_all_section_items("products")
        return {key: ProductData(**value) for key, value in all_products.items()}

    def get_result_count_config(self) -> ResultCountConfig:
        """Get result count configuration."""
        config_data = self.get_section("result_counts")
        return ResultCountConfig(**config_data)

    def get_test_config(self) -> TestConfig:
        """Get general test configuration."""
        config_data = self.get_section("config")
        return TestConfig(**config_data)


# Singleton instance
_loader = TeamAlphaDataLoader()


# Convenience functions for direct access
def load_product_data(product_key: str) -> ProductData:
    """
    Load product test data by key.

    Args:
        product_key: The product identifier (e.g., 'samsung_s24_ultra')

    Returns:
        ProductData object

    Example:
        >>> data = load_product_data("samsung_s24_ultra")
        >>> print(data.search_term)
        'samsung s24 ultra'
        >>> print(data.min_price)
        800
    """
    return _loader.get_product(product_key)


def get_all_products() -> Dict[str, ProductData]:
    """
    Get all product test data.

    Returns:
        Dictionary of product_key -> ProductData

    Example:
        >>> products = get_all_products()
        >>> for key, data in products.items():
        ...     print(f"{key}: {data.search_term}")
    """
    return _loader.get_all_products()


def get_result_config() -> ResultCountConfig:
    """Get result count configuration."""
    return _loader.get_result_count_config()


def get_test_config() -> TestConfig:
    """Get general test configuration."""
    return _loader.get_test_config()


def list_available_products() -> List[str]:
    """
    List all available product keys.

    Returns:
        List of product identifiers

    Example:
        >>> products = list_available_products()
        >>> print(products)
        ['samsung_s24_ultra', 'iphone_15_pro', 'pixel_8_pro']
    """
    return _loader.list_section_items("products")
