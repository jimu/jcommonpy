## Context

The jcli framework needs to support executing external shell commands that return JSON data. This is required for applications that need to aggregate data from multiple command-line tools or scripts. The commands module will provide a clean API for executing commands and automatically parsing their JSON output, with proper error handling for command failures and invalid JSON.

Current state: jcli has echo, config, and diag modules. Commands module will be added as a new capability.

## Goals / Non-Goals

**Goals:**
- Provide `jcli.command.execute(command_string, "json")` method
- Execute shell commands safely using subprocess
- Automatically parse JSON output and return Python objects
- Raise clear exceptions for command failures and invalid JSON
- Integrate with existing jcli builder pattern

**Non-Goals:**
- Support for raw text output (only JSON)
- Command execution metadata (timing, exit codes in return value)
- Complex command pipelines or chaining
- Asynchronous command execution
- Command validation or sandboxing

## Decisions

### 1. Subprocess for command execution
**Decision:** Use Python's `subprocess` module with `run()` for executing shell commands.

**Rationale:** Standard library solution, provides good control over execution, handles stdout/stderr properly. More secure than `os.system()`.

**Alternatives considered:**
- `os.popen()`: Deprecated and less secure
- External libraries like `sh`: Adds dependencies, overkill for MVP

### 2. Exception-based error handling
**Decision:** Raise custom exceptions `CommandFailed` and `InvalidJSON` for different error conditions.

**Rationale:** Clear error types allow applications to handle different failures appropriately. Follows Python exception patterns.

**Alternatives considered:**
- Return error codes/tuples: Less Pythonic, harder to handle
- Logging errors: Doesn't allow programmatic handling

### 3. JSON-only output format
**Decision:** Only support JSON parsing, no raw text output.

**Rationale:** MVP scope focuses on JSON use case. Applications needing raw output can use subprocess directly.

**Alternatives considered:**
- Support multiple formats with format parameter: Increases complexity, not needed for MVP

### 4. Synchronous execution
**Decision:** Commands execute synchronously.

**Rationale:** Simple for MVP, matches typical CLI tool patterns. Async can be added later if needed.

**Alternatives considered:**
- Async execution: Adds complexity with asyncio/subprocess, not needed for MVP

## Risks / Trade-offs

- **[Risk]** Long-running commands block application
  - **Mitigation:** Applications can implement timeouts at the subprocess level if needed. MVP keeps it simple.

- **[Risk]** Platform differences in shell command execution
  - **Mitigation:** Use `subprocess.run()` with `shell=True` for cross-platform compatibility. Test on target platforms.

- **[Risk]** Large JSON outputs consume memory
  - **Mitigation:** JSON parsing loads entire output into memory. For very large outputs, applications can use raw subprocess calls.