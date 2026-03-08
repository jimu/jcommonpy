"""jcli - Reusable modules for CLI applications."""

# Re-export public APIs for easy importing
# Individual modules can be imported directly for lightweight usage

from .cliapp import CLIApp

__all__ = ["CLIApp"]

__version__ = "0.1.0"
