# JCLI Builder

## Purpose

Provides a unified builder API for composing CLI applications from modules (echo, config, diag, commands).

## MODIFIED Requirements

### Requirement: JCLI supports fluent add_module
The JCLI instance SHALL provide an `add_module(name: str, **options)` method that registers a module and returns self for chaining.

#### Scenario: Add echo module
- **WHEN** `jcli.add_module("echo")`
- **THEN** echo module is registered and method returns `jcli` instance

#### Scenario: Add config module with options
- **WHEN** `jcli.add_module("config", path="~/.myapprc", env="MYAPPRC")`
- **THEN** config module is registered with path and env options

#### Scenario: Add diag module with callback
- **WHEN** `jcli.add_module("diag", my_callback)`
- **THEN** diag module is registered with the provided callback

#### Scenario: Add commands module
- **WHEN** `jcli.add_module("commands")`
- **THEN** commands module is registered and method returns `jcli` instance