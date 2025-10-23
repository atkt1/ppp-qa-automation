"""
Wait and Retry Utilities

Common wait and retry patterns for test automation:
- Retry functions with exponential backoff
- Wait for conditions with timeout
- Decorators for automatic retry

Usage:
    from core.utils import wait_with_retry, retry_on_exception

    # Retry a function
    result = wait_with_retry(lambda: get_data(), max_attempts=3)

    # Use as decorator
    @retry_on_exception(max_attempts=3)
    def flaky_operation():
        pass
"""

import time
from typing import Callable, Any, TypeVar, Optional, Tuple
from functools import wraps
from core.logger import log


T = TypeVar('T')


def wait_with_retry(
    func: Callable[[], T],
    max_attempts: int = 3,
    wait_time: float = 2.0,
    exponential_backoff: bool = False,
    exceptions: Tuple[type, ...] = (Exception,),
    on_retry: Optional[Callable[[int, Exception], None]] = None
) -> T:
    """
    Execute function with retry logic.

    Common pattern for handling flaky operations like:
    - Web element interactions
    - API calls
    - Database queries

    Args:
        func: Function to execute (must take no arguments)
        max_attempts: Maximum number of attempts
        wait_time: Base wait time between attempts in seconds
        exponential_backoff: If True, double wait time after each failure
        exceptions: Tuple of exceptions to catch and retry
        on_retry: Optional callback function(attempt_number, exception)

    Returns:
        Result from successful function execution

    Raises:
        Last exception if all attempts fail

    Examples:
        >>> # Simple retry
        >>> result = wait_with_retry(lambda: get_element())

        >>> # Retry with exponential backoff
        >>> result = wait_with_retry(
        ...     lambda: api_call(),
        ...     max_attempts=5,
        ...     wait_time=1.0,
        ...     exponential_backoff=True
        ... )

        >>> # Retry with custom exception handling
        >>> def log_retry(attempt, exc):
        ...     print(f"Attempt {attempt} failed: {exc}")
        >>> result = wait_with_retry(
        ...     lambda: flaky_operation(),
        ...     on_retry=log_retry
        ... )
    """
    current_wait = wait_time

    for attempt in range(1, max_attempts + 1):
        try:
            log.debug(f"Attempt {attempt}/{max_attempts}")
            result = func()
            if attempt > 1:
                log.info(f"Operation succeeded on attempt {attempt}")
            return result

        except exceptions as e:
            if attempt == max_attempts:
                log.error(f"All {max_attempts} attempts failed")
                raise

            log.warning(f"Attempt {attempt} failed: {type(e).__name__}: {str(e)}")

            # Call retry callback if provided
            if on_retry:
                try:
                    on_retry(attempt, e)
                except Exception as callback_error:
                    log.error(f"Retry callback error: {callback_error}")

            # Wait before next attempt
            log.debug(f"Waiting {current_wait}s before retry...")
            time.sleep(current_wait)

            # Apply exponential backoff if enabled
            if exponential_backoff:
                current_wait *= 2


def retry_on_exception(
    max_attempts: int = 3,
    wait_time: float = 2.0,
    exponential_backoff: bool = False,
    exceptions: Tuple[type, ...] = (Exception,),
    log_attempts: bool = True
) -> Callable:
    """
    Decorator to automatically retry a function on exception.

    Args:
        max_attempts: Maximum number of attempts
        wait_time: Base wait time between attempts
        exponential_backoff: If True, double wait time after each failure
        exceptions: Tuple of exceptions to catch and retry
        log_attempts: If True, log each attempt

    Returns:
        Decorated function

    Examples:
        >>> @retry_on_exception(max_attempts=3, wait_time=1.0)
        ... def fetch_data():
        ...     return api.get_data()

        >>> @retry_on_exception(max_attempts=5, exponential_backoff=True)
        ... def click_element(locator):
        ...     element.click()
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            current_wait = wait_time

            for attempt in range(1, max_attempts + 1):
                try:
                    if log_attempts and attempt > 1:
                        log.info(f"{func.__name__}: Attempt {attempt}/{max_attempts}")

                    result = func(*args, **kwargs)

                    if attempt > 1 and log_attempts:
                        log.info(f"{func.__name__}: Succeeded on attempt {attempt}")

                    return result

                except exceptions as e:
                    if attempt == max_attempts:
                        if log_attempts:
                            log.error(f"{func.__name__}: All {max_attempts} attempts failed")
                        raise

                    if log_attempts:
                        log.warning(
                            f"{func.__name__}: Attempt {attempt} failed: "
                            f"{type(e).__name__}: {str(e)}"
                        )

                    time.sleep(current_wait)

                    if exponential_backoff:
                        current_wait *= 2

        return wrapper
    return decorator


def wait_for_condition(
    condition_func: Callable[[], bool],
    timeout: float = 30.0,
    poll_interval: float = 0.5,
    error_message: str = "Condition not met within timeout",
    suppress_errors: bool = True
) -> bool:
    """
    Wait for a condition to become true.

    Polls condition function at regular intervals until it returns True
    or timeout is reached.

    Args:
        condition_func: Function that returns True when condition is met
        timeout: Maximum time to wait in seconds
        poll_interval: Time between condition checks in seconds
        error_message: Error message if timeout occurs
        suppress_errors: If True, suppress exceptions from condition_func

    Returns:
        True if condition met before timeout

    Raises:
        TimeoutError: If condition not met within timeout

    Examples:
        >>> # Wait for element to be visible
        >>> wait_for_condition(
        ...     lambda: element.is_visible(),
        ...     timeout=10.0
        ... )

        >>> # Wait for API status
        >>> wait_for_condition(
        ...     lambda: api.get_status() == "ready",
        ...     timeout=30.0,
        ...     poll_interval=2.0
        ... )

        >>> # Wait with custom error
        >>> wait_for_condition(
        ...     lambda: len(items) > 0,
        ...     error_message="No items found after waiting"
        ... )
    """
    start_time = time.time()
    elapsed = 0.0

    log.debug(f"Waiting for condition (timeout: {timeout}s)")

    while elapsed < timeout:
        try:
            if condition_func():
                log.debug(f"Condition met after {elapsed:.2f}s")
                return True
        except Exception as e:
            if not suppress_errors:
                raise
            log.debug(f"Condition check raised exception: {type(e).__name__}: {str(e)}")

        time.sleep(poll_interval)
        elapsed = time.time() - start_time

    # Timeout reached
    log.error(f"Timeout after {elapsed:.2f}s: {error_message}")
    raise TimeoutError(f"{error_message} (timeout: {timeout}s)")


def wait_for_value_change(
    get_value_func: Callable[[], Any],
    initial_value: Any = None,
    timeout: float = 30.0,
    poll_interval: float = 0.5,
    error_message: str = "Value did not change within timeout"
) -> Any:
    """
    Wait for a value to change from its initial value.

    Useful for waiting for state changes, counter updates, etc.

    Args:
        get_value_func: Function that returns the current value
        initial_value: Initial value to compare against (if None, fetch it first)
        timeout: Maximum time to wait in seconds
        poll_interval: Time between checks in seconds
        error_message: Error message if timeout occurs

    Returns:
        New value after change

    Raises:
        TimeoutError: If value doesn't change within timeout

    Examples:
        >>> # Wait for counter to change
        >>> new_count = wait_for_value_change(
        ...     lambda: page.get_item_count()
        ... )

        >>> # Wait for status to change from specific value
        >>> new_status = wait_for_value_change(
        ...     lambda: api.get_status(),
        ...     initial_value="pending"
        ... )
    """
    # Get initial value if not provided
    if initial_value is None:
        initial_value = get_value_func()
        log.debug(f"Initial value: {initial_value}")

    def condition():
        current = get_value_func()
        return current != initial_value

    # Wait for value to change
    wait_for_condition(
        condition,
        timeout=timeout,
        poll_interval=poll_interval,
        error_message=error_message
    )

    # Return new value
    return get_value_func()


def retry_with_timeout(
    func: Callable[[], T],
    timeout: float = 30.0,
    retry_interval: float = 1.0,
    exceptions: Tuple[type, ...] = (Exception,)
) -> T:
    """
    Retry function until it succeeds or timeout is reached.

    Similar to wait_with_retry but uses timeout instead of max_attempts.

    Args:
        func: Function to execute
        timeout: Maximum time to keep trying in seconds
        retry_interval: Time between retry attempts in seconds
        exceptions: Tuple of exceptions to catch and retry

    Returns:
        Result from successful function execution

    Raises:
        TimeoutError: If timeout reached without success
        Other exceptions: If non-retryable exception occurs

    Examples:
        >>> result = retry_with_timeout(
        ...     lambda: get_data(),
        ...     timeout=60.0,
        ...     retry_interval=5.0
        ... )
    """
    start_time = time.time()
    last_exception = None
    attempt = 0

    while time.time() - start_time < timeout:
        attempt += 1
        try:
            log.debug(f"Retry attempt {attempt}")
            return func()
        except exceptions as e:
            last_exception = e
            elapsed = time.time() - start_time
            remaining = timeout - elapsed

            if remaining <= 0:
                break

            log.debug(f"Attempt failed: {type(e).__name__}, retrying...")
            time.sleep(min(retry_interval, remaining))

    # Timeout reached
    error_msg = f"Operation timed out after {timeout}s and {attempt} attempts"
    if last_exception:
        error_msg += f" (last error: {type(last_exception).__name__}: {str(last_exception)})"

    log.error(error_msg)
    raise TimeoutError(error_msg)


def exponential_backoff_wait(attempt: int, base_wait: float = 1.0, max_wait: float = 30.0) -> float:
    """
    Calculate wait time using exponential backoff.

    Useful for rate-limited APIs or when you want increasing delays.

    Args:
        attempt: Current attempt number (1-based)
        base_wait: Base wait time in seconds
        max_wait: Maximum wait time cap

    Returns:
        Wait time in seconds

    Examples:
        >>> exponential_backoff_wait(1)  # 1.0s
        >>> exponential_backoff_wait(2)  # 2.0s
        >>> exponential_backoff_wait(3)  # 4.0s
        >>> exponential_backoff_wait(10)  # 30.0s (capped at max_wait)
    """
    wait_time = base_wait * (2 ** (attempt - 1))
    return min(wait_time, max_wait)
