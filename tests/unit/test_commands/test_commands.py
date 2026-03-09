"""Tests for jcli.commands module."""

import pytest
from unittest.mock import patch

from jcli.commands import execute, CommandFailed, InvalidJSON
from jcli import JCLI


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

        mock_run.assert_called_once_with("test command", shell=True, capture_output=True, text=True)
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
