## Context

The commands module needs to support variable interpolation in command strings to enable reusable command templates. Command strings can contain placeholders like `[var-name]` that get replaced with values from the configuration's `vars` section before execution. This allows users to define parameterized commands that can be customized via configuration without code changes.

Current state: Commands module executes shell commands and parses JSON output. No variable substitution exists.

## Goals / Non-Goals

**Goals:**
- Parse `[var-name]` placeholders in command strings
- Replace placeholders with values from config `vars` section
- Validate all placeholders have corresponding variable definitions
- Perform interpolation before command execution
- Maintain backward compatibility for commands without placeholders

**Non-Goals:**
- Support for different placeholder syntaxes (only `[var-name]`)
- Variable expressions or functions (only simple substitution)
- Environment variable interpolation (only config vars)
- Nested variable references

## Decisions

### 1. Interpolation timing and location
**Decision:** Perform interpolation in the `execute` function, immediately before subprocess execution.

**Rationale:** Ensures commands are interpolated with current config values at execution time. Keeps interpolation logic contained within the commands module.

**Alternatives considered:**
- Interpolate when commands are loaded from config: Would cache interpolated commands, preventing dynamic config changes.
- Interpolate in JCLI before passing to execute: Would spread interpolation logic across modules.

### 2. Placeholder syntax and validation
**Decision:** Use regex to find all `[var-name]` patterns and validate all are defined before any substitution.

**Rationale:** Regex provides robust parsing. Validating all placeholders upfront prevents partial interpolation states and provides clear error messages.

**Alternatives considered:**
- String replace without validation: Could leave undefined placeholders, leading to confusing command failures.
- Lazy validation: Would interpolate one at a time, potentially masking multiple undefined variables.

### 3. Config access for variables
**Decision:** Pass config object to execute function so it can access the `vars` section.

**Rationale:** Commands module needs access to the same config that contains the commands. This ensures variables come from the correct config source.

**Alternatives considered:**
- Global config access: Would couple commands module to global state.
- Separate vars parameter: Would complicate the API and require callers to manage config access.

### 4. Exception for undefined variables
**Decision:** Create `UndefinedVariable` exception that includes the variable name and available variables.

**Rationale:** Provides clear error information for debugging. Follows existing pattern of specific exceptions (CommandFailed, InvalidJSON).

**Alternatives considered:**
- Reuse existing exceptions: Would be less specific about the error type.
- Return error strings: Less Pythonic than exceptions.

## Risks / Trade-offs

- **[Risk]** Regex performance on very long command strings
  - **Mitigation:** Commands are typically short, regex is efficient for normal use cases.

- **[Risk]** Config changes during execution could affect interpolation
  - **Mitigation:** Config is loaded once at JCLI build time, remains stable during execution.

- **[Risk]** Variable names could conflict with command syntax
  - **Mitigation:** Document that variable names should be chosen to avoid conflicts with command arguments.

- **[Risk]** Complex interpolation could hide command injection risks
  - **Mitigation:** Variables come from trusted config files, not user input. Document security considerations.