# String Interpolation

## Purpose

Provides variable substitution functionality for command strings using configuration values.

## ADDED Requirements

### Requirement: String interpolation substitutes variables in command strings
The string interpolation system SHALL replace `[var-name]` placeholders in command strings with values from the config `vars` section.

#### Scenario: Simple variable substitution
- **WHEN** command string contains `[var-name]` and config has `vars.var-name = "value"`
- **THEN** placeholder is replaced with the variable value

#### Scenario: Multiple variable substitutions in one command
- **WHEN** command string contains multiple different placeholders
- **THEN** all placeholders are replaced with their respective values

#### Scenario: Variable not defined in config
- **WHEN** command string contains `[undefined-var]` and config vars section does not have this key
- **THEN** raises `UndefinedVariable` exception

### Requirement: Interpolation uses same config source as commands
The interpolation system SHALL use the same configuration source that contains the commands section.

#### Scenario: Variables from same config file
- **WHEN** commands and vars are in the same config file
- **THEN** interpolation uses values from that file's vars section

#### Scenario: Commands and vars from different config sources
- **WHEN** commands loaded from one source and vars from another
- **THEN** interpolation uses the vars from the source containing the commands