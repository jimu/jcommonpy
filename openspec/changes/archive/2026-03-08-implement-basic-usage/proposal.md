## Why

The README.md Quick Start section shows a desired usage pattern for building CLI applications with jcli, but this API is not yet implemented. Users need a unified builder API to register modules and arguments, and access module functionality through a consistent interface.

## What Changes

- Add `JCLI` builder class with fluent API for constructing CLI applications
- Implement `builder(app_name)` class method to create new JCLI instances
- Implement `add_module(name, **options)` to register modules (echo, config, diag)
- Implement `add_argument(*args, **kwargs)` to add custom arguments
- Implement echo, config, and diag modules into the JCLI system
- Add diagnostic module (`diag`) that automatically calls a callback and exits when `--diag` flag is passed (no manual method call needed)
- Implement "-h" / "--help" which automatically includes content relevant to any registered modules.

## Capabilities

### New Capabilities
- `jcli-builder`: Unified builder API for composing CLI applications from modules
- `diag-module`: Diagnostic module that executes a callback and exits when `--diag` is provided

### Modified Capabilities
- None - existing echo and config modules will be integrated but not modified in requirements

## Impact

- New file: `src/jcli/jcli.py` - main JCLI builder class
- New file: `src/jcli/diag/__init__.py` - diagnostic module implementation
- Modified: `src/jcli/__init__.py` - export JCLI class
- Modified: existing module files to integrate with JCLI
