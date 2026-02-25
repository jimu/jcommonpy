## Why

jcli needs a simple reference module that CLI applications can import and use to test the package is installed and configured properly.

## What Changes

- Add new `jcli.echo` module with public interface `echo(message: str | None = "Hello, World!") -> str`
- The echo function returns the provided message if given, otherwise defaults to "Hello, World!"

## Capabilities

### New Capabilities
- `echo`: Provides string echoing functionality for CLI applications

### Modified Capabilities
<!-- No existing capabilities are modified -->

## Impact

- Adds a new module to the jcli package
- No breaking changes to existing APIs
- Minimal impact on package size and dependencies
- Affects the public API by adding new importable functionality
