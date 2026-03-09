"""Tests for jcli.commands module."""

import json
import os
import tempfile
from unittest.mock import patch

import pytest

from jcli import JCLI
from jcli.commands import CommandFailed, InvalidJSON, UndefinedVariable, _interpolate_command, execute


class TestExecuteFunction:
    """Test cases for the execute function."""

    def test_execute_with_valid_json_array(self):
        """Test executing command that returns valid JSON array."""
        result = execute('echo "[]"')
        assert result == []

    def test_execute_with_valid_json_object(self):
        """Test executing command that returns valid JSON object."""
        result = execute('echo \'{"key": "value"}\'')
        assert result == {"key": "value"}

    @patch("jcli.commands.subprocess.run")
    def test_execute_calls_subprocess_correctly(self, mock_run):
        """Test that execute calls subprocess.run with correct arguments."""
        mock_run.return_value = type("MockResult", (), {"returncode": 0, "stdout": '{"test": true}', "stderr": ""})()

        result = execute("test command")

        mock_run.assert_called_once_with("test command", shell=True, capture_output=True, text=True, check=False)
        assert result == {"test": True}

    def test_execute_command_failure(self):
        """Test that CommandFailed is raised for non-zero exit codes."""
        with pytest.raises(CommandFailed) as exc_info:
            execute("false")  # Command that always fails

        assert exc_info.value.exit_code == 1
        assert "false" in str(exc_info.value)

    def test_execute_invalid_json(self):
        """Test that InvalidJSON is raised for non-JSON output."""
        with pytest.raises(InvalidJSON) as exc_info:
            execute('echo "not json"')

        assert "not json" in str(exc_info.value)
        assert 'echo "not json"' in str(exc_info.value)

    def test_execute_unsupported_format(self):
        """Test that ValueError is raised for unsupported formats."""
        with pytest.raises(ValueError) as exc_info:
            execute('echo "test"', "xml")

        assert "Unsupported format: xml" in str(exc_info.value)


class TestCommandFailedException:
    """Test cases for CommandFailed exception."""

    def test_command_failed_init(self):
        """Test CommandFailed exception initialization."""
        exc = CommandFailed("test command", 42, "error output")
        assert exc.command == "test command"
        assert exc.exit_code == 42
        assert exc.stderr == "error output"
        assert "exit code 42" in str(exc)
        assert "test command" in str(exc)


class TestInvalidJSONException:
    """Test cases for InvalidJSON exception."""

    def test_invalid_json_init(self):
        """Test InvalidJSON exception initialization."""
        exc = InvalidJSON("test command", "invalid json output")
        assert exc.command == "test command"
        assert exc.output == "invalid json output"
        assert "not valid JSON" in str(exc)
        assert "test command" in str(exc)


class TestInterpolateCommand:
    """Test cases for command interpolation."""

    def test_interpolate_simple_variable(self):
        """Test interpolation of a simple variable."""
        config = {"vars": {"name": "world"}}
        result = _interpolate_command("hello [name]", config)
        assert result == "hello world"

    def test_interpolate_multiple_variables(self):
        """Test interpolation of multiple variables."""
        config = {"vars": {"greeting": "hello", "name": "world"}}
        result = _interpolate_command("[greeting] [name]", config)
        assert result == "hello world"

    def test_interpolate_no_variables(self):
        """Test command with no variables."""
        config = {"vars": {"name": "world"}}
        result = _interpolate_command("echo test", config)
        assert result == "echo test"

    def test_interpolate_undefined_variable(self):
        """Test that undefined variable raises exception."""
        config = {"vars": {"defined": "value"}}
        with pytest.raises(UndefinedVariable) as exc_info:
            _interpolate_command("test [undefined]", config)

        assert exc_info.value.variable == "undefined"
        assert exc_info.value.available_vars == ["defined"]

    def test_interpolate_missing_vars_section(self):
        """Test interpolation when vars section is missing."""
        config = {}
        with pytest.raises(UndefinedVariable):
            _interpolate_command("test [var]", config)


class TestUndefinedVariableException:
    """Test cases for UndefinedVariable exception."""

    def test_undefined_variable_init(self):
        """Test UndefinedVariable exception initialization."""
        exc = UndefinedVariable("missing_var", "command with [missing_var]", ["var1", "var2"])
        assert exc.variable == "missing_var"
        assert exc.command == "command with [missing_var]"
        assert exc.available_vars == ["var1", "var2"]
        assert "Undefined variable 'missing_var'" in str(exc)


class TestJCLICommandsIntegration:
    """Integration tests for commands module with JCLI."""

    def test_jcli_commands_module_registration(self):
        """Test that commands module can be registered with JCLI."""
        jcli = JCLI.builder("testapp")
        jcli.add_module("commands")
        jcli.build([])

        # Should be able to access commands module
        assert hasattr(jcli.commands, "execute")

    def test_jcli_commands_execute_integration(self):
        """Test executing commands through JCLI integration."""
        jcli = JCLI.builder("testapp")
        jcli.add_module("commands")
        jcli.build([])

        result = jcli.commands.execute('echo "[]"')
        assert result == []

    def test_jcli_commands_error_handling_integration(self):
        """Test error handling through JCLI integration."""
        jcli = JCLI.builder("testapp")
        jcli.add_module("commands")
        jcli.build([])

        with pytest.raises(CommandFailed):
            jcli.commands.execute("false")


class TestJCLICommandsInterpolationIntegration:
    """Integration tests for commands module with variable interpolation."""

    def test_jcli_commands_interpolation_simple(self):
        """Test interpolation through JCLI with simple variable."""
        # Create a mock config with vars
        # Create a simple config
        config = {"commands": {"test": 'printf \'{"message": "%s"}\''}, "vars": {"value": "hello"}}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config, f)
            config_file = f.name

        try:
            jcli = JCLI.builder("testapp")
            jcli.add_module("config", path=config_file)
            jcli.add_module("commands")
            jcli.build([])

            # Test interpolation
            result = jcli.commands.execute('printf \'{"message": "%s"}\' [value]')
            assert result == {"message": "hello"}
        finally:
            os.unlink(config_file)

    def test_jcli_commands_interpolation_undefined_var(self):
        """Test interpolation error for undefined variable."""
        # Create config with missing variable
        config = {"commands": {"test": 'printf \'{"message": "%s"}\''}, "vars": {"defined": "value"}}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config, f)
            config_file = f.name

        try:
            jcli = JCLI.builder("testapp")
            jcli.add_module("config", path=config_file)
            jcli.add_module("commands")
            jcli.build([])

            with pytest.raises(UndefinedVariable) as exc_info:
                jcli.commands.execute('printf \'{"message": "%s"}\' [undefined]')

            assert exc_info.value.variable == "undefined"
            assert "defined" in exc_info.value.available_vars
        finally:
            os.unlink(config_file)
