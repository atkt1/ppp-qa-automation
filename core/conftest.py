import os
from typing import Generator

import pytest
from playwright.sync_api import APIRequestContext, BrowserContext, Playwright

from core.config import config
from core.logger import log


@pytest.fixture(scope="session")
def api_request_context(
    playwright: Playwright,
) -> Generator[APIRequestContext, None, None]:
    """
    Session-scoped API request context with authentication headers.

    This fixture creates a persistent API context that can be used across
    all tests in a session, reducing setup overhead.
    """
    log.info(f"Creating API request context for {config.api_base_url}")

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    # Add API key header if token is provided
    # Using X-API-Key header format (used by ReqRes and many APIs)
    if config.api_auth_token:
        headers["X-API-Key"] = config.api_auth_token

    request_context = playwright.request.new_context(base_url=config.api_base_url, extra_http_headers=headers)

    yield request_context

    log.info("Disposing API request context")
    request_context.dispose()


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict) -> dict:
    """
    Fixture to configure browser launch arguments.

    Adds flags to launch browser in maximized/fullscreen mode.
    In headless mode, uses --window-size to set viewport.
    In headed mode, uses --start-maximized.
    """
    args = []

    if config.headless:
        # In headless mode, set explicit window size (maximized dimensions)
        args.extend(
            [
                "--window-size=1920,1080",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ]
        )
    else:
        # In headed mode, maximize the window
        args.append("--start-maximized")

    return {
        **browser_type_launch_args,
        "args": args,
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    """
    Fixture to configure browser context arguments for UI tests.

    This allows global configuration of browser settings like viewport,
    video recording, and more.
    - In headed mode: no_viewport=True allows browser to use full maximized window
    - In headless mode: explicit viewport size is set to 1920x1080
    Video recording works in both headed and headless modes.
    """
    context_args = {
        **browser_context_args,
    }

    # Configure viewport based on headless mode
    if config.headless:
        # In headless mode, set explicit viewport size
        context_args["viewport"] = {"width": 1920, "height": 1080}
        log.info("Headless mode: viewport set to 1920x1080")
    else:
        # In headed mode, use full window size (maximized)
        context_args["no_viewport"] = True
        log.info("Headed mode: using maximized window")

    # Add video recording if enabled (works in both headed and headless mode)
    if config.record_video:
        context_args["record_video_dir"] = "videos/"
        context_args["record_video_size"] = {"width": 1920, "height": 1080}
        log.info("Video recording enabled - videos will be saved to videos/ directory")

    return context_args


@pytest.fixture(scope="function")
def page(context: BrowserContext):
    """
    Function-scoped page fixture with enhanced error handling and logging.

    Each test gets a fresh page instance.
    """
    page = context.new_page()
    page.set_default_timeout(30000)  # 30 seconds default timeout

    # Log navigation events
    page.on("console", lambda msg: log.debug(f"Browser console: {msg.text}"))

    yield page

    # Cleanup
    page.close()


@pytest.fixture(scope="function", autouse=True)
def test_logging(request):
    """
    Automatically log test start and end for every test.
    Note: Team-specific conftest files may override this with more detailed logging.
    """
    test_name = request.node.name
    log.info(f"Starting test: {test_name}")

    yield

    log.info(f"Completed test: {test_name}")


@pytest.fixture(scope="function")
def take_screenshot(page):
    """
    Fixture to easily capture screenshots on demand.
    """

    def _screenshot(name: str):
        screenshot_dir = "screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        path = f"{screenshot_dir}/{name}.png"
        page.screenshot(path=path, full_page=True)
        log.info(f"Screenshot saved: {path}")
        return path

    return _screenshot


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test failures and take screenshots automatically.
    """
    outcome = yield
    rep = outcome.get_result()

    # Check if test failed and has a page fixture
    if rep.when == "call" and rep.failed:
        if "page" in item.fixturenames:
            page = item.funcargs.get("page")
            if page:
                screenshot_dir = "screenshots"
                os.makedirs(screenshot_dir, exist_ok=True)
                screenshot_path = f"{screenshot_dir}/failure_{item.name}.png"
                try:
                    page.screenshot(path=screenshot_path, full_page=True)
                    log.error(f"Test failed. Screenshot saved: {screenshot_path}")
                except Exception as e:
                    log.error(f"Failed to capture screenshot: {e}")
