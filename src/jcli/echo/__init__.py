"""Echo module for jcli - provides simple string echoing functionality."""

__all__ = ["echo"]


def echo(message: str | None = "Hello, World!") -> str:
    """Echo back the provided message or a default greeting.

    Args:
        message: The message to echo. If None, returns "Hello, World!".

    Returns:
        The echoed message.

    Examples:
        >>> echo("Hello!")
        'Hello!'
        >>> echo()
        'Hello, World!'
    """
    return message if message is not None else "Hello, World!"
