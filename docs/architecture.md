# PyRestKit Architecture

## Overview

PyRestKit is designed as a modular, extensible, and type-safe REST API automation framework.

Rather than being a thin wrapper around an HTTP library, PyRestKit separates responsibilities into independent components that can evolve without affecting the rest of the framework.

The architecture follows several core engineering principles:

* Single Responsibility Principle (SRP)
* Composition over inheritance
* Provider abstraction
* Explicit configuration
* Strong typing
* Optional AI integration
* Testability

Every major feature is implemented as an isolated module with a clearly defined responsibility.

---

# High-Level Architecture

```
                      Test Code
                           │
                           ▼
                    API Client Layer
                           │
         ┌─────────────────┴─────────────────┐
         ▼                                   ▼
 Authentication                     Configuration
         │                                   │
         └─────────────────┬─────────────────┘
                           ▼
                    HTTP Transport
                           │
                           ▼
                     HTTP Response
                           │
        ┌──────────────────┴──────────────────┐
        ▼                                     ▼
 Validation Engine                  AI Failure Analysis
        │                                     │
        ▼                                     ▼
 Assertions                     AI Provider Abstraction
                                              │
                    ┌─────────────┬────────────┴─────────────┐
                    ▼             ▼                          ▼
                 OpenAI      Anthropic                 Gemini
                    ▼             ▼                          ▼
               Azure AI       Groq                    Ollama
                    ▼             ▼                          ▼
                 Cohere       Mistral                 Bedrock
```

The framework intentionally keeps these modules independent.

For example:

* Validation has no dependency on AI.
* Authentication has no dependency on configuration.
* AI has no dependency on validators.
* Providers have no dependency on the API client.

This separation minimizes coupling and improves maintainability.

---

# Package Organization

The project is organized by feature rather than by file type.

```
pyrestkit/

    auth/
    client/
    config/
    validators/
    logging/
    retry/
    exceptions/

    ai/
        analyzer.py
        config.py
        factory.py
        prompt_loader.py
        exceptions.py

        providers/

        prompts/
```

Each package owns a specific area of responsibility.

---

# Request Lifecycle

A typical API request passes through several stages.

```
User Test

    │

    ▼

API Client

    │

Authentication Applied

    │

Headers Prepared

    │

HTTP Request Sent

    │

Response Received

    │

Response Object Created

    │

Validation

    │

Assertions

    │

(Optional)

AI Failure Analysis
```

Every stage has a single responsibility.

---

# Core Components

## API Client

The API Client is the central entry point for executing HTTP requests.

Responsibilities include:

* Building requests
* Applying authentication
* Managing headers
* Handling query parameters
* Configuring timeout
* Executing HTTP requests
* Returning response objects

The client deliberately avoids business logic.

It should never:

* validate schemas
* analyze failures
* perform AI operations

Those responsibilities belong elsewhere.

---

## Response Object

The response object wraps the raw HTTP response.

It exposes convenience methods for:

* JSON parsing
* Status code validation
* Header validation
* Response time validation
* Schema validation
* Assertions

Keeping validation close to the response makes test code concise while keeping implementation modular.

---

# Validation Layer

Validation is completely independent from AI.

Its responsibilities include:

* HTTP status validation
* JSON validation
* Header validation
* Response time validation
* JSON schema validation
* Custom validators

Validators raise framework-specific exceptions instead of raw HTTP exceptions.

This produces clearer error messages and a consistent developer experience.

---

# Configuration System

PyRestKit supports multiple configuration sources.

Priority order:

```
Environment Variables

        ▲

YAML Configuration

        ▲

Python Objects

        ▲

Framework Defaults
```

Configuration objects are immutable where practical and validated immediately to fail fast on invalid settings.

---

# Authentication Layer

Authentication strategies are isolated from the client.

Supported approaches include:

* Bearer Token
* Basic Authentication
* API Key
* OAuth
* Custom implementations

New authentication mechanisms can be added without modifying the client itself.

---

# AI Architecture

The AI subsystem is intentionally isolated from the rest of the framework.

```
Validation Failure

        │

        ▼

AI Analyzer

        │

Prompt Loader

        │

Prompt Rendering

        │

Provider Factory

        │

Selected Provider

        │

LLM Response

        │

Formatted Analysis
```

This design ensures that AI remains optional.

If AI is not configured, the rest of PyRestKit continues to function normally.

---

# Provider Abstraction

One of the key architectural decisions is the provider abstraction layer.

Every provider implements the same interface.

```
BaseAIProvider

        ▲

        │

OpenAIProvider

AnthropicProvider

GeminiProvider

GroqProvider

AzureOpenAIProvider

OllamaProvider

MistralProvider

CohereProvider

BedrockProvider
```

Because every provider exposes the same interface, the analyzer never needs provider-specific logic.

This dramatically reduces complexity.

---

# Factory Pattern

The Provider Factory selects the appropriate provider at runtime.

```
provider="openai"

        │

        ▼

ProviderFactory

        │

        ▼

OpenAIProvider
```

Changing providers requires only a configuration change.

No application code changes are necessary.

---

# Prompt System

Prompt templates are stored separately from Python code.

Benefits include:

* easier maintenance
* prompt versioning
* customization
* localization
* testing

The analyzer loads templates, injects runtime context, and forwards the rendered prompt to the selected provider.

---

# Error Handling

The framework defines domain-specific exceptions instead of exposing low-level implementation details.

Examples include:

* Configuration errors
* Validation failures
* Authentication failures
* Provider errors
* AI analysis failures

This makes failures easier to understand and simplifies debugging.

---

# Type Safety

PyRestKit is designed with static analysis in mind.

The project uses:

* type hints
* mypy
* Ruff
* dataclasses
* immutable configuration where appropriate

This helps catch issues during development rather than at runtime.

---

# Testing Strategy

The project emphasizes isolated unit testing.

Components are tested independently.

Examples include:

* configuration loading
* provider behavior
* validation logic
* prompt rendering
* factory selection
* error handling

External AI services are mocked during tests to ensure repeatability and avoid network dependencies.

---

# Extensibility

The framework is designed to grow without requiring modifications to existing components.

Examples include:

* adding a new AI provider
* adding a validator
* adding an authentication strategy
* extending configuration
* introducing new prompt templates

Most extensions require creating a new implementation rather than modifying existing code.

This reduces regression risk and keeps the codebase maintainable.

---

# Design Principles

PyRestKit follows several guiding principles.

## Explicit over implicit

Configuration should be clear and predictable.

## Composition over inheritance

Components collaborate instead of relying on deep inheritance hierarchies.

## AI is optional

Core API automation should never depend on external AI services.

## Strong typing

Static analysis improves correctness and maintainability.

## Small focused modules

Each package should own one responsibility.

## Backward compatibility

New features should minimize breaking changes whenever possible.

---

# Future Evolution

The current architecture is designed to support future enhancements such as:

* asynchronous HTTP client
* plugin architecture
* HTML reporting
* AI-generated test cases
* OpenAPI integration
* custom provider plugins
* CLI tooling
* IDE integrations

These capabilities can be added without fundamentally changing the current architecture because of the existing separation of concerns.

---

# Summary

PyRestKit is organized around modular components with clearly defined responsibilities.

The API client, validation engine, configuration system, authentication layer, and AI subsystem operate independently while collaborating through well-defined interfaces.

This architecture keeps the framework maintainable, extensible, and suitable for both small automation projects and larger enterprise codebases.
