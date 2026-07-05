# 🚀 PyRestKit

> A modern Python framework for REST API automation with built-in validation,
> authentication, configuration management, and optional AI-assisted failure analysis.

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![PyPI](https://img.shields.io/pypi/v/pyrestkit.svg)](https://pypi.org/project/pyrestkit/)
[![License](https://img.shields.io/github/license/Raushanraj77/pyrestkit)](LICENSE)
[![Tests](https://github.com/Raushanraj77/pyrestkit/actions/workflows/tests.yml/badge.svg)](https://github.com/Raushanraj77/pyrestkit/actions)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-black)](https://docs.astral.sh/ruff/)
[![Type Checked](https://img.shields.io/badge/type%20checked-mypy-blue)](https://mypy-lang.org/)

---

## Why PyRestKit?

Testing REST APIs often requires combining multiple libraries for:

- HTTP requests
- Authentication
- Configuration management
- Assertions
- JSON validation
- Logging
- Retry handling
- Environment management

As projects grow, these utilities become difficult to maintain consistently across teams.

PyRestKit provides a unified, extensible framework that brings these capabilities together while keeping your test code clean, maintainable, and type-safe.

In addition, PyRestKit offers **optional AI-assisted failure analysis**, enabling engineers to receive intelligent explanations and debugging suggestions from multiple Large Language Model (LLM) providers.

---

# Features

## REST API Client

- Simple request API
- GET / POST / PUT / PATCH / DELETE
- Custom headers
- Query parameters
- Cookies
- Multipart requests
- Request timeout support

---

## Authentication

Built-in authentication helpers:

- Basic Authentication
- Bearer Token
- API Key
- OAuth 2.0 (yet to implement)
- Custom authentication strategies

---

## Validation

Powerful response validation utilities.

Supported validations include:

- Status Code
- Headers
- JSON Schema
- Response Time
- JSON Path
- Custom Validators

---

## Configuration

Configuration can be loaded from

- YAML
- Environment Variables
- Python Objects

Supports multiple environments including

- Development
- QA
- Staging
- Production

---

## Assertions

Readable assertions for

- Status codes
- Headers
- JSON values
- Collections
- Response time
- Custom assertions

---

## AI-Assisted Failure Analysis

PyRestKit can analyze failed API responses using AI.

Features include

- Root cause explanation
- Human-readable summaries
- Suggested fixes
- Optional system prompts
- Prompt templates
- Provider abstraction

AI support is completely optional and does not affect users who prefer traditional API testing.

---

## Multiple AI Providers

PyRestKit currently supports:

| Provider | Supported |
|-----------|-----------|
| OpenAI | ✅ |
| Anthropic | ✅ |
| Google Gemini | ✅ |
| Azure OpenAI | ✅ |
| Groq | ✅ |
| Cohere | ✅ |
| Mistral | ✅ |
| Ollama | ✅ |
| AWS Bedrock | ✅ |

The provider abstraction allows additional providers to be implemented with minimal effort.

---

# Installation

## Standard Installation

```bash
pip install pyrestkit
```

---

## Development Installation

```bash
git clone https://github.com/Raushanraj77/pyrestkit.git

cd pyrestkit

python -m venv .venv

source .venv/bin/activate

pip install -e .
```

---

## Verify Installation

```python
import pyrestkit

print(pyrestkit.__version__)
```

---

# Quick Start

## Create a Client

```python
from pyrestkit import APIClient

client = APIClient(base_url="https://jsonplaceholder.typicode.com")
```

---

## Send a Request

```python
response = client.get("/posts/1")
```

---

## Validate Response

```python
response.validate_status_code(200)

response.validate_json()

response.validate_response_time(max_time_ms=1000)
```

---

## Read JSON

```python
data = response.json()

print(data["title"])
```

---

# Authentication Example

## Bearer Token

```python
client = APIClient(base_url="https://example.com")

client.authenticate_bearer(token="your-token")
```

---

## Basic Authentication

```python
client.authenticate_basic(username="admin", password="secret")
```

---

## API Key

```python
client.authenticate_api_key(key="xxxxxxxx", header_name="X-API-Key")
```

---

# Configuration Example

Load configuration from YAML.

```yaml
base_url: https://api.example.com

timeout: 30

headers:
  Accept: application/json
```

```python
from pyrestkit.config import Config

config = Config.from_yaml("config.yaml")
```

---

# Response Validation

```python
response.validate_status_code(200)

response.validate_header("Content-Type", "application/json")

response.validate_schema("schemas/user.json")
```

---

# AI Failure Analysis

AI analysis can be enabled whenever deeper insight into a failed response is useful.

```python
from pyrestkit.ai import AIAnalyzer
from pyrestkit.ai import AIConfig

config = AIConfig(provider="openai", model="gpt-4.1-mini", api_key="YOUR_API_KEY")

analyzer = AIAnalyzer(config)

analysis = analyzer.analyze(
    request=request,
    response=response,
)

print(analysis)
```
---

# Supported AI Providers

PyRestKit uses a provider abstraction layer that allows switching AI providers
without changing your test code.

```text
                    AI Analyzer
                         │
                         ▼
                 Provider Factory
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
     OpenAI         Anthropic        Gemini
        │                │                │
        ▼                ▼                ▼
      Groq           Cohere         Azure OpenAI
        │
        ▼
     Mistral
        │
        ▼
     Ollama
        │
        ▼
    AWS Bedrock
```

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

This makes it easy to:

- switch providers
- test providers
- implement custom providers
- support enterprise LLMs

---

# Project Structure

```text
pyrestkit/
│
├── pyrestkit/
│   │
│   ├── auth/
│   ├── client/
│   ├── config/
│   ├── exceptions/
│   ├── logging/
│   ├── retry/
│   ├── validators/
│   │
│   ├── ai/
│   │   ├── analyzer.py
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   ├── factory.py
│   │   ├── prompt_loader.py
│   │   ├── prompts/
│   │   └── providers/
│   │
│   └── ...
│
├── docs/
├── examples/
├── tests/
├── pyproject.toml
└── README.md
```

---

# Framework Architecture

```text
                 Test

                  │

                  ▼

            API Client

                  │

                  ▼

        Authentication Layer

                  │

                  ▼

           HTTP Transport

                  │

                  ▼

            API Response

                  │

       ┌──────────┴──────────┐

       ▼                     ▼

 Validation             AI Analysis

       │                     │

       ▼                     ▼

 Assertions          Root Cause Analysis
```

---

# Why AI Is Optional

PyRestKit is designed as an API automation framework first.

AI is an optional capability.

This provides several advantages:

- no AI dependency for normal users
- predictable execution
- no external API calls unless enabled
- works in offline environments
- enterprise friendly
- easier testing

If AI is never configured, PyRestKit behaves exactly like a traditional API
automation framework.

---

# Extending PyRestKit

Creating a custom AI provider requires implementing a single interface.

```python
from pyrestkit.ai.providers.base import BaseAIProvider


class InternalProvider(BaseAIProvider):
    def complete(
        self,
        prompt: str,
        *,
        config,
        system_prompt=None,
    ) -> str:

        ...

        return result
```

Register the provider.

```python
factory.register(
    "internal",
    InternalProvider,
)
```

Now it can be used exactly like built-in providers.

---

# Example Workflow

```python
response = client.post(
    "/users",
    json=payload,
)

response.validate_status_code(201)

response.validate_schema("schemas/user.json")
```

If validation fails:

```python
analysis = analyzer.analyze(
    request=request,
    response=response,
)

print(analysis)
```

Example output:

```text
Status Code Mismatch

Expected:
201

Received:
400

Likely Cause

The "email" field is required but missing
from the request payload.

Suggested Fix

Include a valid email address before
submitting the request.
```

---

# Documentation

Detailed documentation is available in the `docs` directory.

| Document | Description |
|----------|-------------|
| getting-started.md | Installation and first project |
| architecture.md | Internal framework architecture |
| configuration.md | Configuration system |
| authentication.md | Authentication mechanisms |
| validation.md | Validators and assertions |
| ai.md | AI-assisted failure analysis |
| providers.md | AI provider implementations |
| examples.md | Complete usage examples |
| faq.md | Frequently asked questions |
| roadmap.md | Future development plans |

---

# Running Tests

Run all tests.

```bash
pytest
```

Run with coverage.

```bash
pytest --cov=pyrestkit
```

Run Ruff.

```bash
ruff check .
```

Run MyPy.

```bash
mypy .
```

Build package.

```bash
python -m build
```

---

# Contributing

Contributions are welcome.

Please read:

- CONTRIBUTING.md
- CODE_OF_CONDUCT.md

before submitting pull requests.

---

# Roadmap

## Version 1.x

- REST API Client
- Authentication
- Validation
- Assertions
- Retry
- Configuration
- Logging
- AI Failure Analysis
- Multiple AI Providers

## Version 2.x

Planned improvements include:

- Async HTTP Client
- HTML Reporting
- OpenAPI Integration
- AI Test Generation
- AI Assertion Suggestions
- Plugin System
- CLI
- VS Code Extension

---

# Why PyRestKit?

PyRestKit aims to provide a clean, extensible, and modern approach to REST API automation.

Core principles:

- Simplicity
- Type Safety
- Extensibility
- Clean Architecture
- Optional AI
- Developer Experience

---

# Requirements

- Python 3.10+
- requests
- pydantic
- jsonschema
- PyYAML

Optional:

- OpenAI
- Anthropic
- Gemini
- Azure OpenAI
- Groq
- Cohere
- Mistral
- Ollama
- AWS Bedrock

---

# License

PyRestKit is licensed under the MIT License.

See the LICENSE file for details.

---

# Support

If you encounter an issue:

- Open a GitHub Issue
- Start a GitHub Discussion
- Submit a Pull Request

---

# Acknowledgements

PyRestKit is inspired by the design philosophies of several outstanding open-source projects, including:

- Requests
- HTTPX
- FastAPI
- Pydantic
- Playwright

while focusing specifically on delivering a modern, extensible framework for REST API automation.

---

## Star the Project ⭐

If PyRestKit helps your team build reliable API automation, consider starring the repository to support the project and stay updated with future releases.