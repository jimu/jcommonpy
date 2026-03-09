"""Tests for jcli.diag module."""

from unittest.mock import MagicMock, patch

from jcli import JCLI
from jcli.diag import diag


class TestDiagFunction:
    """Test cases for the diag() function."""

    def test_diag_returns_callback(self):
        """Test that diag() returns the callback function."""
        callback = MagicMock()
        result = diag(callback)
        assert result is callback


class TestJCLIDiagIntegration:
    """Test cases for diag module integration with JCLI."""

    def test_add_module_diag_auto_adds_argument(self):
        """Test that adding diag module adds --diag argument."""
        jcli = JCLI.builder("testapp")

        def mydiag():
            pass

        jcli.add_module("diag", mydiag)
        help_text = jcli._parser.format_help()
        assert "--diag" in help_text

    def test_diag_module_accessible_via_attribute(self):
        """Test that diag module is accessible via attribute."""
        jcli = JCLI.builder("testapp")

        def mydiag():
            pass

        jcli.add_module("diag", mydiag)
        diag_fn = jcli.diag
        assert diag_fn is mydiag

    @patch("jcli.jcli.sys.exit")
    def test_diag_callback_executed_with_flag(self, mock_exit):
        """Test that diag callback is executed when --diag is passed."""
        jcli = JCLI.builder("testapp")
        callback_called = []

        def mydiag():
            callback_called.append(True)

        jcli.add_module("diag", mydiag)
        jcli.parse_args(["--diag"])

        assert callback_called == [True]
        mock_exit.assert_called_once_with(0)

    @patch("jcli.jcli.sys.exit")
    def test_diag_with_positional_callback(self, mock_exit):
        """Test that callback can be passed as positional arg."""
        jcli = JCLI.builder("testapp")
        callback = MagicMock()
        jcli.add_module("diag", callback)

        jcli.parse_args(["--diag"])

        callback.assert_called_once()
        mock_exit.assert_called_once_with(0)

    @patch("jcli.jcli.sys.exit")
    def test_diag_without_callback(self, mock_exit):
        """Test that --diag works without callback."""
        jcli = JCLI.builder("testapp")
        jcli.add_module("diag")

        jcli.parse_args(["--diag"])

        mock_exit.assert_called_once_with(0)

    @patch("jcli.jcli.sys.exit")
    def test_diag_not_called_without_flag(self, mock_exit):
        """Test that callback is not called when --diag is not passed."""
        jcli = JCLI.builder("testapp")
        callback = MagicMock()
        jcli.add_module("diag", callback)

        jcli.parse_args([])

        callback.assert_not_called()
        mock_exit.assert_not_called()
