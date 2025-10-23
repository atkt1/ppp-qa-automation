"""
API Tests for ReqRes API (https://reqres.in/)

Tests cover user management, authentication, and resource endpoints.
"""

import pytest
import allure
from playwright.sync_api import APIRequestContext
from team_alpha.api_clients.reqres_api_client import ReqResApiClient
from core.logger import log


@pytest.mark.team_alpha
@pytest.mark.api
@allure.feature("ReqRes API")
class TestReqResUserAPI:
    """Tests for ReqRes user management endpoints."""

    @pytest.mark.smoke
    @allure.story("User List")
    @allure.title("Get list of users from ReqRes API")
    def test_get_users_list(self, api_request_context: APIRequestContext):
        """
        Test getting paginated list of users.

        Validates:
        - Response status is 200
        - Response contains expected data structure
        - User list is not empty
        - Pagination data is present
        """
        client = ReqResApiClient(api_request_context)

        response = client.get_users(page=2)

        assert response.ok, f"Expected status 200, got {response.status}"
        assert response.status == 200

        body = response.json()
        log.info(f"Response body: {body}")

        # Validate response structure
        assert "page" in body, "Response should contain 'page' field"
        assert "data" in body, "Response should contain 'data' field"
        assert "total" in body, "Response should contain 'total' field"
        assert "total_pages" in body, "Response should contain 'total_pages' field"

        # Validate data
        assert body["page"] == 2, "Page number should be 2"
        assert len(body["data"]) > 0, "User list should not be empty"
        assert body["total"] > 0, "Total users should be greater than 0"

        # Validate first user structure
        first_user = body["data"][0]
        assert "id" in first_user, "User should have 'id' field"
        assert "email" in first_user, "User should have 'email' field"
        assert "first_name" in first_user, "User should have 'first_name' field"
        assert "last_name" in first_user, "User should have 'last_name' field"

    @pytest.mark.smoke
    @allure.story("User Creation")
    @allure.title("Create new user via ReqRes API")
    def test_create_user(self, api_request_context: APIRequestContext):
        """
        Test creating a new user.

        Validates:
        - Response status is 201
        - Response contains user data
        - Response includes id and createdAt timestamp
        """
        client = ReqResApiClient(api_request_context)

        name = "John Doe"
        job = "QA Engineer"

        response = client.create_user(name=name, job=job)

        assert response.ok, f"Expected status 201, got {response.status}"
        assert response.status == 201

        body = response.json()
        log.info(f"Created user: {body}")

        # Validate response contains submitted data
        assert body["name"] == name, f"Expected name '{name}', got '{body['name']}'"
        assert body["job"] == job, f"Expected job '{job}', got '{body['job']}'"

        # Validate response contains server-generated fields
        assert "id" in body, "Response should contain 'id' field"
        assert "createdAt" in body, "Response should contain 'createdAt' field"

    @allure.story("User Update")
    @allure.title("Update existing user via ReqRes API")
    def test_update_user(self, api_request_context: APIRequestContext):
        """
        Test updating an existing user.

        Validates:
        - Response status is 200
        - Response contains updated data
        - Response includes updatedAt timestamp
        """
        client = ReqResApiClient(api_request_context)

        user_id = 2
        updated_name = "Jane Smith"
        updated_job = "Senior QA Engineer"

        response = client.update_user(user_id=user_id, name=updated_name, job=updated_job)

        assert response.ok, f"Expected status 200, got {response.status}"
        assert response.status == 200

        body = response.json()
        log.info(f"Updated user: {body}")

        # Validate response contains updated data
        assert body["name"] == updated_name, f"Expected name '{updated_name}', got '{body['name']}'"
        assert body["job"] == updated_job, f"Expected job '{updated_job}', got '{body['job']}'"

        # Validate response contains server-generated fields
        assert "updatedAt" in body, "Response should contain 'updatedAt' field"

    @allure.story("User Deletion")
    @allure.title("Delete user via ReqRes API")
    def test_delete_user(self, api_request_context: APIRequestContext):
        """
        Test deleting a user.

        Validates:
        - Response status is 204 (No Content)
        """
        client = ReqResApiClient(api_request_context)

        user_id = 2

        response = client.delete_user(user_id=user_id)

        assert response.status == 204, f"Expected status 204, got {response.status}"
        log.info(f"Successfully deleted user {user_id}")


@pytest.mark.team_alpha
@pytest.mark.api
@allure.feature("ReqRes API")
class TestReqResAuthAPI:
    """Tests for ReqRes authentication endpoints."""

    @pytest.mark.smoke
    @allure.story("User Registration")
    @allure.title("Register new user via ReqRes API")
    def test_register_user_success(self, api_request_context: APIRequestContext):
        """
        Test successful user registration.

        Validates:
        - Response status is 200
        - Response contains id and token
        """
        client = ReqResApiClient(api_request_context)

        # ReqRes only accepts specific test emails
        email = "eve.holt@reqres.in"
        password = "pistol"

        response = client.register_user(email=email, password=password)

        assert response.ok, f"Expected status 200, got {response.status}"
        assert response.status == 200

        body = response.json()
        log.info(f"Registration response: {body}")

        # Validate response contains required fields
        assert "id" in body, "Response should contain 'id' field"
        assert "token" in body, "Response should contain 'token' field"
        assert isinstance(body["id"], int), "ID should be an integer"
        assert len(body["token"]) > 0, "Token should not be empty"

    @allure.story("User Registration")
    @allure.title("Register user with missing password - should fail")
    def test_register_user_failure(self, api_request_context: APIRequestContext):
        """
        Test registration failure when password is missing.

        Validates:
        - Response status is 400
        - Response contains error message
        """
        client = ReqResApiClient(api_request_context)

        email = "eve.holt@reqres.in"
        password = ""  # Missing password

        response = client.register_user(email=email, password=password)

        assert response.status == 400, f"Expected status 400, got {response.status}"

        body = response.json()
        log.info(f"Registration error: {body}")

        # Validate error response
        assert "error" in body, "Response should contain 'error' field"

    @pytest.mark.smoke
    @allure.story("User Login")
    @allure.title("Login user via ReqRes API")
    def test_login_user_success(self, api_request_context: APIRequestContext):
        """
        Test successful user login.

        Validates:
        - Response status is 200
        - Response contains token
        """
        client = ReqResApiClient(api_request_context)

        # ReqRes only accepts specific test emails
        email = "eve.holt@reqres.in"
        password = "cityslicka"

        response = client.login_user(email=email, password=password)

        assert response.ok, f"Expected status 200, got {response.status}"
        assert response.status == 200

        body = response.json()
        log.info(f"Login response: {body}")

        # Validate response contains token
        assert "token" in body, "Response should contain 'token' field"
        assert len(body["token"]) > 0, "Token should not be empty"


@pytest.mark.team_alpha
@pytest.mark.api
@allure.feature("ReqRes API")
class TestReqResResourceAPI:
    """Tests for ReqRes resource endpoints."""

    @allure.story("Resources")
    @allure.title("Get list of resources from ReqRes API")
    def test_get_resources_list(self, api_request_context: APIRequestContext):
        """
        Test getting list of resources.

        Validates:
        - Response status is 200
        - Response contains resources data
        - Resource list is not empty
        """
        client = ReqResApiClient(api_request_context)

        response = client.get_resources()

        assert response.ok, f"Expected status 200, got {response.status}"
        assert response.status == 200

        body = response.json()
        log.info(f"Resources response: {body}")

        # Validate response structure
        assert "data" in body, "Response should contain 'data' field"
        assert len(body["data"]) > 0, "Resource list should not be empty"

        # Validate first resource structure
        first_resource = body["data"][0]
        assert "id" in first_resource, "Resource should have 'id' field"
        assert "name" in first_resource, "Resource should have 'name' field"
        assert "year" in first_resource, "Resource should have 'year' field"
        assert "color" in first_resource, "Resource should have 'color' field"

    @allure.story("Resources")
    @allure.title("Get single resource by ID from ReqRes API")
    def test_get_single_resource(self, api_request_context: APIRequestContext):
        """
        Test getting a single resource by ID.

        Validates:
        - Response status is 200
        - Response contains resource data
        - Resource has expected fields
        """
        client = ReqResApiClient(api_request_context)

        resource_id = 2

        response = client.get_resource(resource_id=resource_id)

        assert response.ok, f"Expected status 200, got {response.status}"
        assert response.status == 200

        body = response.json()
        log.info(f"Resource response: {body}")

        # Validate response structure
        assert "data" in body, "Response should contain 'data' field"

        resource = body["data"]
        assert resource["id"] == resource_id, f"Expected id {resource_id}, got {resource['id']}"
        assert "name" in resource, "Resource should have 'name' field"
        assert "year" in resource, "Resource should have 'year' field"
        assert "color" in resource, "Resource should have 'color' field"
        assert "pantone_value" in resource, "Resource should have 'pantone_value' field"
