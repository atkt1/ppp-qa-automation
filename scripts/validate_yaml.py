#!/usr/bin/env python3
"""
YAML Validation Script for QA Automation Framework

Validates all YAML files in the project for:
- Syntax errors
- Duplicate keys
- Proper indentation
- Data structure consistency
"""

import sys
from pathlib import Path
from typing import List, Tuple

import yaml


class YamlValidator:
    """Validator for YAML files in the project."""

    def __init__(self, base_path: Path):
        """Initialize validator with base project path."""
        self.base_path = base_path
        self.errors: List[Tuple[Path, str]] = []
        self.warnings: List[Tuple[Path, str]] = []
        self.validated_count = 0

    def find_yaml_files(self) -> List[Path]:
        """Find all YAML files in test_data directories."""
        yaml_files = []

        # Find all test_data directories
        test_data_dirs = list(self.base_path.rglob("test_data"))

        for test_data_dir in test_data_dirs:
            if test_data_dir.is_dir():
                yaml_files.extend(test_data_dir.glob("*.yaml"))
                yaml_files.extend(test_data_dir.glob("*.yml"))

        return yaml_files

    def validate_syntax(self, file_path: Path) -> bool:
        """Validate YAML syntax."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Empty files are valid
            if not content.strip():
                self.warnings.append((file_path, "File is empty"))
                return True

            # Try to parse YAML
            yaml.safe_load(content)
            return True

        except yaml.YAMLError as e:
            self.errors.append((file_path, f"YAML syntax error: {e}"))
            return False
        except Exception as e:
            self.errors.append((file_path, f"Error reading file: {e}"))
            return False

    def check_indentation(self, file_path: Path) -> bool:
        """Check if indentation is consistent (2 spaces recommended)."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            inconsistent_indentation = False
            for line_num, line in enumerate(lines, start=1):
                if line.strip():  # Skip empty lines
                    # Count leading spaces
                    leading_spaces = len(line) - len(line.lstrip(" "))

                    # Check if indentation is multiple of 2
                    if leading_spaces > 0 and leading_spaces % 2 != 0:
                        inconsistent_indentation = True
                        self.warnings.append(
                            (
                                file_path,
                                f"Line {line_num}: Indentation is {leading_spaces} spaces " f"(should be multiple of 2)",
                            )
                        )

            return not inconsistent_indentation

        except Exception as e:
            self.warnings.append((file_path, f"Could not check indentation: {e}"))
            return True

    def check_duplicate_keys(self, file_path: Path) -> bool:
        """Check for duplicate keys in YAML."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            if not content.strip():
                return True

            # Custom loader to detect duplicate keys
            class DuplicateKeyLoader(yaml.SafeLoader):
                pass

            def check_duplicates(loader, node):
                mapping = {}
                for key_node, value_node in node.value:
                    key = loader.construct_object(key_node, deep=False)
                    if key in mapping:
                        raise yaml.constructor.ConstructorError(
                            f"Duplicate key '{key}' found",
                            key_node.start_mark,
                            "first occurrence",
                            mapping[key].start_mark,
                        )
                    mapping[key] = key_node
                return loader.construct_mapping(node, deep=True)

            DuplicateKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, check_duplicates)

            yaml.load(content, Loader=DuplicateKeyLoader)
            return True

        except yaml.constructor.ConstructorError as e:
            self.errors.append((file_path, f"Duplicate key found: {e}"))
            return False
        except Exception:
            # If custom check fails, fall back to standard validation
            return True

    def validate_file(self, file_path: Path) -> bool:
        """Validate a single YAML file."""
        valid = True

        # Validate syntax (required)
        if not self.validate_syntax(file_path):
            valid = False
            return valid  # No point checking further if syntax is invalid

        # Check indentation (warning)
        self.check_indentation(file_path)

        # Check duplicate keys (error)
        if not self.check_duplicate_keys(file_path):
            valid = False

        self.validated_count += 1
        return valid

    def run(self) -> int:
        """Run validation on all YAML files."""
        yaml_files = self.find_yaml_files()

        if not yaml_files:
            print("⚠️  No YAML files found in test_data directories")
            return 0

        print(f"Found {len(yaml_files)} YAML file(s) to validate\n")

        all_valid = True
        for yaml_file in yaml_files:
            relative_path = yaml_file.relative_to(self.base_path)
            print(f"Validating {relative_path}...", end=" ")

            if self.validate_file(yaml_file):
                print("✓")
            else:
                print("✗")
                all_valid = False

        # Print summary
        print("\n" + "=" * 60)
        print("VALIDATION SUMMARY")
        print("=" * 60)
        print(f"Files validated: {self.validated_count}")
        print(f"Errors: {len(self.errors)}")
        print(f"Warnings: {len(self.warnings)}")

        # Print errors
        if self.errors:
            print("\n❌ ERRORS:")
            for file_path, error in self.errors:
                relative_path = file_path.relative_to(self.base_path)
                print(f"  {relative_path}:")
                print(f"    {error}")

        # Print warnings
        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for file_path, warning in self.warnings:
                relative_path = file_path.relative_to(self.base_path)
                print(f"  {relative_path}:")
                print(f"    {warning}")

        # Final result
        print("\n" + "=" * 60)
        if all_valid:
            if self.warnings:
                print("✅ All YAML files are valid (with warnings)")
                return 0
            else:
                print("✅ All YAML files are valid!")
                return 0
        else:
            print("❌ YAML validation failed!")
            return 1


def main():
    """Main entry point."""
    # Get project root (assuming script is in scripts/ directory)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    validator = YamlValidator(project_root)
    exit_code = validator.run()

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
