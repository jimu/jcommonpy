# CLI App

## Purpose

Provides a simple CLI application framework for registering modules, parsing arguments, and loading configuration.

## ADDED Requirements

### Requirement: CLIApp initialization
The CLIApp class SHALL accept an app_name string and optional hints dict in its __init__ method.

#### Scenario: Initialization with app_name
- **WHEN** app = CLIApp('myapp')
- **THEN** app stores 'myapp' as app_name and empty hints if none provided

#### Scenario: Initialization with hints
- **WHEN** app = CLIApp('myapp', config_dir='~/.config/myapp')
- **THEN** app stores hints for config loading

### Requirement: Module registration
The CLIApp SHALL provide a register_module method that accepts a module name string and adds it to the list of registered modules.

#### Scenario: Register echo module
- **WHEN** app.register_module('echo')
- **THEN** 'echo' is added to registered modules

#### Scenario: Register config module
- **WHEN** app.register_module('config')
- **THEN** 'config' is added to registered modules

### Requirement: Argument parsing
The CLIApp SHALL initialize an ArgumentParser in __init__, add arguments progressively via register_module and add_argument, and provide a parse_args method that parses the configured arguments and returns the parsed args namespace.

#### Scenario: Parse with registered modules
- **WHEN** args = app.parse_args() after registering modules
- **THEN** returns namespace with module arguments parsed

#### Scenario: Parse with custom args
- **WHEN** app.add_argument('-q', '--quiet'); args = app.parse_args()
- **THEN** args.quiet is available in namespace

### Requirement: Configuration loading
The CLIApp SHALL provide a get_config method that loads configuration from sources based on app_name and hints, returning a merged dict.

#### Scenario: Get config with app_name
- **WHEN** config = app.get_config() with app_name set
- **THEN** returns dict loaded from default sources using app_name

#### Scenario: Get config with hints
- **WHEN** config = app.get_config() with hints provided
- **THEN** uses hints to locate config files

### Requirement: Custom argument addition
The CLIApp SHALL provide an add_argument method that forwards to the internal ArgumentParser to allow app-specific arguments.

#### Scenario: Add quiet flag
- **WHEN** app.add_argument('-q', '--quiet', action='store_true')
- **THEN** quiet argument is added to parser

#### Scenario: Add multiple custom args
- **WHEN** app.add_argument('--verbose'); app.add_argument('--output', type=str)
- **THEN** both args are added to parser