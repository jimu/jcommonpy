## Context

The jcli package is being extended with a new `jcli.echo` module to provide a simple reference implementation and utility for CLI applications. This module serves as an example of how to structure jcli modules and provides basic functionality for testing package installation and configuration.

The module needs to be importable by consumers who only want this specific functionality without pulling in other jcli modules unnecessarily.

## Goals / Non-Goals

**Goals:**
- Provide a simple, well-documented echo function with clear type annotations
- Follow jcli's module structure and conventions
- Include comprehensive tests for the public interface
- Serve as a reference implementation for other jcli modules

**Non-Goals:**
- Complex string processing or manipulation beyond basic echoing
- Multiple echo variants or configuration options
- Integration with other jcli modules

## Decisions

**Module Structure:**
- Place in `src/jcli/echo/` directory following jcli's existing module layout
- Use `__init__.py` to export the public `echo` function
- Include proper `__all__` declaration for AI discoverability

**Public API Design:**
- Single `echo()` function with optional string parameter
- Use Python 3.10+ union syntax (`str | None`) for type hints
- Return the input string or default message

**Error Handling:**
- No exceptions for this simple function - rely on Python's natural behavior
- Input validation is minimal since it's a reference implementation

## Risks / Trade-offs

**[Risk] Default message hard-coded in function signature**
**[Mitigation]** Easy to change if needed, and serves as clear example in API docs

**[Risk] Module adds to package size**
**[Mitigation]** Minimal code footprint, justified as reference implementation

**[Risk] Could be seen as unnecessary utility**
**[Mitigation]** Provides clear value as installation test and module example