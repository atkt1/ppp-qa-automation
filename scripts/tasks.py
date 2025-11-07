#!/usr/bin/env python3
"""
Cross-platform task runner for QA Automation Framework.

This module provides Poetry script commands that work identically on Windows, Mac, and Linux.
It serves as an alternative to Makefile for Windows users while maintaining the same functionality.

Usage:
    poetry run format          # Format and lint code
    poetry run test-all        # Run all tests
    poetry run install-hooks   # Install pre-commit hooks
    poetry run pr-ready        # Comprehensive PR check
"""

import subprocess
import sys
from pathlib import Path
from typing import List


def run_command(cmd: str, cwd: Path = None) -> int:
    """
    Run a shell command and return exit code.

    Args:
        cmd: Command to execute
        cwd: Working directory (default: project root)

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    if cwd is None:
        cwd = Path(__file__).parent.parent

    result = subprocess.run(cmd, shell=True, cwd=cwd)
    return result.returncode


def print_header(message: str) -> None:
    """Print a formatted header message."""
    print(f"\n{'=' * 60}")
    print(f"  {message}")
    print(f"{'=' * 60}\n")


def print_step(step: int, total: int, message: str) -> None:
    """Print a formatted step message."""
    print(f"{step}/{total} {message}...")


# ==========================================
# Formatting and Linting
# ==========================================


def format_code() -> None:
    """
    Format and lint code in the correct order.

    Order: isort → black → ruff --fix → validate-yaml

    Exit code: 0 on success, 1 on failure
    """
    print_header("Running Code Formatting and Linting")

    commands = [
        ("1/4", "Running isort", "poetry run isort ."),
        ("2/4", "Running black", "poetry run black ."),
        ("3/4", "Running ruff with auto-fix", "poetry run ruff check --fix ."),
        ("4/4", "Validating YAML files", "poetry run python scripts/validate_yaml.py"),
    ]

    for step, desc, cmd in commands:
        print_step(*step.split("/"), desc)
        exit_code = run_command(cmd)
        if exit_code != 0:
            print(f"\n❌ {desc} failed!")
            sys.exit(exit_code)

    print("\n✅ All formatting and validation complete!\n")


def lint() -> None:
    """Run linting with ruff (check only, no fixes)."""
    sys.exit(run_command("poetry run ruff check ."))


def lint_fix() -> None:
    """Run linting with ruff and auto-fix issues."""
    sys.exit(run_command("poetry run ruff check --fix ."))


def format_check() -> None:
    """
    Check if formatting is needed without making changes (CI mode).

    Checks: isort, black, ruff
    """
    print("Checking code formatting...")

    commands = [
        ("isort", "poetry run isort --check-only ."),
        ("black", "poetry run black --check ."),
        ("ruff", "poetry run ruff check ."),
    ]

    failed = []
    for name, cmd in commands:
        print(f"Checking {name}...")
        if run_command(cmd) != 0:
            failed.append(name)

    if failed:
        print(f"\n❌ Formatting check failed: {', '.join(failed)}")
        print("Run 'poetry run format' to fix issues.")
        sys.exit(1)
    else:
        print("\n✅ All formatting checks passed!")


def validate_yaml() -> None:
    """Validate all YAML files (syntax, duplicates, indentation)."""
    sys.exit(run_command("poetry run python scripts/validate_yaml.py"))


# ==========================================
# Testing
# ==========================================


def test_all() -> None:
    """Run all tests."""
    sys.exit(run_command("poetry run pytest -v"))


def test_api() -> None:
    """Run API tests only."""
    sys.exit(run_command("poetry run pytest team_alpha/tests/api/ -v"))


def test_web() -> None:
    """Run web UI tests (headless)."""
    sys.exit(run_command("poetry run pytest team_alpha/tests/web/ -v"))


def test_web_headed() -> None:
    """Run web UI tests with visible browser."""
    sys.exit(run_command("poetry run pytest team_alpha/tests/web/ --headed -v"))


def test_smoke() -> None:
    """Run smoke tests only."""
    sys.exit(run_command("poetry run pytest -m smoke -v"))


def test_parallel() -> None:
    """Run all tests in parallel (auto-detect CPU cores)."""
    sys.exit(run_command("poetry run pytest -v -n auto"))


def test_api_parallel() -> None:
    """Run API tests in parallel."""
    sys.exit(run_command("poetry run pytest team_alpha/tests/api/ -v -n auto"))


def test_web_parallel() -> None:
    """Run web tests in parallel (headless)."""
    sys.exit(run_command("poetry run pytest team_alpha/tests/web/ -v -n auto"))


def test_smoke_parallel() -> None:
    """Run smoke tests in parallel."""
    sys.exit(run_command("poetry run pytest -m smoke -v -n auto"))


# ==========================================
# Pre-commit and Hooks
# ==========================================


def install_hooks() -> None:
    """Install pre-commit hooks."""
    print("Installing pre-commit hooks...")
    exit_code = run_command("poetry run pre-commit install")

    if exit_code == 0:
        print("\n✅ Pre-commit hooks installed successfully!")
        print("Hooks will run automatically on git commit\n")
    else:
        print("\n❌ Failed to install pre-commit hooks")
        sys.exit(exit_code)


def pre_commit() -> None:
    """Run all pre-commit checks manually on all files."""
    sys.exit(run_command("poetry run pre-commit run --all-files"))


def pre_commit_update() -> None:
    """Update pre-commit hooks to latest versions."""
    sys.exit(run_command("poetry run pre-commit autoupdate"))


# ==========================================
# Combined Tasks
# ==========================================


def pr_ready() -> None:
    """
    Comprehensive check before submitting PR.

    Runs: format + test-all
    """
    print_header("PR Ready Checks")

    # Run formatting
    print("Step 1/2: Running formatting and linting...")
    format_code()

    # Run all tests
    print("\nStep 2/2: Running all tests...")
    exit_code = run_command("poetry run pytest -v")

    if exit_code != 0:
        print("\n❌ Tests failed!")
        sys.exit(exit_code)

    # Success message
    print_header("✅ PR Ready Checks Completed!")
    print("✓ Code formatted (isort + black + ruff)")
    print("✓ YAML files validated")
    print("✓ All tests passed")
    print("\nYour code is ready for PR submission!")
    print("Don't forget to:")
    print("  - Update documentation if needed")
    print("  - Add/update test cases")
    print("  - Fill out PR template completely")
    print("=" * 60 + "\n")


# ==========================================
# Cleanup
# ==========================================


def clean() -> None:
    """Clean up generated files."""
    print("Cleaning up generated files...")

    paths_to_remove = [
        ".pytest_cache",
        "allure-results",
        "allure-report",
        "logs/*.log",
        "videos",
        "screenshots",
    ]

    project_root = Path(__file__).parent.parent

    for path_pattern in paths_to_remove:
        if "*" in path_pattern:
            # Handle glob patterns
            base_dir = project_root / Path(path_pattern).parent
            pattern = Path(path_pattern).name
            if base_dir.exists():
                for file in base_dir.glob(pattern):
                    if file.is_file():
                        file.unlink()
                        print(f"  Removed: {file.relative_to(project_root)}")
        else:
            # Handle directories
            path = project_root / path_pattern
            if path.exists():
                if path.is_dir():
                    import shutil

                    shutil.rmtree(path)
                    print(f"  Removed: {path.relative_to(project_root)}")
                else:
                    path.unlink()
                    print(f"  Removed: {path.relative_to(project_root)}")

    print("\n✅ Cleanup complete!\n")


def clean_videos() -> None:
    """Clean up video recordings only."""
    print("Cleaning up video files...")

    project_root = Path(__file__).parent.parent
    videos_dir = project_root / "videos"

    if videos_dir.exists():
        for video_file in videos_dir.glob("*.webm"):
            video_file.unlink()
            print(f"  Removed: {video_file.name}")

    print("✅ Video files cleaned up\n")


# ==========================================
# Help and Information
# ==========================================


def list_commands() -> None:
    """List all available Poetry script commands."""
    print_header("Available Poetry Script Commands")

    commands = [
        ("Format & Lint", [
            ("format", "Format and lint code (isort → black → ruff → validate-yaml)"),
            ("lint", "Run linting with ruff (check only)"),
            ("lint-fix", "Run linting with ruff and auto-fix"),
            ("format-check", "Check formatting without changes (CI mode)"),
            ("validate-yaml", "Validate all YAML files"),
        ]),
        ("Testing", [
            ("test-all", "Run all tests"),
            ("test-api", "Run API tests only"),
            ("test-web", "Run web tests (headless)"),
            ("test-web-headed", "Run web tests with visible browser"),
            ("test-smoke", "Run smoke tests only"),
            ("test-parallel", "Run all tests in parallel"),
        ]),
        ("Pre-commit", [
            ("install-hooks", "Install pre-commit hooks"),
            ("pre-commit", "Run all pre-commit checks manually"),
            ("pre-commit-update", "Update pre-commit hooks to latest versions"),
        ]),
        ("Combined", [
            ("pr-ready", "Comprehensive PR check (format + test-all)"),
        ]),
        ("Cleanup", [
            ("clean", "Clean up generated files"),
            ("clean-videos", "Clean up video recordings only"),
        ]),
    ]

    for category, cmds in commands:
        print(f"\n{category}:")
        print("-" * 60)
        for cmd, desc in cmds:
            print(f"  poetry run {cmd:20} # {desc}")

    print("\n" + "=" * 60)
    print("Note: Mac/Linux users can also use 'make' commands")
    print("=" * 60 + "\n")


# ==========================================
# Entry Points
# ==========================================

if __name__ == "__main__":
    # If running directly, show help
    list_commands()
