"""
Base classes for the test automation framework.

Provides foundational classes that should be extended by
team-specific implementations.
"""

from core.base.api_client import BaseApiClient
from core.base.page_base import BasePage

__all__ = ["BasePage", "BaseApiClient"]
