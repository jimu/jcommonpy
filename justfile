# Justfile – Python project with uv + ruff + pytest
# Run `just` (with no arguments) to see this list

set shell := ["bash", "-c"]

default: list

# ────────────────────────────────────────────────────────────────────────────
# Show help ───────────────────────────────────────────────────────────────────
# ────────────────────────────────────────────────────────────────────────────

# Show available recipes
list:
    @just --list --unsorted

# ────────────────────────────────────────────────────────────────────────────
# Core development workflow ──────────────────────────────────────────────────
# ────────────────────────────────────────────────────────────────────────────

# Install/update all dependencies (including dev) → fastest with uv
sync:
    uv sync --frozen

# Force full sync + upgrade dev dependencies
sync-dev:
    uv sync --all-extras --upgrade

# Update the lockfile
lock:
    uv lock --upgrade

# Format code with ruff
format:
    uv run ruff format .

# Run ruff lint (with auto-fix where safe)
lint:
    uv run ruff check --fix .

# Lint without fixing (CI-friendly)
lint-check:
    uv run ruff check --diff --no-fix

# Run mypy (if configured)
typecheck:
    uv run mypy src tests

# Run tests (fast default)
test:
    uv run pytest --tb=short

# Tests + coverage report (html + terminal missing)
test-cov:
    uv run pytest --cov=src --cov-report=html --cov-report=term-missing

# Full test suite + coverage + warnings treated as errors
test-all:
    uv run pytest --cov=src -W error --cov-report=term-missing

# ────────────────────────────────────────────────────────────────────────────
# Quality & safety checks ────────────────────────────────────────────────────
# ────────────────────────────────────────────────────────────────────────────

# Recommended pre-PR / pre-merge sequence
check: format lint-check test-cov
    @echo ""
    @echo "All checks passed ✓"

# Run all pre-commit hooks on staged files
pre-commit:
    uv run pre-commit run --all-files

# ────────────────────────────────────────────────────────────────────────────
# Utilities ──────────────────────────────────────────────────────────────────
# ────────────────────────────────────────────────────────────────────────────

# Remove common temporary & build files
clean:
    rm -rf .coverage htmlcov/ .pytest_cache/ .ruff_cache/ .mypy_cache/
    find . -type d -name "__pycache__" -exec rm -rf {} +
    find . -type d -name "*.egg-info" -exec rm -rf {} +
    find . -type f -name "*.py[co]" -delete

# Show dependency tree
deps-tree:
    uv tree

# Show outdated packages
deps-outdated:
    uv pip list --outdated

# ────────────────────────────────────────────────────────────────────────────
# One-liners for common workflows ────────────────────────────────────────────
# ────────────────────────────────────────────────────────────────────────────

# Prepare fresh environment + checks
dev-ready: sync format lint test

# Typical minimal CI job
ci: lint-check test-all

# Strict quality gate
quality: check pre-commit

# ────────────────────────────────────────────────────────────────────────────
# Optional / commented-out recipes (uncomment as needed) ─────────────────────
# ────────────────────────────────────────────────────────────────────────────

# Build & serve documentation (mkdocs / sphinx)
# docs:
#     uv run mkdocs serve

Build wheel + sdist
build:
    uv build

# Upload to TestPyPI
# publish-test: build
#     uv publish --index testpypi
