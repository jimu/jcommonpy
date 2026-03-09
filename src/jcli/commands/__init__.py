"""Commands module for executing shell commands and parsing JSON output."""

from __future__ import annotations

import json
import re
import subprocess
from typing import Any

__all__ = ["CommandFailed", "InvalidJSON", "UndefinedVariable", "execute"]


class CommandFailed(Exception):
    """Raised when a shell command exits with non-zero status."""

    def __init__(self, command: str, exit_code: int, stderr: str) -> None:
        self.command = command
        self.exit_code = exit_code
        self.stderr = stderr
        super().__init__(f"Command failed with exit code {exit_code}: {command}")


class InvalidJSON(Exception):
    """Raised when command output is not valid JSON."""

    def __init__(self, command: str, output: str) -> None:
        self.command = command
        self.output = output
        super().__init__(f"Command output is not valid JSON: {command}")


class UndefinedVariable(Exception):
    """Raised when a command contains a variable placeholder that is not defined."""

    def __init__(self, variable: str, command: str, available_vars: list[str]) -> None:
        self.variable = variable
        self.command = command
        self.available_vars = available_vars
        super().__init__(
            f"Undefined variable '{variable}' in command: {command}. Available: {', '.join(available_vars)}"
        )


def _interpolate_command(command: str, config: dict[str, Any]) -> str:
    """Interpolate variables in command string.

    Args:
        command: Command string with [var-name] placeholders
        config: Configuration dict containing vars section

    Returns:
        Command string with placeholders replaced

    Raises:
        UndefinedVariable: If a placeholder references undefined variable
    """
    vars_section = config.get("vars", {})

    # Find all [var-name] patterns (allow letters, numbers, underscore, hyphen)
    pattern = r"\[([a-zA-Z_][a-zA-Z0-9_-]*)\]"
    placeholders = re.findall(pattern, command)

    # Validate all variables are defined
    undefined_vars = []
    for var in placeholders:
        if var not in vars_section:
            undefined_vars.append(var)

    if undefined_vars:
        available_vars = list(vars_section.keys())
        raise UndefinedVariable(undefined_vars[0], command, available_vars)

    # Perform substitution
    def replace_var(match):
        var_name = match.group(1)
        return str(vars_section[var_name])

    return re.sub(pattern, replace_var, command)


def execute(command: str, format: str = "json") -> Any:
    """Execute a shell command and parse its output (no interpolation).

    Args:
        command: Shell command to execute (already interpolated)
        format: Output format ("json" only for MVP)

    Returns:
        Parsed output (Python object for JSON)

    Raises:
        CommandFailed: If command exits with non-zero status
        InvalidJSON: If output is not valid JSON
        ValueError: If format is not supported
    """
    if format != "json":
        raise ValueError(f"Unsupported format: {format}. Only 'json' is supported.")

    # Execute the command
    result = subprocess.run(command, shell=True, capture_output=True, text=True, check=False)

    # Check for command failure
    if result.returncode != 0:
        raise CommandFailed(command, result.returncode, result.stderr)

    # Parse JSON output
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as err:
        raise InvalidJSON(command, result.stdout) from err
