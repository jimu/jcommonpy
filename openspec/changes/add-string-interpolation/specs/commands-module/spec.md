# Commands Module

## Purpose

Provides functionality for executing shell commands that return JSON data, with automatic parsing and error handling.

## MODIFIED Requirements

### Requirement: Commands module executes shell commands and parses JSON
The commands module SHALL provide a method to execute shell commands and parse their JSON output. Command strings SHALL support variable interpolation using `[var-name]` placeholders before execution.

#### Scenario: Execute command with valid JSON array output
- **WHEN** `jcli.command.execute("echo '[]'", "json")` is called
- **THEN** returns empty array `[]`

#### Scenario: Execute command with valid JSON object output
- **WHEN** `jcli.command.execute("echo '{\"key\": \"value\"}'", "json")` is called
- **THEN** returns parsed object `{"key": "value"}`

#### Scenario: Execute command that fails
- **WHEN** `jcli.command.execute("false", "json")` is called (command exits non-zero)
- **THEN** raises `CommandFailed` exception with exit code and stderr

#### Scenario: Execute command with invalid JSON output
- **WHEN** `jcli.command.execute("echo 'invalid json'", "json")` is called
- **THEN** raises `InvalidJSON` exception with command output

#### Scenario: Execute command with variable interpolation
- **WHEN** `jcli.command.execute("[prefix]command", "json")` is called and config has `vars.prefix = "my"`
- **THEN** executes `"mycommand"` and returns parsed JSON

#### Scenario: Execute command with undefined variable
- **WHEN** `jcli.command.execute("[undefined]command", "json")` is called and undefined is not in vars
- **THEN** raises `UndefinedVariable` exception

### Requirement: Commands module handles interpolation errors
The commands module SHALL validate all variable placeholders in command strings and raise appropriate exceptions for undefined variables.

#### Scenario: Multiple undefined variables in command
- **WHEN** command contains `[undefined1]` and `[undefined2]` neither defined in vars
- **THEN** raises `UndefinedVariable` exception for the first undefined variable encountered

#### Scenario: Mixed defined and undefined variables
- **WHEN** command contains `[defined]` and `[undefined]`, where defined exists in vars but undefined does not
- **THEN** raises `UndefinedVariable` exception for the undefined variable