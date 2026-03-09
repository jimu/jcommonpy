"""JCLI - Builder API for composing CLI applications."""

from __future__ import annotations

import argparse
import sys
from typing import Any

from jcli import commands as commands_module
from jcli import config as config_module
from jcli.echo import echo as echo_func

__all__ = ["JCLI"]


class JCLI:
    """Builder class for composing CLI applications from modules."""

    ALLOWED_MODULES = frozenset({"echo", "config", "diag", "commands"})

    def __init__(self, app_name: str) -> None:
        """Initialize JCLI with app name.

        Args:
            app_name: The name of the CLI application.
        """
        self._app_name = app_name
        self._modules: dict[str, Any] = {}
        self._module_options: dict[str, dict[str, Any]] = {}
        self._parser = argparse.ArgumentParser(prog=app_name)
        self._config_cache: dict[str, Any] | None = None
        self._parsed_args: argparse.Namespace | None = None

    @property
    def app_name(self) -> str:
        """Return the app name."""
        return self._app_name

    @property
    def args(self) -> argparse.Namespace:
        """Return parsed command line arguments.

        Assumes build() has been called to parse arguments.
        """
        if self._parsed_args is None:
            raise RuntimeError("Must call build() before accessing args")
        return self._parsed_args

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

        if name == "config":
            self._parser.add_argument("-c", "--config", type=str, help="Path to config file (YAML)")

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

    def build(self, args: list[str] | None = None) -> JCLI:
        """Build the CLI application by parsing arguments.

        This method parses command line arguments and sets up the application
        for use. Call this after configuring modules and arguments.

        Args:
            args: Arguments to parse. Defaults to sys.argv.

        Returns:
            Self for method chaining.
        """
        if self._parsed_args is None:
            self._parsed_args = self._parse_args(args)
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
            return echo_func

        if name == "config":

            class ConfigWrapper:
                def __init__(self, jcli: JCLI, config_mod, app_name: str, opts: dict):
                    self._jcli = jcli
                    self._config = config_mod
                    self._app_name = app_name
                    self._opts = opts

                def get(self, key: str, default: Any = None) -> Any:
                    cfg = self._jcli.get_config()
                    return cfg.get(key, default)

            return ConfigWrapper(self, config_module, self._app_name, options)

        if name == "diag":
            callback = options.get("callback")
            return callback

        if name == "commands":

            class CommandsWrapper:
                def __init__(self, commands_mod, jcli: JCLI):
                    self._commands = commands_mod
                    self._jcli = jcli

                def execute(self, command: str, format: str = "json") -> Any:
                    # Interpolate variables in command
                    config = self._jcli.get_config()
                    interpolated_command = self._commands._interpolate_command(command, config)
                    # Execute with interpolated command
                    return self._commands.execute(interpolated_command, format)

                # Expose exception classes
                @property
                def CommandFailed(self):
                    return self._commands.CommandFailed

                @property
                def InvalidJSON(self):
                    return self._commands.InvalidJSON

                @property
                def UndefinedVariable(self):
                    return self._commands.UndefinedVariable

            return CommandsWrapper(commands_module, self)

        raise ValueError(f"Unknown module: {name}")

    def _parse_args(self, args: list[str] | None = None) -> argparse.Namespace:
        """Parse CLI arguments internally.

        Args:
            args: Arguments to parse. Defaults to sys.argv.

        Returns:
            The parsed arguments namespace.
        """
        parsed = self._parser.parse_args(args)

        if "config" in self._modules:
            config_opts = self._module_options.get("config", {})
            config_file = getattr(parsed, "config", None)
            if config_file:
                config_opts = {**config_opts, "config_file": config_file}

            self._config_cache = config_module.load_config(
                app_name=self._app_name,
                **config_opts,
            )

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
        if self._config_cache is not None:
            return self._config_cache

        config_opts = self._module_options.get("config", {})
        self._config_cache = config_module.load_config(app_name=self._app_name, **config_opts)
        return self._config_cache
