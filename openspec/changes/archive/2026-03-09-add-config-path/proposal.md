## Why

The diagnostic module attempts to print the config file path via `jcli.config.config_path`, but this property is not implemented. This change enables proper diagnostic reporting of configuration usage.

## What Changes

- Add `config_path` property to the config module that returns the pathname of the configuration file currently in use.

## Capabilities

### New Capabilities
- `config-path`: Provides access to the configuration file pathname currently being used by the CLI application.

### Modified Capabilities

## Impact

- Affects the config module API by adding a new property.
- Enables the diag module to correctly display config file information.
- No breaking changes to existing functionality.</content>
<parameter name="filePath">/home/jimu/proj/oc/jcli/openspec/changes/add-config-path/proposal.md