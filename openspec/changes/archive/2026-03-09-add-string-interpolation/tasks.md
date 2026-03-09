## 1. Commands Module Updates

- [x] 1.1 Add UndefinedVariable exception class
- [x] 1.2 Implement placeholder parsing with regex
- [x] 1.3 Add variable validation logic
- [x] 1.4 Implement string substitution logic
- [x] 1.5 Modify execute function to use config from JCLI context

## 2. JCLI Integration Updates

- [x] 2.1 Update _load_module to provide config access to commands module
- [x] 2.2 Create CommandsWrapper to provide config access (replaces ConfigWrapper modification)
- [x] 2.3 Test that commands module can access config vars

## 3. Testing

- [x] 3.1 Add unit tests for interpolation functionality
- [x] 3.2 Add tests for UndefinedVariable exception
- [x] 3.3 Add integration tests with config vars
- [x] 3.4 Test error cases with undefined variables

## 4. Example Updates

- [x] 4.1 Verify examples/basic.config has proper vars section
- [x] 4.2 Test interpolation works with existing example commands