## 1. Commands Module Implementation

- [x] 1.1 Create `src/jcli/commands/__init__.py` module
- [x] 1.2 Define `CommandFailed` and `InvalidJSON` exception classes
- [x] 1.3 Implement `execute(command_string, format)` function using subprocess
- [x] 1.4 Add JSON parsing logic with error handling

## 2. JCLI Integration

- [x] 2.1 Update `JCLI._load_module()` to handle "commands" module
- [x] 2.2 Verify commands module accessible via `jcli.command.execute()`

## 3. Testing

- [x] 3.1 Create `tests/unit/test_commands/` directory
- [x] 3.2 Add unit tests for execute function with valid/invalid JSON
- [x] 3.3 Add tests for CommandFailed and InvalidJSON exceptions
- [x] 3.4 Add integration tests for JCLI commands module

## 4. Example Integration

- [x] 4.1 Update `examples/basic.py` to implement "list" argument (does not need commands module)
- [x] 4.2 Update `examples/basic.py` to use commands module for "count" subcommand
- [x] 4.3 Test example with actual command execution
