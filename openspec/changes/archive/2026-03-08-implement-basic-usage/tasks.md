## 1. JCLI Builder Class Implementation

- [x] 1.1 Create `src/jcli/jcli.py` with JCLI class and `builder` class method
- [x] 1.2 Implement `__init__` to store app_name and initialize modules registry
- [x] 1.3 Implement `add_module(name, **options)` method with fluent chaining
- [x] 1.4 Implement `add_argument(*args, **kwargs)` method with fluent chaining
- [x] 1.5 Implement `__getattr__` for module attribute delegation
- [x] 1.6 Implement `parse_args()` method using internal ArgumentParser
- [x] 1.7 Implement `get_config()` method

## 2. Diag Module Implementation

- [x] 2.1 Create `src/jcli/diag/__init__.py` module
- [x] 2.2 Implement `diag(callback)` function that checks for `--diag` flag
- [x] 2.3 Add `--diag` argument to JCLI parser when diag module is registered

## 3. Integration

- [x] 3.1 Update `src/jcli/__init__.py` to export JCLI class
- [x] 3.2 Verify echo module integration works via `jcli.echo()`
- [x] 3.3 Verify config module integration works via `jcli.config.get()`

## 4. Testing

- [x] 4.1 Run existing tests to ensure no regressions
- [x] 4.2 Verify basic usage example from README works
