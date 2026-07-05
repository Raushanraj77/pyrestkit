# Changelog

All notable changes to **PyRestKit** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/) and this project follows [Semantic Versioning](https://semver.org/).

---

# [Unreleased]

## Added

* Placeholder for upcoming features.

## Changed

* Placeholder for improvements.

## Fixed

* Placeholder for bug fixes.

---

# [1.2.0] - 2026-07-05

## 🚀 Highlights

PyRestKit 1.2.0 introduces **AI-powered API failure analysis**, enabling developers to receive intelligent explanations for failed API validations using multiple Large Language Model (LLM) providers.

This release adds a provider-independent AI layer while maintaining full backward compatibility with existing PyRestKit users.

---

## Added

### AI-Assisted Failure Analysis

* Added AI-powered failure analysis.
* Added provider-independent AI architecture.
* Added reusable AI analysis pipeline.
* Added prompt templating system.
* Added prompt loader with secure template rendering.
* Added AI configuration model.
* Added environment variable support for AI configuration.
* Added YAML-based AI configuration.
* Added configurable AI provider registry.

### Supported AI Providers

Added built-in support for:

* OpenAI
* Azure OpenAI
* Anthropic Claude
* Google Gemini
* Groq
* Mistral AI
* Cohere
* Ollama
* Amazon Bedrock

### AI Configuration

Added support for:

* Provider selection
* Model selection
* API keys
* Base URLs
* Organization identifiers
* Custom HTTP headers
* Temperature
* Maximum output tokens
* Request timeout
* Environment variable loading
* Mapping/YAML configuration loading

### AI Infrastructure

Added:

* `AIConfig`
* `BaseAIProvider`
* Provider abstraction layer
* Prompt loader
* Prompt templates
* Failure analyzer
* AI-specific exceptions
* Provider registry

### Testing

Added comprehensive unit tests covering:

* AI configuration
* Prompt loading
* Provider implementations
* Provider error handling
* HTTP failures
* Invalid responses
* Environment configuration
* Mapping configuration
* AI integration

### Documentation

Added:

* AI Guide
* AI Provider Guide
* Configuration Guide
* Examples
* Architecture documentation
* Authentication Guide
* Validation Guide
* Contributor Guide

---

## Changed

### Architecture

* Introduced modular AI provider architecture.
* Standardized provider interfaces.
* Unified provider response parsing.
* Improved internal extensibility.

### Developer Experience

* Improved error messages.
* Improved configuration validation.
* Improved type safety.
* Better provider customization.
* Cleaner AI integration API.

---

## Fixed

* Configuration validation edge cases.
* Optional header handling.
* Provider response parsing inconsistencies.
* MyPy typing issues.
* Ruff lint violations.
* Prompt rendering validation.
* JSON parsing edge cases.
* Session injection for testing.
* Provider-specific validation issues.

---

# [1.1.0] - 2026-07-04

## 🚀 Highlights

PyRestKit 1.1.0 focused on improving the core API automation experience through enhanced validation, configuration, documentation, and overall framework stability.

---

## Added

### Core HTTP Client

* Improved HTTP request handling.
* Enhanced request configuration.
* Better response object usability.

### Authentication

Support for:

* Bearer Token Authentication
* Basic Authentication
* API Key Authentication

### Validation

Added and improved:

* Status code validation
* Response header validation
* JSON validation
* JSON Schema validation
* Response time validation

### Configuration

Added support for:

* YAML configuration
* Environment variables
* Default request headers
* Configurable timeouts

### Documentation

Added comprehensive project documentation including:

* Installation Guide
* Quick Start Guide
* Authentication Guide
* Validation Guide
* Examples
* Architecture documentation

---

## Changed

* Improved validation API.
* Improved exception messages.
* Improved project structure.
* Improved documentation quality.
* Refactored internal validation modules.
* Better developer experience.

---

## Fixed

* Validation edge cases.
* Response parsing improvements.
* Minor documentation corrections.
* Internal refactoring and stability improvements.

---

# [1.0.0] - Initial Release

## 🎉 Initial Public Release

### Added

Core framework functionality including:

### HTTP Methods

* GET
* POST
* PUT
* PATCH
* DELETE

### Authentication

* Bearer Authentication
* Basic Authentication
* API Key Authentication

### Validation

* Status Code Validation
* Header Validation
* JSON Validation
* JSON Schema Validation
* Response Time Validation

### Configuration

* Environment Variable Support
* YAML Configuration
* Default Headers

### Testing Support

* Pytest Integration
* Validation Helpers
* Response Utilities

### Documentation

* README
* Installation Guide
* Basic Usage Examples

---

# Upgrade Guide

## Upgrading from 1.0.x to 1.1.x

No breaking changes.

Upgrade normally:

```bash
pip install --upgrade pyrestkit
```

---

## Upgrading from 1.1.x to 1.2.x

No breaking changes.

AI functionality is completely optional.

Existing API automation projects continue to work without modification.

To enable AI features:

```bash
pip install "pyrestkit[ai]"
```

Example:

```python
from pyrestkit.ai import AIConfig

config = AIConfig(
    provider="openai",
    model="gpt-4.1-mini",
    api_key="YOUR_API_KEY",
)
```

AI analysis is enabled only when explicitly configured.

---

# Roadmap

Planned future enhancements include:

## v1.3.x

* Async HTTP client
* Retry and backoff strategies
* Request/response logging
* CLI utilities

## v1.4.x

* OpenAPI/Swagger import
* AI-powered test generation
* Plugin architecture
* HTML reporting

## Future

* GraphQL support
* WebSocket testing
* Performance testing utilities
* Mock server integration
* AI-generated API documentation

---

# Support

For bug reports, feature requests, or questions:

* Open a GitHub Issue
* Submit a Pull Request
* Start a GitHub Discussion

Community contributions are welcome.
