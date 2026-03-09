## Why

CLI applications often need to define command templates with configurable parameters. Users want to create reusable command patterns where variables can be substituted from configuration, enabling dynamic command construction without code changes.

## What Changes

- jcli commands module supports string interpolation using `[var-name]` placeholders
- Command strings are interpolated with values from config `vars` section before execution
- Add error handling for undefined variable references in command strings
- Variables are resolved from the same config source used for the commands

## Capabilities

### New Capabilities
- `string-interpolation`: Variable substitution in command strings using config values

### Modified Capabilities
- `commands-module`: Enhanced to perform interpolation before command execution

## Impact

- Modified: `src/jcli/commands/__init__.py` - Add interpolation logic to execute function
- Modified: `examples/basic.config` - Add vars section for interpolation
- New exception: `UndefinedVariable` for missing variable references
- Enhanced error messages for command execution failures