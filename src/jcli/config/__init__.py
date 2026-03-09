"""Configuration loading module for jcli."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

import yaml

__all__ = ["load_config"]


def load_config(
    app_name: str | None = None,
    path: str | None = None,
    env: str | None = None,
    config_file: str | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Load configuration from YAML file.

    Args:
        app_name: Application name (for future use).
        path: Default config file path.
        env: Environment variable containing config file path.
        config_file: Explicit config file path from --config argument.

    Returns:
        Configuration dictionary.

    Raises:
        SystemExit: If --config is specified but file cannot be read, or if
            env variable is set but points to unreadable/invalid file.
    """
    config_path: Path | None = None

    if config_file:
        config_path = Path(config_file)
        if not _is_readable_yaml(config_path):
            print(
                f"Error: Cannot read config file '{config_file}': file not found or not readable",
                file=sys.stderr,
            )
            sys.exit(1)
        return _load_yaml(config_path)

    if env:
        env_value = os.environ.get(env)
        if env_value:
            config_path = Path(env_value)
            if not _is_readable_yaml(config_path):
                print(
                    f"Error: Cannot read config file from {env}='{env_value}': file not found or not readable",
                    file=sys.stderr,
                )
                sys.exit(1)
            return _load_yaml(config_path)

    if path:
        config_path = Path(path)
        if _is_readable_yaml(config_path):
            return _load_yaml(config_path)

    return {}


def _is_readable_yaml(path: Path) -> bool:
    """Check if path is a readable YAML file."""
    if not path.exists() or not path.is_file():
        return False
    try:
        with open(path) as f:
            yaml.safe_load(f)
        return True
    except Exception:
        return False


def _load_yaml(path: Path) -> dict[str, Any]:
    """Load and parse a YAML file."""
    with open(path) as f:
        return yaml.safe_load(f) or {}
