## ADDED Requirements

### Requirement: JCLI builder creates instances with app_name
The JCLI class SHALL provide a `builder(app_name: str)` class method that returns a new JCLI instance with the given app_name.

#### Scenario: Builder with app_name
- **WHEN** `jcli = JCLI.builder("myapp")`
- **THEN** `jcli.app_name` equals `"myapp"`

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

### Requirement: JCLI supports fluent add_argument
The JCLI instance SHALL provide an `add_argument(*args, **kwargs)` method that forwards to argparse and returns self for chaining.

#### Scenario: Add boolean flag
- **WHEN** `jcli.add_argument("--verbose", action="store_true")`
- **THEN** verbose argument is added to parser

#### Scenario: Add string argument
- **WHEN** `jcli.add_argument("--output", type=str, default="result.txt")`
- **THEN** output argument is available in parsed args

### Requirement: JCLI allows accessing module methods via attributes
The JCLI instance SHALL use `__getattr__` to delegate attribute access to registered modules.

#### Scenario: Access echo module
- **WHEN** `result = jcli.echo("hello")` after adding echo module
- **THEN** result equals `"hello"`

#### Scenario: Access config module
- **WHEN** `value = jcli.config.get("key", "default")` after adding config module
- **THEN** returns the config value or default

### Requirement: JCLI can parse arguments
The JCLI instance SHALL provide a `parse_args()` method that parses registered arguments and returns the namespace.

#### Scenario: Parse with default empty args
- **WHEN** `args = jcli.parse_args([])`
- **THEN** returns namespace with no attributes set

#### Scenario: Parse with custom args
- **WHEN** `jcli.add_argument("--quiet", action="store_true")` then `args = jcli.parse_args(["--quiet"])`
- **THEN** `args.quiet` is True

### Requirement: JCLI provides get_config method
The JCLI instance SHALL provide a `get_config()` method that loads configuration using the app_name and any registered config module options.

#### Scenario: Get config returns dict
- **WHEN** `config = jcli.get_config()`
- **THEN** returns a dictionary object

### Requirement: Config module supports --config argument
The config module SHALL automatically add `-c/--config` argument when registered.

#### Scenario: --config argument added
- **WHEN** `jcli.add_module("config")`
- **THEN** `-c` and `--config` arguments are available in the parser

#### Scenario: Valid config file with --config
- **WHEN** `--config /path/to/config.yaml` provided and file is readable
- **THEN** config loaded from specified file

#### Scenario: Invalid config file with --config
- **WHEN** `--config /nonexistent.yaml` provided and file is not readable
- **THEN** app exits with error message and code 1

### Requirement: Config module supports environment variable fallback
When --config is not specified, the config module SHALL check the environment variable specified during registration.

#### Scenario: Environment variable set and valid
- **WHEN** env var `MYCONFIG` is set to `/path/to/config.yaml` and file is readable
- **AND** `jcli.add_module("config", env="MYCONFIG")` without --config
- **THEN** config loaded from the file pointed to by env var

#### Scenario: Environment variable set but invalid
- **WHEN** env var `MYCONFIG` is set to `/nonexistent.yaml` and file is not readable
- **AND** `jcli.add_module("config", env="MYCONFIG")` without --config
- **THEN** app exits with error message and code 1

### Requirement: Config module supports default path fallback
When --config is not specified and env var is not set, the config module SHALL try the default path specified during registration.

#### Scenario: Default path valid
- **WHEN** `jcli.add_module("config", path="/path/to/config.yaml")` and file exists
- **AND** no --config or env var specified
- **THEN** config loaded from the default path

#### Scenario: Default path invalid
- **WHEN** `jcli.add_module("config", path="/nonexistent.yaml")` and file does not exist
- **AND** no --config or env var specified
- **THEN** returns empty config dict (not an error)
