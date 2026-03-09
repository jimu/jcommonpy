"""Diagnostic module for jcli - runs callback when --diag is passed."""

from collections.abc import Callable

__all__ = ["diag"]


def diag(callback: Callable[[], None]) -> Callable[[], None]:
    """Create a diagnostic callback wrapper.

    This is a simple wrapper that stores the callback. The JCLI builder
    automatically handles executing the callback when --diag is passed.

    Args:
        callback: The callback function to run when --diag is passed.

    Returns:
        The callback function (for compatibility).
    """
    return callback
