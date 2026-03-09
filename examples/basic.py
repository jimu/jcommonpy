#!/usr/bin/env python
"""Reference implementation demonstrating jcli basic usage.

This example demonstrates all features implemented so far:
- JCLI builder with fluent API
- Module registration (echo, config, diag)
- Custom argument parsing
- Module access via attributes
"""

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
        .add_module("config", path="~/.myapprc")
        .add_argument("--verbose", action="store_true", help="Enable verbose output")
        .add_module("diag", run_diagnostic)
        .add_argument("--output", type=str, default="output.txt", help="Output file name")
        .build()
    )

    if jcli.args.verbose:
        print(f"[DEBUG] App: {jcli.app_name}")
        print(f"[DEBUG] Output file: {jcli.args.output}")

    result = jcli.echo(f"Output: {jcli.args.output}")
    print(result)


if __name__ == "__main__":
    main()
