# Testing Philosophy

This document describes the testing approach for jcli.

## Guiding Principles

### 1. Tests Document the Public Interface

Tests are the **second set of documentation** for your public API. When a maintainer (human or AI) wants to understand how to use `jcli.config`, they can:

1. Read the docstrings
2. Look at the tests in `tests/unit/test_config/`

**We test public interfaces only.** Private functions (`_helper`, `_internal`) are implementation details - not tested directly.

```python
# DO: Test the public API
from jcli.config import load_config
def test_load_config_merges_sources():
    ...

# DON'T: Test private implementation
def test_internal_merge_function():  # No
    ...
```

### 2. TDD Workflow

1. Write a failing test for the desired behavior
2. Write minimal code to pass the test
3. Refactor (tests keep you safe)

### 3. Test Structure

```
tests/
├── unit/                    # Fast, isolated, mocked
│   ├── test_config/
│   │   ├── test_loader.py
│   │   ├── test_sources.py
│   │   └── __init__.py
│   ├── test_presentation/
│   │   ├── test_base_presenter.py
│   │   ├── presenters/
│   │   │   ├── test_rich_presenter.py
│   │   │   └── ...
│   │   └── __init__.py
│   └── conftest.py          # Unit-level fixtures
├── integration/             # Tests across modules, no mocks
│   ├── test_config_sources.py
│   ├── test_presenter_factory.py
│   └── conftest.py
└── e2e/                     # Full CLI invocation, subprocess
    ├── test_cli_help.py
    └── conftest.py
```

| Layer | What it tests | Speed | Mocks |
|-------|---------------|-------|-------|
| Unit | Single class/function | Fast | Yes |
| Integration | Multiple modules together | Medium | No |
| E2E | Full CLI invocation | Slow | No |

## Fixtures and Factories

### Pytest Fixtures

Use `conftest.py` files to share fixtures at appropriate scopes:

```python
# tests/unit/conftest.py
import pytest
from jcli.config import ConfigLoader

@pytest.fixture
def config_loader():
    return ConfigLoader()
```

```python
# tests/unit/test_config/test_loader.py
def test_loader_something(config_loader):
    # config_loader is injected
    ...
```

### Factory Functions

Use factory functions to create test objects with sensible defaults:

```python
# tests/unit/test_presentation/conftest.py
import pytest
from jcli.presentation import RichPresenter

@pytest.fixture
def rich_presenter():
    def _create(**overrides):
        defaults = {"theme": "default", "verbose": False}
        return RichPresenter(**{**defaults, **overrides})
    return _create

def test_presenter_with_custom_theme(rich_presenter):
    presenter = rich_presenter(theme="dark")
    assert presenter.theme == "dark"
```

### Fixture Scopes

- **`function`** (default): New instance per test
- **`class`**: One instance per test class
- **`module`**: One instance per test file
- **`session`**: One instance for entire test run (rare - use for expensive setup)

## Running Tests

```bash
# All tests
pytest

# Unit tests only (fast)
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# E2E tests only
pytest tests/e2e/

# With coverage
pytest --cov=src --cov-report=term-missing

# Watch mode (rerun on changes)
pytest-watch
```

## What to Test

### Unit Tests
- Each public class/method has at least one test
- Test happy path
- Test edge cases (empty input, None, etc.)
- Test error conditions (invalid input raises appropriate error)

### Integration Tests
- How sources compose (env + file + CLI)
- Factory produces correct presenter types
- Config values interpolate correctly through the chain

### E2E Tests
- CLI help output
- Exit codes on success/failure
- Error messages are user-friendly

## What NOT to Test

- Private functions (`_private_method`)
- Implementation details (internal state that isn't part of the public API)
- Third-party library behavior (mock them)

## Maintainers

When adding a new module:
1. Add `tests/unit/test_<module>/`
2. Add `tests/integration/test_<module>/` if it composes with others
3. Document public interfaces in docstrings
4. Add examples in docstrings - they become testable documentation
