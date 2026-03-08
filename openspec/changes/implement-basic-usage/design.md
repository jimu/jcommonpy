## Context

The README.md Quick Start section demonstrates a desired fluent builder API for composing CLI applications:

```python
jcli = JCLI.builder("my-app-name")
    .add_module("echo")
    .add_argument("--verbose", action="store_true", help="Display verbose output")
    .add_module("config", path="~/.myapprc", env="MYAPPRC")
    .add_module("diag", mydiag)

jcli.echo("Hello World!")
jcli.config.get("mykey", "default value")
```

Currently, the `JCLI` class does not exist. The echo module exists as a standalone function, config module is a stub, and the diag module doesn't exist.

## Goals / Non-Goals

**Goals:**
- Implement `JCLI` builder class with fluent API
- Support registering echo, config, and diag modules
- Allow adding custom arguments via `add_argument`
- Enable direct access to module methods via `jcli.echo()`, `jcli.config.get()`, etc.
- Implement diag module that calls callback and exits when `--diag` flag is used

**Non-Goals:**
- Full-featured CLI framework (argparse wrapper only, not a complete CLI framework like Click)
- Module loading from external plugins (only built-in modules supported initially)
- Async support or complex configuration merging logic

## Decisions

### 1. JCLI builder pattern using class method
**Decision:** Use `JCLI.builder(app_name)` as the entry point instead of `JCLI(app_name)`.

**Rationale:** The builder pattern allows progressive configuration before "building" the final instance. Matches the README example exactly.

### 2. Lazy module initialization
**Decision:** Modules are registered but not permitted or instantiated unless enabled/configured by the builder.

**Rationale:** Keeps startup fast; only loads modules that are actually used. Allows passing options to `add_module()` that configure how the module initializes.

### 3. Attribute-based module access via `__getattr__`
**Decision:** Use Python's `__getattr__` to delegate attribute access to registered modules.

**Rationale:** Enables the clean `jcli.echo()` syntax from the README. Modules are looked up dynamically by name.

### 4. Internal ArgumentParser
**Decision:** JCLI maintains the application's argparse.ArgumentParser instance.

**Rationale:** The README shows `.add_argument()` as part of the fluent API.

### 5. Diag module with callback
**Decision:** The diag module accepts a callable in `add_module("diag", callback)`.

**Rationale:** The callback is user-defined and called when `--diag` is passed. Matches the README example pattern.

## Risks / Trade-offs

- **[Risk]** Module name conflicts with Python built-ins or jcli internal attributes
  - **Mitigation:** Use a whitelist of allowed module names (echo, config, diag) and raise clear errors for unknown modules

- **[Risk]** No clear "run" or "execute" entry point in the API
  - **Mitigation:** The current design is for method chaining; actual execution happens by calling module methods directly. This matches the README example.

- **[Risk]** Config module is currently a stub and returns empty dict
  - **Mitigation:** Accept that config.get() will return defaults until the config module is fully implemented. The JCLI integration is still valid.
