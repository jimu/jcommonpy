# Echo

## Purpose
Provides string echoing functionality for CLI applications. Serves as a simple reference implementation and utility module.

## Requirements

### Requirement: Echo function accepts optional message parameter
The echo function SHALL accept an optional `message` parameter of type `str | None` with a default value of `"Hello, World!"`.

#### Scenario: Message parameter provided
- **WHEN** echo function is called with a string message
- **THEN** it SHALL return the provided message unchanged

#### Scenario: No message parameter provided
- **WHEN** echo function is called without parameters
- **THEN** it SHALL return the default message "Hello, World!"

### Requirement: Echo function has proper type annotations
The echo function SHALL have complete type annotations for all parameters and return values using Python 3.10+ union syntax.

#### Scenario: Type annotations are present
- **WHEN** inspecting the echo function signature
- **THEN** it SHALL show `message: str | None = "Hello, World!"` parameter type and `str` return type