"""
Team Alpha Test Data Package

Provides centralized test data management using YAML files.

Usage:
    from team_alpha.test_data import load_product_data, get_all_products

    # Load specific product
    samsung = load_product_data("samsung_s24_ultra")

    # Get all products
    products = get_all_products()
"""

from team_alpha.test_data.data_loader import (
    ProductData,
    ResultCountConfig,
    TestConfig,
    get_all_products,
    get_result_config,
    get_test_config,
    list_available_products,
    load_product_data,
)

__all__ = [
    "ProductData",
    "ResultCountConfig",
    "TestConfig",
    "load_product_data",
    "get_all_products",
    "get_result_config",
    "get_test_config",
    "list_available_products",
]
