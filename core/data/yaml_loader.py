"""
Generic YAML Data Loader

Base class for loading test data from YAML files.
Implements singleton pattern with caching for performance.

Each team can subclass this to create their own specialized data loaders.

Usage:
    # Team-specific implementation
    class MyTeamDataLoader(BaseYamlDataLoader):
        def __init__(self):
            yaml_file = Path(__file__).parent / "my_data.yaml"
            super().__init__(yaml_file)

        def get_user(self, key: str) -> UserData:
            data = self.get_section_item("users", key)
            return UserData(**data)

    # Use in tests
    loader = MyTeamDataLoader()
    user = loader.get_user("admin_user")
"""

import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from core.logger import log


class BaseYamlDataLoader:
    """
    Generic base class for YAML data loading with singleton pattern.

    Features:
    - Singleton pattern: One instance per subclass
    - Automatic caching: Data loaded once and cached
    - Generic accessors: Get data by section and key
    - Error handling: Clear error messages for missing data
    - Path flexibility: Accepts Path or string for YAML file

    Subclasses should:
    1. Call super().__init__(yaml_file_path) in their __init__
    2. Provide typed getter methods for their specific data structures
    """

    # Class-level cache for singleton instances per subclass
    _instances: Dict[type, 'BaseYamlDataLoader'] = {}
    _data_cache: Dict[type, Dict[str, Any]] = {}

    def __new__(cls, yaml_file: Optional[Path] = None):
        """
        Implement singleton pattern per subclass.
        Each subclass gets its own singleton instance.
        """
        if cls not in cls._instances:
            instance = super(BaseYamlDataLoader, cls).__new__(cls)
            cls._instances[cls] = instance
        return cls._instances[cls]

    def __init__(self, yaml_file: Union[Path, str]):
        """
        Initialize the YAML data loader.

        Args:
            yaml_file: Path to the YAML file to load
        """
        # Only load data once per class (singleton pattern)
        if type(self) not in self._data_cache:
            self.yaml_file = Path(yaml_file) if isinstance(yaml_file, str) else yaml_file
            self._load_data()

    def _load_data(self):
        """
        Load YAML data from file and cache it.

        Raises:
            FileNotFoundError: If YAML file doesn't exist
            yaml.YAMLError: If YAML file is malformed
        """
        if not self.yaml_file.exists():
            log.error(f"YAML file not found: {self.yaml_file}")
            raise FileNotFoundError(f"YAML file not found: {self.yaml_file}")

        log.info(f"Loading YAML data from: {self.yaml_file}")

        try:
            with open(self.yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            if data is None:
                log.warning(f"YAML file is empty: {self.yaml_file}")
                data = {}

            # Cache data at class level
            type(self)._data_cache[type(self)] = data
            log.info(f"Successfully loaded YAML data with {len(data)} top-level sections")

        except yaml.YAMLError as e:
            log.error(f"Error parsing YAML file: {e}")
            raise

    @property
    def data(self) -> Dict[str, Any]:
        """
        Get the cached data for this loader instance.

        Returns:
            Complete YAML data as dictionary
        """
        return type(self)._data_cache.get(type(self), {})

    def get_section(self, section_name: str) -> Dict[str, Any]:
        """
        Get an entire section from the YAML data.

        Args:
            section_name: Name of the top-level section

        Returns:
            Section data as dictionary

        Raises:
            KeyError: If section doesn't exist

        Example:
            >>> loader.get_section("users")
            {'admin': {...}, 'guest': {...}}
        """
        if section_name not in self.data:
            available = list(self.data.keys())
            raise KeyError(
                f"Section '{section_name}' not found in YAML. "
                f"Available sections: {', '.join(available)}"
            )

        return self.data[section_name]

    def get_section_item(self, section_name: str, item_key: str) -> Dict[str, Any]:
        """
        Get a specific item from a section.

        Args:
            section_name: Name of the section
            item_key: Key of the item within the section

        Returns:
            Item data as dictionary

        Raises:
            KeyError: If section or item doesn't exist

        Example:
            >>> loader.get_section_item("users", "admin")
            {'email': 'admin@example.com', 'role': 'admin'}
        """
        section = self.get_section(section_name)

        if item_key not in section:
            available = list(section.keys())
            raise KeyError(
                f"Item '{item_key}' not found in section '{section_name}'. "
                f"Available items: {', '.join(available)}"
            )

        return section[item_key]

    def get_all_section_items(self, section_name: str) -> Dict[str, Dict[str, Any]]:
        """
        Get all items from a section as a dictionary.

        Args:
            section_name: Name of the section

        Returns:
            Dictionary mapping item keys to item data

        Example:
            >>> loader.get_all_section_items("users")
            {'admin': {...}, 'guest': {...}}
        """
        return self.get_section(section_name)

    def list_sections(self) -> List[str]:
        """
        List all available top-level sections.

        Returns:
            List of section names

        Example:
            >>> loader.list_sections()
            ['users', 'products', 'config']
        """
        return list(self.data.keys())

    def list_section_items(self, section_name: str) -> List[str]:
        """
        List all item keys in a section.

        Args:
            section_name: Name of the section

        Returns:
            List of item keys

        Example:
            >>> loader.list_section_items("users")
            ['admin', 'guest', 'editor']
        """
        section = self.get_section(section_name)
        return list(section.keys())

    def has_section(self, section_name: str) -> bool:
        """
        Check if a section exists.

        Args:
            section_name: Name of the section

        Returns:
            True if section exists
        """
        return section_name in self.data

    def has_item(self, section_name: str, item_key: str) -> bool:
        """
        Check if an item exists in a section.

        Args:
            section_name: Name of the section
            item_key: Key of the item

        Returns:
            True if item exists
        """
        try:
            section = self.get_section(section_name)
            return item_key in section
        except KeyError:
            return False

    def get_config_value(self, *keys: str, default: Any = None) -> Any:
        """
        Get a configuration value using nested keys.
        Useful for accessing nested config like: config.api.timeout

        Args:
            *keys: Nested keys to traverse
            default: Default value if key path doesn't exist

        Returns:
            Configuration value or default

        Example:
            >>> loader.get_config_value("api", "timeout")
            30
            >>> loader.get_config_value("api", "retries", default=3)
            3
        """
        current = self.data

        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                log.debug(f"Config key path {'.'.join(keys)} not found, using default: {default}")
                return default

        return current

    def reload(self):
        """
        Force reload data from YAML file.
        Useful if file has been modified during test execution.
        """
        log.info(f"Reloading YAML data from: {self.yaml_file}")
        # Clear cache for this class
        if type(self) in type(self)._data_cache:
            del type(self)._data_cache[type(self)]
        # Reload data
        self._load_data()

    def __repr__(self) -> str:
        """String representation of the loader."""
        sections = ', '.join(self.list_sections())
        return f"{self.__class__.__name__}(file={self.yaml_file.name}, sections=[{sections}])"
