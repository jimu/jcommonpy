## Why

To simplify building CLI applications by providing a high-level CLIApp class that handles module registration and configuration loading, allowing developers to create apps without needing to understand argparse or manual config file handling.

## What Changes

- Introduce a new public `CLIApp` class in the jcli package
- `CLIApp.__init__()` accepts app_name and hints for configuration
- `register_module()` method to add modules like 'echo' or 'config'
- `parse_args()` method that builds and parses the full argument parser internally
- `get_config()` method that locates and loads configuration files based on app_name or hints

## Capabilities

### New Capabilities
- `cli-app`: High-level API for building CLI applications with module registration and automatic configuration handling

### Modified Capabilities

## Impact

- Adds new public API to the jcli package
- Affects the main jcli module structure