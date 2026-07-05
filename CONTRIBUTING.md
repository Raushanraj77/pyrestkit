# Contributing

Thank you for your interest in contributing to PyRestKit.

Whether you are fixing a bug, improving documentation, adding a new AI provider, or implementing a new feature, your contribution is appreciated.

This guide explains the development workflow, coding standards, testing requirements, and contribution process.

---

# Project Philosophy

PyRestKit is built around several core principles:

* Simple APIs
* Strong typing
* Readable code
* Comprehensive testing
* Clear documentation
* Provider independence
* Modular architecture

Every contribution should align with these goals.

---

# Development Environment

Clone the repository:

```bash
git clone https://github.com/Raushanraj77/pyrestkit.git

cd pyrestkit
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

Install development dependencies:

```bash
pip install -e ".[dev]"
```

---

# Project Structure

```text
pyrestkit/
│
├── pyrestkit/
│   ├── ai/
│   ├── auth/
│   ├── client/
│   ├── models/
│   ├── validators/
│   ├── exceptions/
│   └── utils/
│
├── tests/
│
├── docs/
│
├── examples/
│
└── pyproject.toml
```

Each package has a clearly defined responsibility.

Avoid creating cross-package dependencies unless absolutely necessary.

---

# Coding Standards

PyRestKit follows:

* PEP 8
* Ruff
* MyPy
* Type-safe development
* Small reusable functions

Example:

```python
def validate_status_code(
    expected: int,
    actual: int,
) -> None: ...
```

Avoid:

* Large functions
* Deep nesting
* Global state
* Hidden side effects

---

# Type Hints

Every public API must include type hints.

Good:

```python
def load_config(path: str) -> AIConfig: ...
```

Avoid:

```python
def load_config(path): ...
```

The project targets strict MyPy compliance.

---

# Testing

Every feature should include tests.

Run:

```bash
pytest
```

Before submitting a pull request, also run:

```bash
ruff check .

mypy .

pytest
```

All checks should pass.

---

# Writing Tests

Tests should verify:

* Success cases
* Failure cases
* Edge cases
* Invalid input
* Exception paths

Prefer small focused tests over large integration tests.

---

# Documentation

Documentation is considered part of the codebase.

Whenever adding:

* a feature
* a public API
* a provider
* configuration options

update the documentation.

Documentation changes are required for user-facing features.

---

# Commit Messages

Use descriptive commit messages.

Examples:

```text
Add Gemini provider

Fix JSON schema validation

Improve AI prompt rendering

Refactor authentication module
```

Avoid:

```text
Update

Fix

Changes
```

---

# Pull Requests

A good pull request includes:

* Clear description
* Motivation
* Tests
* Documentation updates

Keep pull requests focused.

Avoid combining unrelated changes.

---

# Adding a New AI Provider

To add a provider:

1. Create a provider class.

2. Inherit from:

```python
BaseAIProvider
```

3. Implement:

```python
complete(...)
```

4. Add tests.

5. Update provider registry.

6. Update documentation.

7. Add examples.

---

# Provider Requirements

Every provider should:

* validate configuration
* construct requests
* parse responses
* handle HTTP errors
* raise framework exceptions
* support injected sessions for testing

Providers should not contain unrelated business logic.

---

# Error Handling

Raise framework-specific exceptions.

Example:

```python
raise AIProviderError("Unexpected response.")
```

Avoid raising generic exceptions directly.

---

# Backward Compatibility

Avoid breaking existing APIs.

If a breaking change is required:

* document it
* update migration notes
* update examples

---

# Dependencies

Before adding a dependency, consider:

* Is it necessary?
* Is it actively maintained?
* Is it lightweight?
* Does it duplicate existing functionality?

Prefer the standard library whenever practical.

---

# Performance

Contributors should consider:

* startup time
* memory usage
* network overhead
* unnecessary allocations

Avoid premature optimization, but keep implementations efficient.

---

# Security

Never commit:

* API keys
* passwords
* tokens
* credentials

Use environment variables for secrets.

Avoid logging sensitive information.

---

# Issue Reporting

When reporting issues, include:

* Python version
* Operating system
* PyRestKit version
* Reproduction steps
* Expected behavior
* Actual behavior
* Error messages

Minimal reproducible examples are highly appreciated.

---

# Feature Requests

Good feature requests explain:

* the problem
* the proposed solution
* possible alternatives
* expected API

This helps maintainers evaluate new ideas.

---

# Code Review

Reviews focus on:

* correctness
* readability
* maintainability
* testing
* documentation
* API consistency

Feedback is intended to improve the project.

---

# Release Process

A typical release includes:

1. Update version
2. Update changelog
3. Run tests
4. Build package
5. Publish to PyPI
6. Create GitHub release
7. Update documentation

---

# Community Guidelines

Please be:

* respectful
* constructive
* patient
* collaborative

Everyone starts somewhere, and thoughtful feedback helps build a stronger open-source community.

---

# Thank You

Thank you for helping improve PyRestKit.

Every contribution—whether code, documentation, tests, bug reports, or ideas—helps make the project better for everyone.
