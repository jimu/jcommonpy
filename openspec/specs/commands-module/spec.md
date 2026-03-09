# Commands Module

## Purpose

Provides functionality for executing shell commands that return JSON data, with automatic parsing and error handling.

## ADDED Requirements

### Requirement: Commands module executes shell commands and parses JSON
The commands module SHALL provide a method to execute shell commands and parse their JSON output.

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