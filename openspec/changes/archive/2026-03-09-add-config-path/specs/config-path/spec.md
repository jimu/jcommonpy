## ADDED Requirements

### Requirement: Config Path Access
The config module SHALL expose a `config_path` property that returns the absolute pathname of the configuration file currently in use, or None if no configuration file is loaded.

#### Scenario: Config file specified via --config argument
- **WHEN** a config file is specified using the --config CLI argument
- **THEN** config_path SHALL return the absolute path of that file

#### Scenario: Config file specified via environment variable
- **WHEN** no --config is provided but an environment variable points to a valid config file
- **THEN** config_path SHALL return the absolute path from the environment variable

#### Scenario: Config file found at default path
- **WHEN** no --config or environment variable, but a config file exists at the specified path option
- **THEN** config_path SHALL return the absolute path of the default config file

#### Scenario: No config file in use
- **WHEN** no config file is loaded (using defaults)
- **THEN** config_path SHALL return None</content>
<parameter name="filePath">/home/jimu/proj/oc/jcli/openspec/changes/add-config-path/specs/config-path/spec.md