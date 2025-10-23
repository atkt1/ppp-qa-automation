from typing import Optional, Dict, Any
from playwright.sync_api import APIRequestContext, APIResponse
from core.logger import log


class BaseApiClient:
    """
    Base class for all API clients.
    
    Provides common functionality for API interactions including
    request logging, response validation, and error handling.
    """
    
    def __init__(self, api_context: APIRequestContext):
        self.api_context = api_context
    
    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> APIResponse:
        """
        Send GET request.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            headers: Additional headers
        
        Returns:
            APIResponse object
        """
        log.info(f"GET request to: {endpoint}")
        if params:
            log.debug(f"Query params: {params}")
        
        response = self.api_context.get(
            endpoint,
            params=params,
            headers=headers
        )
        
        self._log_response(response)
        return response
    
    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> APIResponse:
        """
        Send POST request.
        
        Args:
            endpoint: API endpoint path
            data: Request body data
            headers: Additional headers
        
        Returns:
            APIResponse object
        """
        log.info(f"POST request to: {endpoint}")
        if data:
            log.debug(f"Request body: {data}")
        
        response = self.api_context.post(
            endpoint,
            data=data,
            headers=headers
        )
        
        self._log_response(response)
        return response
    
    def put(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> APIResponse:
        """
        Send PUT request.
        
        Args:
            endpoint: API endpoint path
            data: Request body data
            headers: Additional headers
        
        Returns:
            APIResponse object
        """
        log.info(f"PUT request to: {endpoint}")
        if data:
            log.debug(f"Request body: {data}")
        
        response = self.api_context.put(
            endpoint,
            data=data,
            headers=headers
        )
        
        self._log_response(response)
        return response
    
    def patch(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> APIResponse:
        """
        Send PATCH request.
        
        Args:
            endpoint: API endpoint path
            data: Request body data
            headers: Additional headers
        
        Returns:
            APIResponse object
        """
        log.info(f"PATCH request to: {endpoint}")
        if data:
            log.debug(f"Request body: {data}")
        
        response = self.api_context.patch(
            endpoint,
            data=data,
            headers=headers
        )
        
        self._log_response(response)
        return response
    
    def delete(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None
    ) -> APIResponse:
        """
        Send DELETE request.
        
        Args:
            endpoint: API endpoint path
            headers: Additional headers
        
        Returns:
            APIResponse object
        """
        log.info(f"DELETE request to: {endpoint}")
        
        response = self.api_context.delete(
            endpoint,
            headers=headers
        )
        
        self._log_response(response)
        return response
    
    def _log_response(self, response: APIResponse):
        """Log response details."""
        log.info(f"Response status: {response.status}")
        
        if not response.ok:
            log.error(f"Request failed with status {response.status}")
            log.error(f"Response body: {response.text()}")
    
    def assert_status_code(self, response: APIResponse, expected_status: int):
        """
        Assert response status code matches expected value.
        
        Args:
            response: API response
            expected_status: Expected HTTP status code
        """
        actual_status = response.status
        assert actual_status == expected_status, \
            f"Expected status {expected_status}, got {actual_status}. Response: {response.text()}"
        log.info(f"Status code assertion passed: {expected_status}")
    
    def get_json(self, response: APIResponse) -> Dict[str, Any]:
        """
        Get JSON response body.
        
        Args:
            response: API response
        
        Returns:
            Parsed JSON response
        """
        return response.json()