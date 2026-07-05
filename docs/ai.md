# AI-Assisted Failure Analysis

## Overview

PyRestKit provides an optional AI-assisted failure analysis module that helps developers understand API failures faster by generating natural-language explanations and actionable suggestions.

Unlike traditional assertion failures, which typically report only what failed, the AI subsystem focuses on explaining **why** the failure likely occurred and, where possible, suggests how to resolve it.

The AI module is completely optional. If it is not configured, PyRestKit functions as a standard REST API automation framework without any dependency on external AI services.

---

# Goals

The AI subsystem was designed with the following goals:

* Keep AI completely optional.
* Support multiple LLM providers through a unified interface.
* Make providers interchangeable through configuration.
* Separate prompt management from application code.
* Keep prompts reusable and customizable.
* Make provider implementations independently testable.
* Enable future AI capabilities without affecting the core framework.

---

# High-Level Architecture

```text
                   Validation Failure
                           │
                           ▼
                    AIFailureAnalyzer
                           │
                           ▼
                     Prompt Loader
                           │
                           ▼
                   Rendered Prompt
                           │
                           ▼
                    Provider Factory
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
       OpenAI         Anthropic         Gemini
          ▼                ▼                ▼
        Groq          Azure OpenAI      Cohere
          ▼                ▼                ▼
      Mistral         Ollama           Bedrock
                           │
                           ▼
                   AI Generated Analysis
```

Each component has a single responsibility and can evolve independently.

---

# Components

## AIConfig

`AIConfig` stores provider-specific configuration while presenting a provider-agnostic interface to the rest of the framework.

Typical configuration includes:

* Provider name
* Model name
* API key
* Base URL
* Temperature
* Maximum output tokens
* Timeout
* Organization (where supported)
* Custom HTTP headers

Configuration values can be created directly, loaded from mappings, or read from environment variables.

Example:

```python
from pyrestkit.ai import AIConfig

config = AIConfig(
    provider="openai",
    model="gpt-4.1-mini",
    api_key="YOUR_API_KEY",
    temperature=0.2,
)
```

---

## AIFailureAnalyzer

The analyzer is the public entry point into the AI subsystem.

Responsibilities include:

* collecting failure context
* loading prompts
* rendering templates
* selecting the provider
* requesting analysis
* returning the final explanation

The analyzer intentionally knows nothing about provider-specific HTTP APIs.

---

## Prompt Loader

Prompt templates are stored separately from Python code.

This separation provides several benefits:

* prompts can evolve without code changes
* easier experimentation
* improved readability
* better testing
* easier localization
* organization-specific customization

Typical prompt flow:

```text
Template

↓

Runtime Variables

↓

Rendered Prompt

↓

Provider
```

---

## Prompt Templates

Prompt templates define how information is presented to the LLM.

Rather than constructing prompts with string concatenation inside Python code, PyRestKit keeps prompts in dedicated template files.

Typical prompt information includes:

* HTTP method
* Request URL
* Request headers
* Request body
* Response status
* Response headers
* Response body
* Validation failure
* Expected behavior

The rendered prompt becomes the input for the selected provider.

---

# Provider Factory

The Provider Factory converts a provider name into the corresponding implementation.

Example:

```text
provider = "gemini"

↓

ProviderFactory

↓

GeminiProvider
```

The analyzer never contains provider-specific branching logic.

---

# Provider Interface

Every provider implements the same interface.

```python
class BaseAIProvider:
    def complete(
        self,
        prompt: str,
        *,
        config: AIConfig,
        system_prompt: str | None = None,
    ) -> str: ...
```

This abstraction allows new providers to be added without changing existing application code.

---

# Supported Providers

PyRestKit currently supports the following providers:

| Provider     | Authentication     |
| ------------ | ------------------ |
| OpenAI       | API Key            |
| Anthropic    | API Key            |
| Gemini       | API Key            |
| Azure OpenAI | API Key            |
| Groq         | API Key            |
| Cohere       | API Key            |
| Mistral      | API Key            |
| Ollama       | Local / No API Key |
| AWS Bedrock  | AWS Credentials    |

Each provider converts the common interface into its native HTTP API.

---

# Provider Responsibilities

A provider implementation is responsible for:

* validating configuration
* constructing the request payload
* sending the HTTP request
* validating the HTTP response
* parsing provider-specific JSON
* extracting the generated text
* raising meaningful provider errors

The provider should not:

* load prompts
* build prompt templates
* analyze failures
* validate API responses

Those concerns belong elsewhere.

---

# AI Request Flow

```text
User Test

↓

Validation Failure

↓

AIFailureAnalyzer

↓

Prompt Loader

↓

Rendered Prompt

↓

Selected Provider

↓

LLM API

↓

Provider Response

↓

Extract Text

↓

Analysis Returned
```

---

# Configuration Sources

Configuration can be provided through several mechanisms.

## Python

```python
config = AIConfig(
    provider="openai",
    model="gpt-4.1-mini",
)
```

---

## Environment Variables

Example:

```text
PYRESTKIT_AI_PROVIDER=openai
PYRESTKIT_AI_MODEL=gpt-4.1-mini
PYRESTKIT_AI_API_KEY=...
```

Then:

```python
config = AIConfig.from_env()
```

---

## Mapping

```python
config = AIConfig.from_mapping(mapping)
```

This is useful for configuration files or application settings.

---

# Error Handling

The AI subsystem defines dedicated exceptions.

Examples include:

* AIConfigurationError
* AIProviderError

Configuration issues are detected before any HTTP request is made.

Provider errors wrap remote service failures in framework-specific exceptions.

---

# Why AI Is Optional

AI can be valuable for diagnosing failures, but not every project requires it.

Keeping AI optional provides several advantages:

* deterministic execution
* offline capability
* reduced dependencies
* no additional runtime cost
* easier CI integration
* enterprise compliance

Users who do not configure AI experience no behavior changes in the rest of the framework.

---

# Testing Strategy

Provider implementations are tested independently.

Tests cover:

* configuration validation
* payload generation
* HTTP error handling
* JSON parsing
* response extraction
* invalid responses
* missing configuration

External APIs are replaced with mocked HTTP sessions to ensure reliable and repeatable test execution.

---

# Extending PyRestKit

Adding a new provider requires implementing the common provider interface.

Typical steps:

1. Create a provider class.
2. Implement `complete()`.
3. Validate configuration.
4. Send the provider-specific request.
5. Parse the response.
6. Register the provider with the factory.
7. Add unit tests.

Because the analyzer communicates only with the base interface, no analyzer changes are required.

---

# Future Enhancements

The current architecture provides a strong foundation for future AI capabilities.

Potential additions include:

* AI-generated test cases
* OpenAPI-driven prompt generation
* Assertion suggestions
* Automatic root cause classification
* Failure severity estimation
* Retry recommendations
* Documentation linking
* Historical failure analysis
* Team-specific prompt libraries
* Prompt versioning

These enhancements can be introduced while preserving the current provider abstraction.

---

# Best Practices

When using AI-assisted failure analysis:

* Enable AI primarily for failed tests rather than every request.
* Keep prompt templates focused and concise.
* Store API keys securely using environment variables or secret managers.
* Use deterministic temperature settings for consistent results.
* Validate AI suggestions before applying them to production code.

---

# Summary

The AI subsystem extends PyRestKit with intelligent failure explanations while remaining completely independent from the core API automation framework.

By separating prompt management, provider implementations, configuration, and analysis into dedicated components, PyRestKit achieves a modular architecture that is easy to extend, test, and maintain.

This design enables support for multiple LLM providers today while providing a flexible foundation for future AI-powered capabilities.
