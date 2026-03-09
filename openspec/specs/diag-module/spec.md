# Diag Module

## Purpose

Provides diagnostic functionality for CLI applications - calls a callback function when `--diag` flag is passed and exits.

## ADDED Requirements

### Requirement: Diag module registers callback with add_module
The diag module SHALL accept a callback function when registered via `add_module("diag", callback)`.

#### Scenario: Register diag with callback
- **WHEN** `jcli.add_module("diag", my_callback)`
- **THEN** the callback is stored for later execution

### Requirement: Diag module auto-adds --diag argument
The diag module SHALL automatically add `--diag` argument to the parser when registered.

#### Scenario: --diag argument added automatically
- **WHEN** `jcli.add_module("diag", callback)`
- **THEN** `--diag` flag is available in the parser

### Requirement: Diag callback executes and exits when --diag is passed
When the JCLI app is run with `--diag` flag, the registered callback SHALL be executed and the app SHALL exit automatically without requiring any manual method calls.

#### Scenario: Callback executes on --diag
- **WHEN** app is run with `--diag` argument
- **THEN** callback is executed and app exits with code 0

#### Scenario: No callback provided
- **WHEN** `jcli.add_module("diag")` without callback
- **AND** app is run with `--diag`
- **THEN** app exits with code 0 without error
