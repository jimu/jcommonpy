## 1. JCLI Builder Class Implementation

- [ ] 1.1 Create `src/jcli/jcli.py` with JCLI class and `builder` class method
- [ ] 1.2 Implement `__init__` to store app_name and initialize modules registry
- [ ] 1.3 Implement `add_module(name, **options)` method with fluent chaining
- [ ] 1.4 Implement `add_argument(*args, **kwargs)` method with fluent chaining
- [ ] 1.5 Implement `__getattr__` for module attribute delegation
- [ ] 1.6 Implement `parse_args()` method using internal ArgumentParser
- [ ] 1.7 Implement `get_config()` method

## 2. Diag Module Implementation

- [ ] 2.1 Create `src/jcli/diag/__init__.py` module
- [ ] 2.2 Implement `diag(callback)` function that checks for `--diag` flag
- [ ] 2.3 Add `--diag` argument to JCLI parser when diag module is registered

## 3. Integration

- [ ] 3.1 Update `src/jcli/__init__.py` to export JCLI class
- [ ] 3.2 Verify echo module integration works via `jcli.echo()`
- [ ] 3.3 Verify config module integration works via `jcli.config.get()`

## 4. Testing

- [ ] 4.1 Run existing tests to ensure no regressions
- [ ] 4.2 Verify basic usage example from README works
