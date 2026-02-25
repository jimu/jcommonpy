# AGENTS.md - Guidance for AI Coding Agents

This file provides guidance for AI agents operating in this repository.

## Project Overview

jcli is a Python package providing reusable modules for CLI applications (config management, presentation layer, etc.). Consumers import only what they need.

## Build, Lint, and Test Commands

### Running Tests

```bash
# All tests
pytest

# Single test file
pytest tests/unit/test_config/test_loader.py

# Single test function
pytest tests/unit/test_config/test_loader.py::test_load_config_merges_sources

# Run by marker
pytest -m unit        # Unit tests only
pytest -m integration # Integration tests only
pytest -m e2e         # E2E tests only

# With coverage
pytest --cov=src --cov-report=term-missing --cov-report=html
```

### Linting and Formatting

```bash
# Run all linters
just lint
```

### Building

```bash
# Install in development mode
pip install -e ".[dev]"

# Build package
just build

# Run pre-commit checks
just pre-commit
```

## Code Style Guidelines

### Imports

- Use absolute imports: `from jcli.config import Loader`
- Use `__all__` to explicitly declare public API

### Type Annotations

- All public functions MUST have type annotations
- Use `typing.TypeAlias` for complex type definitions
- Prefer `Protocol` for structural typing

### Docstrings

- Use Google-style docstrings for all public classes and functions
- Include: Description, Args, Returns, Raises
- Keep first line concise (under 79 chars)

### Public vs Private

- **Public**: Documented in `__all__`, stable API, tested
- **Private**: Prefix with `_`, implementation detail, not tested directly

### Testing Guidelines

See [tests/README.md](tests/README.md) for full details.

- Test public interfaces only (not private `_helper` functions)
- Use pytest fixtures for shared setup
- Use factory fixtures for test objects with defaults

### Module Structure

```
src/jcli/
├── __init__.py          # Re-exports public API
├── config/
│   ├── __init__.py      # Public API: Loader, load_config, interpolate
│   ├── loader.py
│   ├── sources.py
│   └── ...
└── presentation/
    ├── __init__.py      # Public API: BasePresenter, create_presenter
    ├── base.py
    └── presenters/
```
