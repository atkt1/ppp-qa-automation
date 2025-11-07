"""
Core library for the test automation framework.

This package provides shared functionality for all teams including:
- Configuration management
- Logging utilities
- Base classes for page objects and API clients
- Common fixtures and utilities
"""

from core.config import config
from core.logger import log

__all__ = ["config", "log"]
