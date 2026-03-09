## 1. Implement CLIApp class

- [x] 1.1 Create src/jcli/cliapp.py with CLIApp class
- [x] 1.2 Implement __init__ method (app_name, hints, initialize ArgumentParser)
- [x] 1.3 Implement register_module method (add module arguments to parser)
- [x] 1.4 Implement parse_args method (parse the pre-configured parser)
- [x] 1.5 Implement get_config method
- [x] 1.6 Implement add_argument method (add custom arguments to parser)

## 2. Module registry

- [x] 2.1 Define registry of available modules with add_arguments methods
- [x] 2.2 Add validation for module names in register_module

## 3. Configuration integration

- [x] 3.1 Import config.load_config in get_config
- [x] 3.2 Handle hints in config loading

## 4. Package updates

- [x] 4.1 Export CLIApp in src/jcli/__init__.py

## 5. Testing

- [x] 5.1 Write unit tests for all methods
- [x] 5.2 Test example usage from proposal
- [x] 5.3 Run linter and tests