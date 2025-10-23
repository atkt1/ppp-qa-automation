from playwright.sync_api import Page, Locator, expect
from core.logger import log


class BasePage:
    """
    Base class for all Page Object Models.
    
    Provides common functionality and utilities for page interactions.
    """
    
    def __init__(self, page: Page):
        self.page = page
    
    def navigate(self, url: str):
        """Navigate to a specific URL."""
        log.info(f"Navigating to: {url}")
        self.page.goto(url)
    
    def get_title(self) -> str:
        """Get the current page title."""
        return self.page.title()
    
    def get_url(self) -> str:
        """Get the current URL."""
        return self.page.url
    
    def wait_for_url(self, url: str, timeout: int = 30000):
        """Wait for URL to match a pattern."""
        log.info(f"Waiting for URL to match: {url}")
        self.page.wait_for_url(url, timeout=timeout)
    
    def wait_for_element(self, selector: str, timeout: int = 30000) -> Locator:
        """Wait for element to be visible."""
        log.debug(f"Waiting for element: {selector}")
        locator = self.page.locator(selector)
        locator.wait_for(state="visible", timeout=timeout)
        return locator
    
    def click(self, selector: str):
        """Click on an element."""
        log.debug(f"Clicking element: {selector}")
        self.page.locator(selector).click()
    
    def fill(self, selector: str, text: str):
        """Fill input field with text."""
        log.debug(f"Filling {selector} with: {text}")
        self.page.locator(selector).fill(text)
    
    def get_text(self, selector: str) -> str:
        """Get text content of an element."""
        return self.page.locator(selector).text_content()
    
    def is_visible(self, selector: str) -> bool:
        """Check if element is visible."""
        return self.page.locator(selector).is_visible()
    
    def scroll_to_element(self, selector: str):
        """Scroll element into view."""
        log.debug(f"Scrolling to element: {selector}")
        self.page.locator(selector).scroll_into_view_if_needed()
    
    def take_screenshot(self, name: str):
        """Take a screenshot of the current page."""
        import os
        screenshot_dir = "screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        path = f"{screenshot_dir}/{name}.png"
        self.page.screenshot(path=path, full_page=True)
        log.info(f"Screenshot saved: {path}")
        return path
    
    def reload(self):
        """Reload the current page."""
        log.info("Reloading page")
        self.page.reload()
    
    def go_back(self):
        """Navigate back in browser history."""
        log.info("Navigating back")
        self.page.go_back()
    
    def wait_for_load_state(self, state: str = "load"):
        """
        Wait for page to reach a specific load state.
        
        Args:
            state: 'load', 'domcontentloaded', or 'networkidle'
        """
        log.debug(f"Waiting for load state: {state}")
        self.page.wait_for_load_state(state)