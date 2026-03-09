# jcli

A collection of reusable modules for building CLI applications in Python.

## Overview

jcli provides common building blocks for CLI apps so you don't have to reinvent the wheel each time. Import only what you need:

```python
from jcli.echo import echo, echos parameter (reference module)
from jcli.diag import diag
from jcli.config import load_config, interpolate # TBD
from jcli.presentation import BasePresenter, RichPresenter # TBD
```

## Modules

| Module | Description | TBD |
|--------|-------------|-----|
| `jcli.echo` | Reference module - echos given parameter | TBD |
| `jcli.diag` | Reference module - calls given function when '--diag' and exits
| `jcli.config` | Configuration management - env vars, CLI args, YAML files, interpolation
| `jcli.presentation` | Pluggable output presenters - Log, Text, Rich, HTML, CSV | TBD |

## Quick Start

```python
from jcli import JCLI

jcli = JCLI.builder("my-app-name")
    .add_module("echo")
    .add_argument("--verbose", action="store_true", help="Display verbose output")
    .add_module("config", path="~/.myapprc", env="MYAPPRC")
    .add_module("diag", mydiag)

# defines the callback function supplied to the diag module
def mydiag() -> None:
    print("any diagnostic output")

# uses the echo module
jcli.echo("Hello World!")

# returns value from configuration file
jcli.config.get("mykey", "default value")

# parse arguments (diag runs automatically if --diag is passed)
args = jcli.parse_args()
```

## Running the Example

Install jcli in your environment, then run:

```bash
# Install jcli
uv pip install -e .

# Run the example
python examples/basic.py
python examples/basic.py --verbose
python examples/basic.py --diag

# Or run directly (add project to PATH first)
./basic
./basic --verbose
./basic --diag
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

```bash
# Install jcli
uv pip install -e .
```

## Running Tests

```bash
just test
```

## Testing Philosophy

See [tests/README.md](tests/README.md) for detailed testing philosophy and structure.
