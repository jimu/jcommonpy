"""Tests for examples/basic.py reference implementation."""

from unittest.mock import patch

import pytest

from examples import basic


class TestBasicExample:
    """Test cases for the basic example."""

    @patch("sys.argv", ["basic.py"])
    def test_basic_execution(self, capsys):
        """Test basic execution without flags."""
        basic.main()
        captured = capsys.readouterr()
        assert "Output: output.txt" in captured.out

    @patch("sys.argv", ["basic.py", "--verbose"])
    def test_verbose_mode(self, capsys):
        """Test execution with --verbose flag."""
        basic.main()
        captured = capsys.readouterr()
        assert "[DEBUG] App: my-app" in captured.out
        assert "[DEBUG] Output file: output.txt" in captured.out
        assert "Output: output.txt" in captured.out

    @patch("sys.argv", ["basic.py", "--output", "custom.txt"])
    def test_custom_output(self, capsys):
        """Test execution with custom output file."""
        basic.main()
        captured = capsys.readouterr()
        assert "Output: custom.txt" in captured.out

    @patch("sys.argv", ["basic.py", "--diag"])
    @patch("jcli.jcli.sys.exit")
    def test_diag_mode(self, mock_exit, capsys):
        """Test execution with --diag flag."""
        basic.main()
        captured = capsys.readouterr()
        assert "Output: output.txt" in captured.out
        assert "Running diagnostic checks" in captured.out
        assert "Diagnostic complete!" in captured.out
        mock_exit.assert_called_once_with(0)

    @patch("sys.argv", ["basic.py", "list"])
    def test_list_commands(self, capsys):
        """Test that 'list' argument shows command keys."""
        basic.main()
        captured = capsys.readouterr()
        assert "- catfood" in captured.out
        assert "- litter" in captured.out


class TestBasicExampleHelp:
    """Test cases for help output."""

    @patch("sys.argv", ["basic.py", "--help"])
    def test_help_output(self, capsys):
        """Test that --help shows correct options."""
        with pytest.raises(SystemExit):
            basic.main()
        captured = capsys.readouterr()
        assert "--diag" in captured.out
        assert "--verbose" in captured.out
        assert "--output" in captured.out
