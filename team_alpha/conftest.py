import pytest
from playwright.sync_api import APIRequestContext
from team_alpha.api_clients.reqres_api_client import ReqResApiClient
from core.logger import log

# Note: Fixtures from core/conftest.py are automatically discovered by pytest
# No manual imports needed in simplified structure!


@pytest.fixture(scope="function")
def reqres_api_client(api_request_context: APIRequestContext) -> ReqResApiClient:
    """
    Fixture that provides a ReqResApiClient instance.

    Args:
        api_request_context: API request context

    Returns:
        ReqResApiClient object ready to use
    """
    return ReqResApiClient(api_request_context)


@pytest.fixture(scope="function", autouse=True)
def log_test_info(request):
    """
    Automatically log test information for Team Alpha tests.

    This fixture runs automatically for all tests in this module and overrides
    the basic test_logging fixture from core conftest with more detailed logging.
    """
    test_name = request.node.name
    test_module = request.node.module.__name__

    log.info("=" * 80)
    log.info(f"TEAM ALPHA TEST: {test_module}::{test_name}")
    log.info("=" * 80)

    yield

    log.info(f"COMPLETED: {test_name}")
    log.info("=" * 80)