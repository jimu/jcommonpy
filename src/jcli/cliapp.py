import argparse
from typing import Any, ClassVar

from jcli.config import load_config


class CLIApp:
    _module_registry: ClassVar[dict[str, Any]] = {
        "config": lambda parser: parser.add_argument("-c", "--config", help="Path to config file"),
        "echo": lambda parser: parser.add_argument("message", help="Message to echo"),
    }

    def __init__(self, app_name, **hints):
        self.app_name = app_name
        self.hints = hints
        self.parser = argparse.ArgumentParser(prog=app_name)

    def register_module(self, name):
        if name not in self._module_registry:
            raise ValueError(f"Unknown module: {name}")
        self._module_registry[name](self.parser)

    def parse_args(self, args=None):
        return self.parser.parse_args(args)

    def get_config(self):
        return load_config(app_name=self.app_name, **self.hints)

    def add_argument(self, *args, **kwargs):
        self.parser.add_argument(*args, **kwargs)
