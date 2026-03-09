"""JCLI - Builder API for composing CLI applications."""

from __future__ import annotations

import argparse
import sys
from typing import Any

__all__ = ["JCLI"]


class JCLI:
    """Builder class for composing CLI applications from modules."""

    ALLOWED_MODULES = frozenset({"echo", "config", "diag"})

    def __init__(self, app_name: str) -> None:
        """Initialize JCLI with app name.

        Args:
            app_name: The name of the CLI application.
        """
        self._app_name = app_name
        self._modules: dict[str, Any] = {}
        self._module_options: dict[str, dict[str, Any]] = {}
        self._parser = argparse.ArgumentParser(prog=app_name)

    @property
    def app_name(self) -> str:
        """Return the app name."""
        return self._app_name

    @classmethod
    def builder(cls, app_name: str) -> JCLI:
        """Create a new JCLI builder instance.

        Args:
            app_name: The name of the CLI application.

        Returns:
            A new JCLI instance.
        """
        return cls(app_name)

    def add_module(self, name: str, *args: Any, **options: Any) -> JCLI:
        """Register a module with optional configuration.

        Args:
            name: The module name to register.
            *args: Positional arguments (used for diag callback).
            **options: Configuration options for the module.

        Returns:
            Self for method chaining.

        Raises:
            ValueError: If module name is not allowed.
        """
        if name not in self.ALLOWED_MODULES:
            raise ValueError(f"Unknown module: {name}. Allowed: {', '.join(self.ALLOWED_MODULES)}")

        if name == "diag" and args:
            options["callback"] = args[0]

        if name == "diag":
            self._parser.add_argument("--diag", action="store_true", help="Run diagnostic and exit")

        self._module_options[name] = options
        self._modules[name] = None
        return self

    def add_argument(self, *args: Any, **kwargs: Any) -> JCLI:
        """Add an argument to the CLI parser.

        Args:
            *args: Positional arguments for argparse.
            **kwargs: Keyword arguments for argparse.

        Returns:
            Self for method chaining.
        """
        self._parser.add_argument(*args, **kwargs)
        return self

    def __getattr__(self, name: str) -> Any:
        """Delegate attribute access to registered modules.

        Args:
            name: The module name to access.

        Returns:
            The module or module function.

        Raises:
            AttributeError: If module is not registered.
        """
        if name.startswith("_"):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

        if name not in self._modules:
            raise AttributeError(
                f"Module '{name}' not registered. Registered: {', '.join(self._modules.keys()) or 'none'}"
            )

        module = self._modules[name]
        if module is None:
            module = self._load_module(name)
            self._modules[name] = module

        return module

    def _load_module(self, name: str) -> Any:
        """Load a module by name.

        Args:
            name: The module name to load.

        Returns:
            The loaded module or module wrapper.
        """
        options = self._module_options.get(name, {})

        if name == "echo":
            from jcli.echo import echo as echo_func

            return echo_func

        if name == "config":
            from jcli import config as config_module

            class ConfigWrapper:
                def __init__(self, config_mod, app_name: str, opts: dict):
                    self._config = config_mod
                    self._app_name = app_name
                    self._opts = opts

                def get(self, key: str, default: Any = None) -> Any:
                    cfg = self._config.load_config(app_name=self._app_name, **self._opts)
                    return cfg.get(key, default)

            return ConfigWrapper(config_module, self._app_name, options)

        if name == "diag":
            callback = options.get("callback")
            return callback

        raise ValueError(f"Unknown module: {name}")

    def parse_args(self, args: list[str] | None = None) -> argparse.Namespace:
        """Parse CLI arguments.

        Args:
            args: Arguments to parse. Defaults to sys.argv.

        Returns:
            The parsed arguments namespace.
        """
        parsed = self._parser.parse_args(args)

        if "diag" in self._modules and getattr(parsed, "diag", False):
            callback = self._module_options.get("diag", {}).get("callback")
            if callback:
                callback()
            sys.exit(0)

        return parsed

    def get_config(self) -> dict[str, Any]:
        """Load configuration using app_name and registered options.

        Returns:
            A dictionary with configuration values.
        """
        from jcli import config as config_module

        config_opts = self._module_options.get("config", {})
        return config_module.load_config(app_name=self._app_name, **config_opts)
