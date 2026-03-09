"""Commands module for executing shell commands and parsing JSON output."""

from __future__ import annotations

import json
import subprocess
from typing import Any

__all__ = ["execute", "CommandFailed", "InvalidJSON"]


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


def execute(command: str, format: str = "json") -> Any:
    """Execute a shell command and parse its output.

    Args:
        command: Shell command to execute
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
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Check for command failure
    if result.returncode != 0:
        raise CommandFailed(command, result.returncode, result.stderr)

    # Parse JSON output
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        raise InvalidJSON(command, result.stdout)
