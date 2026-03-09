#!/usr/bin/env python
"""Reference implementation demonstrating jcli basic usage.

This example demonstrates all features implemented so far:
- JCLI builder with fluent API
- Module registration (echo, config, diag)
- Custom argument parsing
- Module access via attributes
"""

import sys

from jcli import JCLI


def main() -> None:
    """Main entry point for the example CLI application."""

    def run_diagnostic() -> None:
        print("Running diagnostic checks...")
        print("- All systems operational")
        print("Diagnostic complete!")

    jcli = (
        JCLI.builder("my-app")
        .add_module("echo")
        .add_module("config", path="examples/basic.config")
        .add_argument("--verbose", action="store_true", help="Enable verbose output")
        .add_module("diag", run_diagnostic)
        .add_module("commands")
        .add_argument("--output", type=str, default="output.txt", help="Output file name")
        .add_argument("action", nargs="?", choices=["list", "count"], help="Action to perform (list or count)")
        .build()
    )

    if jcli.args.verbose:
        print(f"[DEBUG] App: {jcli.app_name}")
        print(f"[DEBUG] Output file: {jcli.args.output}")

    if jcli.args.action == "list":
        # List all command keys from config
        config = jcli.get_config()
        commands = config.get("commands", {})
        for key in commands.keys():
            print(f" - {key}")
    elif jcli.args.action == "count":
        # Execute each command and count JSON array items
        config = jcli.get_config()
        commands = config.get("commands", {})
        for key, command in commands.items():
            try:
                result = jcli.commands.execute(command, "json")
                if isinstance(result, list):
                    count = len(result)
                    print(f" {key}: {count}")
                else:
                    print(f"Error: Command '{key}' did not return a JSON array", file=sys.stderr)
                    sys.exit(1)
            except (jcli.commands.CommandFailed, jcli.commands.InvalidJSON) as e:
                print(f"Error executing command '{key}': {e}", file=sys.stderr)
                sys.exit(1)
    else:
        # Default behavior - echo output
        result = jcli.echo(f"Output: {jcli.args.output}")
        print(result)


if __name__ == "__main__":
    main()
