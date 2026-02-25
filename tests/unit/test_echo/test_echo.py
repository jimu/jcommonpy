"""Tests for jcli.echo module."""

import pytest

from jcli.echo import echo


class TestEcho:
    """Test cases for the echo function."""

    def test_echo_with_message(self):
        """Test echoing a provided message."""
        result = echo("Hello, Test!")
        assert result == "Hello, Test!"

    def test_echo_default_message(self):
        """Test echoing the default message when no parameter provided."""
        result = echo()
        assert result == "Hello, World!"

    def test_echo_none_message(self):
        """Test echoing the default message when None is provided."""
        result = echo(None)
        assert result == "Hello, World!"

    @pytest.mark.parametrize(
        "message,expected",
        [
            ("Custom message", "Custom message"),
            ("", ""),  # Empty string
            ("Hello, World!", "Hello, World!"),  # Same as default
        ],
    )
    def test_echo_various_messages(self, message, expected):
        """Test echo with various message inputs."""
        result = echo(message)
        assert result == expected
