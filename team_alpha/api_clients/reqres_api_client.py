import allure
from playwright.sync_api import APIRequestContext, APIResponse

from core.base.api_client import BaseApiClient
from core.logger import log


class ReqResApiClient(BaseApiClient):
    """
    API Client for ReqRes API (https://reqres.in/).

    ReqRes is a hosted REST API for testing and prototyping.
    """

    def __init__(self, request_context: APIRequestContext):
        super().__init__(request_context)

    @allure.step("Get list of users (page {page})")
    def get_users(self, page: int = 1) -> APIResponse:
        """
        Get a list of users.

        Args:
            page: Page number (default: 1)

        Returns:
            APIResponse with user list
        """
        log.info(f"Getting users list - page {page}")
        return self.get(f"/api/users?page={page}")

    @allure.step("Get single user with ID: {user_id}")
    def get_user(self, user_id: int) -> APIResponse:
        """
        Get a single user by ID.

        Args:
            user_id: User ID

        Returns:
            APIResponse with user details
        """
        log.info(f"Getting user with ID: {user_id}")
        return self.get(f"/api/users/{user_id}")

    @allure.step("Create new user")
    def create_user(self, name: str, job: str) -> APIResponse:
        """
        Create a new user.

        Args:
            name: User's name
            job: User's job title

        Returns:
            APIResponse with created user data
        """
        log.info(f"Creating new user: {name}, Job: {job}")
        payload = {"name": name, "job": job}
        return self.post("/api/users", data=payload)

    @allure.step("Update user {user_id}")
    def update_user(self, user_id: int, name: str, job: str) -> APIResponse:
        """
        Update an existing user.

        Args:
            user_id: User ID to update
            name: Updated name
            job: Updated job title

        Returns:
            APIResponse with updated user data
        """
        log.info(f"Updating user {user_id}: {name}, Job: {job}")
        payload = {"name": name, "job": job}
        return self.put(f"/api/users/{user_id}", data=payload)

    @allure.step("Delete user {user_id}")
    def delete_user(self, user_id: int) -> APIResponse:
        """
        Delete a user.

        Args:
            user_id: User ID to delete

        Returns:
            APIResponse (204 No Content on success)
        """
        log.info(f"Deleting user {user_id}")
        return self.delete(f"/api/users/{user_id}")

    @allure.step("Register user")
    def register_user(self, email: str, password: str) -> APIResponse:
        """
        Register a new user.

        Args:
            email: User email
            password: User password

        Returns:
            APIResponse with registration token
        """
        log.info(f"Registering user: {email}")
        payload = {"email": email, "password": password}
        return self.post("/api/register", data=payload)

    @allure.step("Login user")
    def login_user(self, email: str, password: str) -> APIResponse:
        """
        Login a user.

        Args:
            email: User email
            password: User password

        Returns:
            APIResponse with auth token
        """
        log.info(f"Logging in user: {email}")
        payload = {"email": email, "password": password}
        return self.post("/api/login", data=payload)

    @allure.step("Get list of resources")
    def get_resources(self) -> APIResponse:
        """
        Get list of resources (colors).

        Returns:
            APIResponse with resource list
        """
        log.info("Getting resources list")
        return self.get("/api/unknown")

    @allure.step("Get resource with ID: {resource_id}")
    def get_resource(self, resource_id: int) -> APIResponse:
        """
        Get a single resource by ID.

        Args:
            resource_id: Resource ID

        Returns:
            APIResponse with resource details
        """
        log.info(f"Getting resource with ID: {resource_id}")
        return self.get(f"/api/unknown/{resource_id}")
