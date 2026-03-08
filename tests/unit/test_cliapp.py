from unittest.mock import patch

import pytest

from jcli import CLIApp


class TestCLIApp:
    def test_init(self):
        app = CLIApp("testapp", config_dir="/tmp")
        assert app.app_name == "testapp"
        assert app.hints == {"config_dir": "/tmp"}
        assert app.parser is not None

    def test_register_module_valid(self):
        app = CLIApp("testapp")
        app.register_module("config")
        # Check that argument was added
        assert "-c" in str(app.parser.format_help())

    def test_register_module_invalid(self):
        app = CLIApp("testapp")
        with pytest.raises(ValueError, match="Unknown module: invalid"):
            app.register_module("invalid")

    def test_add_argument(self):
        app = CLIApp("testapp")
        app.add_argument("-q", "--quiet", action="store_true")
        assert "--quiet" in str(app.parser.format_help())

    def test_parse_args(self):
        app = CLIApp("testapp")
        app.add_argument("-q", "--quiet", action="store_true")
        args = app.parse_args(["-q"])
        assert args.quiet is True

    @patch("jcli.cliapp.load_config")
    def test_get_config(self, mock_load):
        mock_load.return_value = {"key": "value"}
        app = CLIApp("testapp", some_hint="hint")
        config = app.get_config()
        mock_load.assert_called_once_with(app_name="testapp", some_hint="hint")
        assert config == {"key": "value"}

    @patch("jcli.cliapp.load_config")
    def test_example_usage(self, mock_load):
        mock_load.return_value = {"default_message": "hello world"}
        app = CLIApp("echo_test")
        app.register_module("echo")
        app.register_module("config")
        args = app.parse_args(["test message"])
        config = app.get_config()
        assert args.message == "test message"
        assert config["default_message"] == "hello world"
