## Context

The commands module currently executes shell commands and parses their JSON output. Users need visibility into what commands would execute without actually running them, especially for potentially destructive operations. The proposal adds --dry-run and --verbose flags to provide this functionality.

## Goals / Non-Goals

**Goals:**
- Add --dry-run (-n) flag that prints commands instead of executing them
- Add --verbose (-v) flag that prints commands regardless of dry-run mode
- Maintain existing command execution behavior when flags are not used
- No breaking changes to existing APIs or command formats

**Non-Goals:**
- Changing command string interpolation or parsing logic
- Adding dry-run support to other JCLI modules
- Modifying existing command execution error handling

## Decisions

**Flag Implementation:**
- Add --dry-run (-n) and --verbose (-v) flags to JCLI argument parser when commands module is enabled
- Store flag values in JCLI instance for access by commands wrapper
- Pass dry-run and verbose states to execute method as parameters

**Execution Logic:**
- Modify commands.execute() to accept dry_run and verbose parameters
- When dry_run=True, print command and return mock success result
- When verbose=True, print command before execution
- Preserve existing execution flow when both flags are False

**Result Handling:**
- For dry-run, return a mock JSON result (e.g., {"dry_run": true}) instead of executing
- For verbose execution, print command but still execute normally

## Risks / Trade-offs

**Risk:** Users might assume dry-run prevents all side effects → **Mitigation:** Clearly document that dry-run only affects command execution, not argument parsing or interpolation

**Risk:** Verbose output could clutter logs in production → **Mitigation:** Verbose flag is opt-in and clearly named

**Trade-off:** Added parameters to execute method → **Rationale:** Clean API that doesn't break existing code, flags are optional