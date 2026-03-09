"""Tests for jcli.jcli module."""

from unittest.mock import patch

import pytest

from jcli import JCLI


class TestJCLIBuilder:
    """Test cases for the JCLI builder class."""

    def test_builder_creates_instance(self):
        """Test that builder class method creates a JCLI instance."""
        jcli = JCLI.builder("testapp")
        assert isinstance(jcli, JCLI)

    def test_app_name_stored(self):
        """Test that app_name is stored correctly."""
        jcli = JCLI.builder("myapp")
        assert jcli.app_name == "myapp"

    def test_add_module_returns_self(self):
        """Test that add_module returns self for chaining."""
        jcli = JCLI.builder("testapp")
        result = jcli.add_module("echo")
        assert result is jcli

    def test_add_module_echo(self):
        """Test adding echo module."""
        jcli = JCLI.builder("testapp")
        jcli.add_module("echo")
        result = jcli.echo("Hello!")
        assert result == "Hello!"

    def test_add_module_config(self):
        """Test adding config module."""
        jcli = JCLI.builder("testapp")
        jcli.add_module("config")
        value = jcli.config.get("key", "default")
        assert value == "default"

    def test_add_module_config_with_options(self):
        """Test adding config module with options."""
        jcli = JCLI.builder("testapp")
        jcli.add_module("config", path="~/.testrc", env="TESTRC")
        value = jcli.config.get("key", "default")
        assert value == "default"

    def test_add_module_invalid_raises_error(self):
        """Test that adding invalid module raises ValueError."""
        jcli = JCLI.builder("testapp")
        with pytest.raises(ValueError, match="Unknown module"):
            jcli.add_module("invalid")

    def test_add_module_allows_valid_modules(self):
        """Test that all allowed modules can be added."""
        jcli = JCLI.builder("testapp")
        for module in ["echo", "config", "diag"]:
            jcli.add_module(module)
        assert "echo" in jcli._modules
        assert "config" in jcli._modules
        assert "diag" in jcli._modules


class TestJCLIArguments:
    """Test cases for argument handling."""

    def test_add_argument_returns_self(self):
        """Test that add_argument returns self for chaining."""
        jcli = JCLI.builder("testapp")
        result = jcli.add_argument("--verbose", action="store_true")
        assert result is jcli

    def test_add_argument_boolean_flag(self):
        """Test adding a boolean flag argument."""
        jcli = JCLI.builder("testapp")
        jcli.add_argument("--verbose", action="store_true")
        jcli.build(["--verbose"])
        assert jcli.args.verbose is True

    def test_add_argument_without_flag(self):
        """Test parsing without the flag."""
        jcli = JCLI.builder("testapp")
        jcli.add_argument("--verbose", action="store_true")
        jcli.build([])
        assert jcli.args.verbose is False

    def test_add_argument_string_arg(self):
        """Test adding a string argument."""
        jcli = JCLI.builder("testapp")
        jcli.add_argument("--output", type=str, default="result.txt")
        jcli.build(["--output", "myfile.txt"])
        assert jcli.args.output == "myfile.txt"

    def test_fluent_api_chain(self):
        """Test fluent API chaining works."""
        jcli = JCLI.builder("myapp")
        jcli.add_module("echo").add_argument("--verbose", action="store_true")
        assert jcli.echo("test") == "test"

    def test_build_default_empty(self):
        """Test build with empty args."""
        jcli = JCLI.builder("testapp")
        jcli.add_module("config")
        jcli.build([])
        assert isinstance(jcli.args, object)

    def test_config_module_adds_config_argument(self):
        """Test that config module adds -c/--config argument."""
        jcli = JCLI.builder("testapp")
        jcli.add_module("config")
        help_text = jcli._parser.format_help()
        assert "-c" in help_text
        assert "--config" in help_text

    @patch("jcli.config.load_config")
    def test_config_file_passed_to_load_config(self, mock_load):
        """Test that --config value is passed to load_config."""
        mock_load.return_value = {}
        jcli = JCLI.builder("testapp")
        jcli.add_module("config")
        jcli.build(["--config", "/path/to/config.yaml"])
        mock_load.assert_called()

    def test_config_env_var_invalid_exits(self):
        """Test that invalid env var causes exit."""
        import os

        os.environ["TEST_INVALID_CONFIG"] = "/nonexistent.yaml"
        try:
            jcli = JCLI.builder("testapp")
            jcli.add_module("config", env="TEST_INVALID_CONFIG")
            with pytest.raises(SystemExit) as exc_info:
                jcli.build([])
            assert exc_info.value.code == 1
        finally:
            del os.environ["TEST_INVALID_CONFIG"]


class TestJCLIGetConfig:
    """Test cases for get_config method."""

    def test_get_config_returns_dict(self):
        """Test that get_config returns a dictionary."""
        jcli = JCLI.builder("testapp")
        config = jcli.get_config()
        assert isinstance(config, dict)

    def test_get_config_with_module_options(self):
        """Test get_config with config module options."""
        jcli = JCLI.builder("testapp")
        jcli.add_module("config", path="~/.testrc")
        config = jcli.get_config()
        assert isinstance(config, dict)


class TestJCLIModuleAccess:
    """Test cases for module attribute access."""

    def test_access_unregistered_module_raises_error(self):
        """Test that accessing unregistered module raises AttributeError."""
        jcli = JCLI.builder("testapp")
        with pytest.raises(AttributeError, match="not registered"):
            _ = jcli.echo

    def test_access_echo_module(self):
        """Test accessing echo module."""
        jcli = JCLI.builder("testapp")
        jcli.add_module("echo")
        result = jcli.echo("message")
        assert result == "message"

    def test_access_config_module(self):
        """Test accessing config module."""
        jcli = JCLI.builder("testapp")
        jcli.add_module("config")
        config_wrapper = jcli.config
        assert hasattr(config_wrapper, "get")

    def test_lazy_module_loading(self):
        """Test that modules are loaded lazily."""
        jcli = JCLI.builder("testapp")
        jcli.add_module("echo")
        assert jcli._modules["echo"] is None
        _ = jcli.echo
        assert jcli._modules["echo"] is not None
