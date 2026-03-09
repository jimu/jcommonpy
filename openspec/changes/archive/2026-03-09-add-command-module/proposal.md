## Why

CLI applications often need to aggregate data from multiple external commands or tools. Users want a simple way to define command pipelines in configuration and execute them through a unified interface, with automatic JSON parsing and result aggregation.

## What Changes

- jcli
  - Add `commands` module to JCLI that can execute shell commands and parse JSON responses
  - Extend JCLI builder with `.add_module("commands")` to enable command execution
  - jcli.command.execute(command_string, "json") executes command and returns parsed JSON array
  - Commands module raises exceptions for command failures or invalid JSON; application decides how to handle (abort, warn, etc.)

- Application-level CLI logic (example in basic.py)
  - Commands are defined in config file under "commands" section as key-value pairs (application convention)
  - "list" subcommand: Lists command keys (application-level feature, not in commands module)
  - "count" subcommand: Executes each command via commands module, counts JSON array items, displays results (application-level feature)
  - Application catches and handles exceptions from commands module (abort on errors)


## Capabilities

### New Capabilities
- `commands-module`: Module for executing shell commands that return JSON data and aggregating results

### Modified Capabilities
- `jcli-builder`: Extended to support commands module registration

## Impact

- New file: `src/jcli/commands/__init__.py` - Commands module implementation
- Modified: `src/jcli/jcli.py` - Add commands module support
- Modified: `examples/basic.py` - Demonstrate commands usage
- New dependency: `subprocess` module (already in stdlib)