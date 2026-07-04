# Contributing to PyRestKit

Thank you for your interest in contributing to PyRestKit.

## Development Setup

Clone the repository:

```bash
git clone https://github.com/Raushanraj77/pyrestkit.git
cd pyrestkit
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Quality Checks

Before creating a pull request, ensure all quality checks pass:

```bash
make check
```

This executes:

* Ruff (Linting)
* MyPy (Static Type Checking)
* Pytest (Unit Tests)

## Coding Standards

* Follow PEP 8
* Use type hints
* Keep functions focused and maintainable
* Add unit tests for new functionality
* Maintain backward compatibility whenever possible

## Commit Messages

This project follows Conventional Commits.

Examples:

* feat: add OAuth2 authentication
* fix: handle empty JSON response
* refactor: simplify request builder
* test: add schema validation tests
* docs: update README
* ci: add GitHub Actions workflow

## Pull Requests

Please ensure:

* All tests pass
* Ruff passes
* MyPy passes
* Documentation is updated where necessary
* New functionality includes unit tests

Thank you for helping improve PyRestKit.
