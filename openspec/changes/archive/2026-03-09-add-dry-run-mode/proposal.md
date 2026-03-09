## Why

Users need a way to preview command execution without actually running commands, which is useful for testing configurations, understanding what will happen, or debugging command strings before execution. This is particularly important when working with potentially destructive or long-running commands.

## What Changes

- Add `--dry-run` (`-n`) flag to JCLI when the commands module is enabled
- When dry-run is enabled, commands are printed to stdout instead of being executed
- Commands are also printed when `--verbose` (`-v`) flag is enabled, regardless of dry-run mode
- No breaking changes to existing APIs or command formats

## Capabilities

### New Capabilities

### Modified Capabilities
- `commands-module`: Add dry-run and verbose execution modes that change command execution behavior

## Impact

- Affects JCLI argument parsing and command execution flow
- Commands module will need to check for dry-run/verbose flags
- No changes to existing command string formats or config files