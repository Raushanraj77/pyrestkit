# Authentication Guide

## Overview

Most REST APIs require authentication before protected resources can be accessed.

PyRestKit provides a flexible authentication layer that separates authentication logic from request execution, making authentication strategies reusable, testable, and easy to extend.

The authentication subsystem is designed so that switching authentication mechanisms does not require changes to the API client implementation.

---

# Design Goals

The authentication layer is built around the following principles:

* Separation of concerns
* Reusability
* Extensibility
* Type safety
* Framework independence
* Minimal boilerplate

Authentication is responsible only for preparing requests. It does not execute HTTP calls or validate responses.

---

# Authentication Flow

```text
               API Request

                    │

                    ▼

        Authentication Strategy

                    │

                    ▼

      Request Headers / Parameters

                    │

                    ▼

              HTTP Transport

                    │

                    ▼

               API Response
```

Authentication modifies the outgoing request before it is sent.

---

# Supported Authentication Methods

PyRestKit includes support for common authentication mechanisms.

| Authentication        | Typical Usage         |
| --------------------- | --------------------- |
| Bearer Token          | JWT / OAuth APIs      |
| Basic Authentication  | Username and password |
| API Key               | Public REST APIs      |
| OAuth 2.0             | Enterprise APIs       |
| Custom Authentication | Internal services     |

Additional authentication methods can be added without modifying the API client.

---

# Bearer Token Authentication

Bearer authentication is commonly used with JWT and OAuth access tokens.

Example:

```python
from pyrestkit import APIClient

client = APIClient(
    base_url="https://api.example.com",
)

client.authenticate_bearer(
    token="YOUR_ACCESS_TOKEN",
)

response = client.get("/users")
```

Resulting request header:

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

---

# Basic Authentication

Basic authentication sends a Base64-encoded username and password.

Example:

```python
client.authenticate_basic(
    username="admin",
    password="secret",
)
```

Resulting header:

```http
Authorization: Basic <base64 credentials>
```

This method is commonly used by internal services and legacy APIs.

---

# API Key Authentication

Many REST APIs use API keys instead of bearer tokens.

Example:

```python
client.authenticate_api_key(
    key="YOUR_API_KEY",
    header_name="X-API-Key",
)
```

Generated request:

```http
X-API-Key: YOUR_API_KEY
```

Some APIs use different header names such as:

* X-API-Key
* Api-Key
* x-api-token

PyRestKit allows the header name to be customized.

---

# OAuth 2.0

Many enterprise APIs use OAuth 2.0 access tokens.

Typical workflow:

```text
User Credentials

        │

        ▼

Authorization Server

        │

        ▼

Access Token

        │

        ▼

Bearer Authentication

        │

        ▼

Protected Resource
```

PyRestKit expects a valid access token to be provided.

Token acquisition is intentionally kept separate because OAuth implementations vary between providers.

---

# Custom Authentication

Some organizations use proprietary authentication mechanisms.

Examples include:

* Signed requests
* HMAC authentication
* Custom headers
* Session tokens
* Internal gateways

These strategies can be implemented without modifying the API client.

---

# Authentication Lifecycle

The request lifecycle with authentication is:

```text
Create Request

        │

        ▼

Apply Authentication

        │

        ▼

Merge Headers

        │

        ▼

Send Request

        │

        ▼

Receive Response
```

Authentication occurs immediately before the HTTP request is sent.

---

# Header Management

Authentication headers are merged with user-defined headers.

Example:

```python
client.get(
    "/users",
    headers={
        "Accept": "application/json",
    },
)
```

Final request may include:

```http
Accept: application/json
Authorization: Bearer token
```

Framework-generated authentication headers coexist with user-provided headers.

---

# Authentication and AI

The AI subsystem maintains its own authentication independent of API requests.

For example:

* API Client authentication secures requests to the application under test.
* AI Provider authentication secures requests to the selected LLM provider.

These two authentication flows are intentionally separate.

Example:

```text
Application Request

↓

Bearer Token

↓

REST API


AI Analysis

↓

OpenAI API Key

↓

OpenAI API
```

Keeping these concerns separate simplifies maintenance and avoids accidental credential reuse.

---

# Security Best Practices

When working with authentication:

* Never hardcode credentials in source code.
* Store secrets in environment variables or secret managers.
* Rotate credentials regularly.
* Use HTTPS for authenticated requests.
* Grant the minimum required permissions.
* Avoid logging sensitive authentication headers.

---

# Error Handling

Authentication-related issues commonly include:

* Missing credentials
* Expired tokens
* Invalid API keys
* Unauthorized requests
* Forbidden responses

These failures should be handled separately from validation failures to simplify debugging.

---

# Testing Authentication

Authentication logic should be tested independently from business functionality.

Recommended tests include:

* Header generation
* Credential validation
* Missing credentials
* Invalid credentials
* Header precedence
* Authentication switching

Using mocked HTTP sessions allows authentication behavior to be verified without contacting external services.

---

# Extending Authentication

New authentication strategies should follow the existing design principles:

* Perform only authentication logic.
* Avoid request execution.
* Avoid response validation.
* Produce deterministic request modifications.
* Keep implementations small and focused.

A well-isolated authentication strategy is easier to reuse across projects.

---

# Future Enhancements

The authentication subsystem is designed to support additional mechanisms, including:

* OAuth refresh token handling
* AWS Signature Version 4
* Mutual TLS (mTLS)
* OpenID Connect helpers
* Pluggable authentication middleware
* Automatic token refresh
* Credential caching

These capabilities can be added while preserving the existing authentication architecture.

---

# Summary

PyRestKit provides a modular authentication layer that supports common REST API authentication mechanisms while remaining independent of request execution and response validation.

This separation improves maintainability, simplifies testing, and allows new authentication strategies to be introduced with minimal impact on the rest of the framework.
