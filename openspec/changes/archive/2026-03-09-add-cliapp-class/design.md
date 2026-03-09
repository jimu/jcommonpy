## Context

jcli is a Python package providing reusable modules for CLI applications, focusing on config management and presentation layers. Currently, developers building CLI apps must manually handle argparse setup and config file loading, which requires understanding of these libraries. This design introduces a high-level CLIApp class to abstract these complexities, allowing developers to focus on app logic rather than boilerplate.

## Goals / Non-Goals

**Goals:**
- Provide a simple API for registering modules and handling configuration
- Enable CLI app creation without argparse knowledge
- Maintain compatibility with existing jcli modules

**Non-Goals:**
- Modify existing low-level APIs or module interfaces
- Add new modules or change module behavior
- Support highly customized argument parsing

## Decisions

- **Class Structure**: CLIApp class with `__init__`, `register_module`, `parse_args`, `get_config`, `add_argument` methods. ArgumentParser created in `__init__`. Stored in `src/jcli/cliapp.py` and exported in `__init__.py`.
- **Module Registration**: Accept string module names (e.g., 'echo', 'config'). Internally map to module classes that implement an `add_arguments(parser)` method for parser extension.
- **Argument Parsing**: ArgumentParser created in `__init__`. `register_module()` and `add_argument()` add arguments progressively to the parser. `parse_args()` parses `sys.argv` and returns the namespace. Parser becomes immutable after parsing.
- **Configuration Loading**: `get_config()` uses existing `config.load_config()` with sources derived from `app_name` and `hints`, returning a merged config dict.
- **Module Discovery**: Predefined registry of available modules to validate registration and provide instances.

## Risks / Trade-offs

- [Module naming conflicts] → Mitigation: Use kebab-case names and validate uniqueness
- [Limited customization] → Trade-off: Prioritizes simplicity over advanced argparse features; advanced users can use low-level APIs
- [Performance overhead] → Mitigation: Lazy loading of modules and caching where possible
- [Parser immutability after parsing] → Mitigation: Document that all arguments must be added before calling parse_args()