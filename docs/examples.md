# Examples

## Overview

This guide contains practical examples demonstrating common PyRestKit workflows.

Each example focuses on a single concept and can be adapted to real-world projects.

Examples progress from basic HTTP requests to advanced API validation and AI-assisted failure analysis.

---

# Creating an API Client

```python
from pyrestkit import APIClient

client = APIClient(base_url="https://api.example.com")
```

The API client manages:

* Base URL
* Default headers
* Authentication
* Timeouts
* Request execution

---

# Simple GET Request

```python
response = client.get("/users")

print(response.status_code)
print(response.json())
```

---

# GET Request with Query Parameters

```python
response = client.get(
    "/users",
    params={
        "page": 1,
        "limit": 20,
    },
)
```

Equivalent request:

```
GET /users?page=1&limit=20
```

---

# POST Request

```python
payload = {
    "name": "John",
    "email": "john@example.com",
}

response = client.post(
    "/users",
    json=payload,
)
```

---

# PUT Request

```python
payload = {
    "name": "Updated User",
}

response = client.put(
    "/users/1",
    json=payload,
)
```

---

# PATCH Request

```python
response = client.patch(
    "/users/1",
    json={
        "status": "ACTIVE",
    },
)
```

---

# DELETE Request

```python
response = client.delete("/users/1")
```

---

# Status Code Validation

```python
response = client.get("/users")

response.validate_status_code(200)
```

---

# Header Validation

```python
response.validate_header(
    "Content-Type",
    "application/json",
)
```

---

# JSON Validation

```python
body = response.json()

assert body["id"] == 1
assert body["name"] == "John"
```

---

# Schema Validation

```python
response.validate_schema(
    "schemas/user.json",
)
```

---

# Response Time Validation

```python
response.validate_response_time(
    max_time_ms=500,
)
```

---

# Bearer Authentication

```python
client.authenticate_bearer(
    token="YOUR_TOKEN",
)

response = client.get("/users")
```

---

# Basic Authentication

```python
client.authenticate_basic(
    username="admin",
    password="secret",
)
```

---

# API Key Authentication

```python
client.authenticate_api_key(
    key="API_KEY",
    header_name="X-API-Key",
)
```

---

# Default Headers

```python
client = APIClient(
    base_url="https://api.example.com",
    headers={
        "Accept": "application/json",
        "User-Agent": "PyRestKit",
    },
)
```

---

# Request Timeout

```python
client = APIClient(
    base_url="https://api.example.com",
    timeout=30,
)
```

---

# YAML Configuration

```yaml
base_url: https://api.example.com

timeout: 30

headers:
  Accept: application/json

ai:
  provider: openai
  model: gpt-4.1-mini
```

Loading configuration:

```python
config = AIConfig.from_mapping(yaml_config)
```

---

# Environment Variables

```
PYRESTKIT_AI_PROVIDER=openai
PYRESTKIT_AI_MODEL=gpt-4.1-mini
PYRESTKIT_AI_API_KEY=YOUR_API_KEY
```

```python
config = AIConfig.from_env()
```

---

# OpenAI Example

```python
from pyrestkit.ai import AIConfig
from pyrestkit.ai import analyze_failure

config = AIConfig(
    provider="openai",
    model="gpt-4.1-mini",
    api_key="YOUR_KEY",
)

analysis = analyze_failure(
    exception=error,
    response=response,
    config=config,
)

print(analysis)
```

---

# Gemini Example

```python
config = AIConfig(
    provider="gemini",
    model="gemini-2.5-pro",
    api_key="YOUR_KEY",
)
```

---

# Ollama Example

```python
config = AIConfig(
    provider="ollama",
    model="llama3.2",
    base_url="http://localhost:11434",
)
```

---

# AI-Assisted Failure Analysis

```python
try:
    response.validate_status_code(200)

except Exception as error:
    explanation = analyze_failure(
        exception=error,
        response=response,
        config=config,
    )

    print(explanation)
```

Typical AI output:

```
Expected status code 200.

Received 500.

The response indicates an internal server error.

The stack trace suggests the request payload is missing a required field.
```

---

# Custom Headers

```python
response = client.get(
    "/users",
    headers={
        "X-Correlation-ID": "abc-123",
    },
)
```

---

# Multiple Validations

```python
response.validate_status_code(200)

response.validate_header(
    "Content-Type",
    "application/json",
)

response.validate_schema(
    "schemas/user.json",
)

response.validate_response_time(
    max_time_ms=500,
)
```

---

# Using Pytest

```python
def test_get_users(client):

    response = client.get("/users")

    response.validate_status_code(200)
```

---

# Data-Driven Testing

```python
import pytest


@pytest.mark.parametrize(
    "user_id",
    [1, 2, 3],
)
def test_users(client, user_id):

    response = client.get(f"/users/{user_id}")

    response.validate_status_code(200)
```

---

# Error Handling

```python
try:
    response.validate_schema(
        "schemas/user.json",
    )

except ValidationException as error:
    print(error)
```

---

# Complete End-to-End Example

```python
from pyrestkit import APIClient
from pyrestkit.ai import AIConfig
from pyrestkit.ai import analyze_failure

client = APIClient(
    base_url="https://api.example.com",
)

client.authenticate_bearer(
    token="TOKEN",
)

config = AIConfig(
    provider="openai",
    model="gpt-4.1-mini",
    api_key="YOUR_KEY",
)

response = client.get("/users")

try:
    response.validate_status_code(200)

    response.validate_header(
        "Content-Type",
        "application/json",
    )

    response.validate_schema(
        "schemas/user.json",
    )

except Exception as error:
    explanation = analyze_failure(
        exception=error,
        response=response,
        config=config,
    )

    print(explanation)
```

---

# Best Practices

* Keep tests focused on one scenario.
* Reuse API client instances where practical.
* Store secrets in environment variables.
* Validate status codes before parsing JSON.
* Use JSON Schema for contract validation.
* Enable AI analysis only for failed tests.
* Keep custom validators reusable.
* Organize schemas under a dedicated `schemas/` directory.
* Separate test data from test logic.
* Prefer readable assertions over complex helper functions.

---

# Summary

These examples demonstrate the typical workflows supported by PyRestKit, from simple HTTP requests to enterprise-grade API testing with authentication, schema validation, reusable configuration, and AI-assisted failure analysis.

As your project grows, these building blocks can be combined to create maintainable, scalable, and highly readable API automation suites.
