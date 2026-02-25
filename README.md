# jcli

A collection of reusable modules for building CLI applications in Python.

## Overview

jcli provides common building blocks for CLI apps so you don't have to reinvent the wheel each time. Import only what you need:

```python
from jcli.echo import echo, echos parameter (reference module)
from jcli.config import load_config, interpolate # TBD
from jcli.presentation import BasePresenter, RichPresenter # TBD
```

## Modules

| Module | Description | TBD |
|--------|-------------|-----|
| `jcli.echo` | Reference module - echos parameter | TBD |
| `jcli.config` | Configuration management - env vars, CLI args, YAML files, interpolation | TBD |
| `jcli.presentation` | Pluggable output presenters - Log, Text, Rich, HTML, CSV | TBD |

## Quick Start

```python
from jcli.echo import echo

echo("Hello World!")
=> "Hello, World!"
```

## Design Philosophy

### Lightweight Imports
Consumers import only the modules they use. This keeps AI coding agents' context lightweight.

```python
# Only import what you need - presentation module stays unloaded
from jcli.config import load_config
```

### AI Discoverability
- All public interfaces have type annotations
- Docstrings on modules, classes, and public methods
- Explicit `__all__` exports in every module
- Single import path: `from jcli.<module> import <PublicClass>`

### Public vs Private
- **Public**: Anything importable from `jcli.<module>` - stable, documented, tested
- **Private**: Anything prefixed with `_` - implementation detail, subject to change

### Opinionated Defaults
Sensible defaults out of the box, but extensible when you need more control.

## Installation

TBD

# Run tests
just test

## Testing Philosophy

See [tests/README.md](tests/README.md) for detailed testing philosophy and structure.
