"""Tests for jcli.config module."""

import os
import tempfile

import pytest

from jcli.config import load_config


class TestLoadConfig:
    """Test cases for load_config function."""

    def test_load_empty_config(self):
        """Test loading with no config sources returns empty dict."""
        config = load_config()
        assert config == {}

    def test_load_config_with_explicit_file(self):
        """Test loading from explicit config file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("key1: value1\nkey2: 123\n")
            tmp = f.name

        try:
            config = load_config(config_file=tmp)
            assert config == {"key1": "value1", "key2": 123}
        finally:
            os.unlink(tmp)

    def test_load_config_with_explicit_invalid_file(self):
        """Test loading from non-existent explicit config file exits."""
        with pytest.raises(SystemExit) as exc_info:
            load_config(config_file="/nonexistent.yaml")
        assert exc_info.value.code == 1

    def test_load_config_env_var_valid(self):
        """Test loading from environment variable."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("env_key: env_value\n")
            tmp = f.name

        try:
            os.environ["TESTCONFIG"] = tmp
            config = load_config(env="TESTCONFIG")
            assert config == {"env_key": "env_value"}
        finally:
            del os.environ["TESTCONFIG"]
            os.unlink(tmp)

    def test_load_config_env_var_invalid(self):
        """Test loading from invalid environment variable exits."""
        os.environ["TESTCONFIG"] = "/nonexistent.yaml"
        try:
            with pytest.raises(SystemExit) as exc_info:
                load_config(env="TESTCONFIG")
            assert exc_info.value.code == 1
        finally:
            del os.environ["TESTCONFIG"]

    def test_load_config_env_var_not_set(self):
        """Test loading when environment variable is not set."""
        config = load_config(env="NOTSET_VAR_12345")
        assert config == {}

    def test_load_config_path_valid(self):
        """Test loading from default path."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("path_key: path_value\n")
            tmp = f.name

        try:
            config = load_config(path=tmp)
            assert config == {"path_key": "path_value"}
        finally:
            os.unlink(tmp)

    def test_load_config_path_invalid(self):
        """Test loading from invalid path returns empty dict."""
        config = load_config(path="/nonexistent.yaml")
        assert config == {}

    def test_priority_config_file_over_env(self):
        """Test that --config takes priority over env var."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("explicit: true\n")
            explicit = f.name

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("env: true\n")
            env_file = f.name

        try:
            os.environ["TESTCONFIG"] = env_file
            config = load_config(config_file=explicit, env="TESTCONFIG")
            assert config == {"explicit": True}
        finally:
            os.unlink(explicit)
            os.unlink(env_file)
            del os.environ["TESTCONFIG"]

    def test_priority_env_over_path(self):
        """Test that env var takes priority over path."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("env: true\n")
            env_file = f.name

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("path: true\n")
            path_file = f.name

        try:
            os.environ["TESTCONFIG"] = env_file
            config = load_config(env="TESTCONFIG", path=path_file)
            assert config == {"env": True}
        finally:
            os.unlink(env_file)
            os.unlink(path_file)
            del os.environ["TESTCONFIG"]
