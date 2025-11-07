import os
from pathlib import Path

from dotenv import load_dotenv


class Config:
    """Singleton configuration class for the test framework."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """Load configuration from .env file."""
        # Load .env file from the project root
        # Search upwards from current file to find project root
        current = Path(__file__).resolve()
        for parent in current.parents:
            env_path = parent / ".env"
            if env_path.exists():
                load_dotenv(dotenv_path=env_path)
                break
        else:
            # Fallback: try loading from current working directory
            load_dotenv()

        # Environment settings
        self.env = os.getenv("ENV", "local")
        self.web_base_url = os.getenv("WEB_BASE_URL", "https://example.com")
        self.api_base_url = os.getenv("API_BASE_URL", "https://api.example.com")
        self.api_auth_token = os.getenv("API_AUTH_TOKEN", "")

        # Browser settings
        self.headless = os.getenv("HEADLESS", "true").lower() == "true"
        self.browser = os.getenv("BROWSER", "chromium")
        self.record_video = os.getenv("RECORD_VIDEO", "false").lower() == "true"

        # Test execution settings
        self.pytest_workers = os.getenv("PYTEST_WORKERS", "auto")

    def is_ci(self) -> bool:
        """Check if running in CI environment."""
        return os.getenv("CI", "false").lower() == "true"

    def get_base_url(self, service: str = "web") -> str:
        """Get base URL for a specific service."""
        if service == "api":
            return self.api_base_url
        return self.web_base_url


# Singleton instance
config = Config()
