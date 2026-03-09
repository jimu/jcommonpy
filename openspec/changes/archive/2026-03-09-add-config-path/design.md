## Context

JCLI's config module loads configuration from YAML files but does not expose the pathname of the file currently in use. The diagnostic module attempts to access this via `jcli.config.config_path`, which is not implemented.

## Goals / Non-Goals

**Goals:**
- Add `config_path` property to the config module that returns the pathname of the configuration file in use.
- Enable diagnostic reporting of config file location.

**Non-Goals:**
- Changing the existing `load_config` function signature or behavior.
- Modifying configuration loading logic beyond what's needed for path exposure.

## Decisions

- **Property Location**: Add `config_path` as a property on the `ConfigWrapper` class, which wraps the config module functionality.
- **Path Resolution**: Replicate the path finding logic from `load_config` in the property getter to determine the active config file path.
- **Return Type**: Return `str | None` - the absolute path as string if a config file is in use, None if no config file (using defaults).
- **Caching**: Do not cache the path separately; recompute on each access since it's lightweight and ensures consistency.

## Risks / Trade-offs

- **Code Duplication**: Path resolution logic is duplicated between `load_config` and `config_path`. If the logic in `load_config` changes, both need updates.
- **Performance**: Minimal impact since path resolution is simple file system checks.
- **API Consistency**: Adding a property to the wrapper maintains the module's API style.</content>
<parameter name="filePath">/home/jimu/proj/oc/jcli/openspec/changes/add-config-path/design.md