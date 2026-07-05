# Configuration Guide

## Overview

Configuration is a fundamental part of every automation framework.

PyRestKit provides a flexible configuration system that supports multiple configuration sources while keeping application code clean and environment independent.

The framework is designed so that configuration can easily change between local development, testing, staging, and production without modifying test code.

---

# Design Goals

The configuration system is built around several principles:

* Simplicity
* Explicit configuration
* Environment independence
* Type safety
* Early validation
* Predictable behavior

Configuration errors are detected as early as possible to prevent unexpected runtime failures.

---

# Configuration Sources

PyRestKit supports multiple configuration sources.

Typical sources include:

* Python objects
* YAML files
* Environment variables

These sources can be combined depending on project requirements.

---

# Python Configuration

The simplest approach is to create configuration directly in code.

Example:

```python
from pyrestkit.ai import AIConfig

config = AIConfig(
    provider="openai",
    model="gpt-4.1-mini",
    api_key="YOUR_API_KEY",
)
```

This approach is useful for:

* examples
* quick experiments
* unit tests
* small projects

---

# YAML Configuration

For larger projects, configuration is commonly stored in YAML files.

Example:

```yaml
base_url: https://api.example.com

timeout: 30

headers:
  Accept: application/json

ai:
  provider: openai
  model: gpt-4.1-mini
  api_key: YOUR_API_KEY
  temperature: 0.2
```

Loading configuration from YAML keeps sensitive values and environment-specific settings outside application code.

---

# Environment Variables

Environment variables are recommended for secrets and deployment-specific configuration.

Example:

```text
PYRESTKIT_AI_PROVIDER=openai
PYRESTKIT_AI_MODEL=gpt-4.1-mini
PYRESTKIT_AI_API_KEY=YOUR_API_KEY
PYRESTKIT_AI_TIMEOUT=60
PYRESTKIT_AI_TEMPERATURE=0.2
```

Configuration can then be created using:

```python
config = AIConfig.from_env()
```

This approach works well with:

* Docker
* GitHub Actions
* Jenkins
* Azure DevOps
* GitLab CI
* Kubernetes

---

# AIConfig

The `AIConfig` class provides a provider-independent configuration model for the AI subsystem.

Typical fields include:

| Field        | Description                               |
| ------------ | ----------------------------------------- |
| provider     | AI provider name                          |
| model        | Model identifier                          |
| api_key      | Provider API key                          |
| base_url     | Custom endpoint                           |
| timeout      | Request timeout                           |
| temperature  | Model temperature                         |
| max_tokens   | Maximum generated tokens                  |
| organization | Provider-specific organization identifier |
| headers      | Additional HTTP headers                   |

The same configuration object is used by every provider.

---

# Configuration Validation

Configuration is validated during object creation.

Examples of validation include:

* Provider cannot be empty.
* Model cannot be empty.
* Temperature must be within the supported range.
* Timeout must be greater than zero.
* Maximum tokens must be positive.
* Headers must be a mapping.

Detecting invalid values early improves developer experience and avoids unnecessary network requests.

---

# Loading from a Mapping

Configuration can also be created from a mapping.

Example:

```python
mapping = {
    "provider": "openai",
    "model": "gpt-4.1-mini",
    "temperature": 0.2,
}

config = AIConfig.from_mapping(mapping)
```

Nested mappings are also supported.

Example:

```python
mapping = {
    "ai": {
        "provider": "gemini",
        "model": "gemini-2.5-pro",
    }
}
```

---

# Default Values

Several configuration options provide sensible defaults.

Examples:

| Option      | Default       |
| ----------- | ------------- |
| temperature | 0.2           |
| timeout     | 60 seconds    |
| headers     | Empty mapping |

Using defaults keeps configuration concise while remaining explicit where necessary.

---

# Provider-Specific Settings

Although every provider shares the same configuration model, some settings are only used by specific providers.

Examples include:

* `organization` for OpenAI
* `base_url` for Azure OpenAI deployments
* Local URLs for Ollama
* AWS-specific endpoints for Bedrock

Unused configuration values are ignored by providers that do not require them.

---

# Custom Headers

Additional HTTP headers can be provided through the `headers` field.

Example:

```python
config = AIConfig(
    provider="openai",
    model="gpt-4.1-mini",
    api_key="YOUR_API_KEY",
    headers={
        "X-Correlation-ID": "12345",
    },
)
```

These headers are merged with provider-required headers before the request is sent.

---

# Secrets Management

API keys and other secrets should never be committed to source control.

Recommended approaches include:

* Environment variables
* Secret management services
* CI/CD secret stores
* Cloud key vaults

Avoid embedding secrets directly in Python source files.

---

# Environment-Specific Configuration

A common project structure might include:

```text
config/
├── development.yaml
├── qa.yaml
├── staging.yaml
└── production.yaml
```

Each environment can define its own:

* Base URLs
* Credentials
* Timeouts
* Headers
* AI settings

This allows the same test suite to run across multiple environments without modification.

---

# Configuration Precedence

When multiple configuration sources are used, projects should define a clear precedence strategy.

A common approach is:

```text
Environment Variables
        │
        ▼
YAML Configuration
        │
        ▼
Default Values
```

Environment variables typically take precedence because they are easiest to override in deployment pipelines.

---

# Error Handling

Configuration errors raise dedicated exceptions or validation errors before any HTTP request is attempted.

Typical causes include:

* Missing required values
* Invalid numeric ranges
* Incorrect data types
* Invalid header structures

Early validation reduces debugging time and prevents invalid requests from reaching external services.

---

# Best Practices

To keep configuration maintainable:

* Keep secrets outside source control.
* Use environment variables for credentials.
* Use YAML for environment-specific settings.
* Keep default values conservative.
* Validate configuration during application startup.
* Share configuration objects where practical rather than recreating them repeatedly.

---

# Future Enhancements

The configuration system is designed to support future capabilities such as:

* Multiple named AI profiles
* Provider failover configuration
* Configuration inheritance
* Dynamic configuration reloading
* Encrypted configuration files
* Plugin-based configuration sources

These enhancements can be added without changing the existing configuration model.

---

# Summary

PyRestKit provides a flexible, strongly typed configuration system that supports Python objects, mappings, YAML files, and environment variables.

By validating configuration early and using a provider-independent model, the framework keeps applications predictable, secure, and easy to maintain across different environments.
