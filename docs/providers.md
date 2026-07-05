# AI Provider Guide

## Overview

PyRestKit supports multiple Large Language Model (LLM) providers through a unified provider abstraction.

Regardless of which provider is used, the rest of the framework interacts with the same interface.

This allows applications to switch providers without modifying business logic.

---

# Design Goals

The provider architecture is designed around the following principles:

* Provider independence
* Consistent public interface
* Minimal provider-specific logic outside provider classes
* Easy testing
* Easy extensibility
* Fail-fast configuration validation

---

# Architecture

```text
                    AI Analyzer
                         │
                         ▼
                 Provider Factory
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
     OpenAI         Anthropic         Gemini
        ▼                ▼                ▼
   Azure OpenAI       Groq           Cohere
        ▼                ▼                ▼
     Mistral         Ollama         Bedrock
```

The analyzer never knows which provider is currently being used.

Only the Provider Factory performs provider selection.

---

# BaseAIProvider

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

This interface represents the contract between the analyzer and every provider.

---

# Provider Lifecycle

Every provider follows the same high-level workflow.

```text
Validate Configuration

↓

Build Request Payload

↓

Prepare Headers

↓

Send HTTP Request

↓

Check HTTP Status

↓

Parse JSON

↓

Extract Generated Text

↓

Return Analysis
```

Although each provider communicates with a different external API, the internal flow remains consistent.

---

# Provider Factory

The Provider Factory is responsible for converting a provider name into its implementation.

Example:

```python
provider = factory.create(config.provider)
```

The factory hides implementation details from the analyzer.

Adding new providers requires updating the factory registration only once.

---

# Built-in Providers

## OpenAI

Authentication:

* API Key

Endpoint:

```text
POST /v1/responses
```

Typical configuration:

```python
AIConfig(
    provider="openai",
    model="gpt-4.1-mini",
    api_key="...",
)
```

Supports:

* instructions
* temperature
* max output tokens
* organization header

---

## Anthropic

Authentication:

* API Key

Endpoint:

```text
POST /v1/messages
```

Supports:

* system prompt
* max tokens
* messages API

---

## Google Gemini

Authentication:

* API Key

Endpoint:

```text
POST /models/{model}:generateContent
```

Supports:

* contents
* system instruction
* parts API

---

## Azure OpenAI

Authentication:

* API Key

Endpoint:

Azure deployment endpoint.

Supports:

* deployment-specific URLs
* Azure API version
* Azure authentication headers

---

## Groq

Authentication:

* API Key

API compatibility:

OpenAI Chat Completions compatible.

Suitable when migrating existing OpenAI integrations.

---

## Cohere

Authentication:

* API Key

Supports:

* chat endpoint
* conversation-based generation

---

## Mistral

Authentication:

* API Key

Uses the Chat Completions API.

Behavior is intentionally similar to OpenAI-compatible providers.

---

## Ollama

Authentication:

None (local deployment)

Typical endpoint:

```text
http://localhost:11434
```

Advantages:

* Local execution
* No API cost
* Private models
* Offline development

---

## AWS Bedrock

Authentication:

AWS credentials.

Typical environments:

* IAM Roles
* AWS CLI
* Environment Variables

Bedrock acts as an abstraction over multiple foundation models.

---

# Configuration

All providers receive the same configuration object.

```python
config = AIConfig(
    provider="openai",
    model="gpt-4.1-mini",
    api_key="...",
)
```

Each provider uses only the configuration fields relevant to it.

Unused values are ignored.

---

# Shared Configuration

Common configuration options include:

* provider
* model
* api_key
* base_url
* timeout
* temperature
* max_tokens
* organization
* custom headers

This shared configuration simplifies switching providers.

---

# Request Payload Translation

The analyzer produces a single prompt.

Each provider converts that prompt into the format required by its API.

Example:

Analyzer output:

```text
Analyze why this API request failed.
```

OpenAI:

```json
{
  "input": "...",
  "model": "..."
}
```

Gemini:

```json
{
  "contents": [
    {
      "parts": [
        {
          "text": "..."
        }
      ]
    }
  ]
}
```

Anthropic:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "..."
    }
  ]
}
```

This translation layer is isolated inside provider implementations.

---

# Response Parsing

Every provider returns a different JSON structure.

Each implementation extracts the generated text and converts it into the common return type.

Regardless of provider:

```python
result = provider.complete(...)
```

always returns

```python
str
```

This hides provider-specific JSON structures from the analyzer.

---

# Error Handling

Providers raise framework-specific exceptions.

Typical failure categories include:

* Missing API key
* Invalid configuration
* HTTP failure
* Invalid JSON
* Missing generated text

Errors are normalized into AI-specific exceptions instead of exposing raw HTTP implementation details.

---

# HTTP Client

Provider implementations communicate using an injectable HTTP session.

Benefits include:

* Unit testing
* Dependency injection
* Mocking
* Reduced coupling

During tests, fake sessions replace real HTTP clients.

---

# Creating a Custom Provider

A custom provider requires only a few steps.

## Step 1

Create a new provider.

```python
class InternalProvider(BaseAIProvider): ...
```

---

## Step 2

Implement `complete()`.

Responsibilities:

* Validate configuration
* Build request
* Send request
* Parse response
* Return generated text

---

## Step 3

Register the provider.

Example:

```python
factory.register(
    "internal",
    InternalProvider,
)
```

---

## Step 4

Configure it.

```python
AIConfig(
    provider="internal",
    model="company-model",
)
```

No other framework changes are required.

---

# Testing Providers

Recommended test coverage includes:

* Missing configuration
* Invalid configuration
* HTTP failures
* Invalid JSON
* Invalid response structure
* Successful completion
* Timeout behavior
* Header generation

Provider tests should never call external APIs.

Instead, use mocked sessions and fake responses.

---

# Best Practices

When implementing providers:

* Keep providers focused on HTTP communication only.
* Do not generate prompts.
* Do not analyze failures.
* Validate configuration before making requests.
* Normalize provider-specific errors.
* Return plain text only.

Keeping providers small makes them easier to maintain and test.

---

# Why Provider Abstraction?

Without abstraction, every analyzer would contain provider-specific branching logic.

Example:

```text
if provider == OpenAI
...

elif provider == Gemini
...

elif provider == Anthropic
...
```

As more providers are added, this quickly becomes difficult to maintain.

Instead, PyRestKit isolates provider-specific behavior inside dedicated implementations while the analyzer depends only on a single interface.

This significantly reduces complexity and makes adding new providers straightforward.

---

# Summary

The provider abstraction is one of the key architectural decisions in PyRestKit.

It enables support for multiple AI providers through a consistent interface while keeping the analyzer independent of provider-specific APIs.

This approach improves maintainability, simplifies testing, and allows new providers to be introduced with minimal changes to the rest of the framework.
