# Validation Guide

## Overview

Validation is the core of API automation.

Sending an HTTP request is only the first step; determining whether the response is correct is what makes an automated test valuable.

PyRestKit provides a flexible validation engine that allows developers to verify every aspect of an API response using clear, readable, and reusable assertions.

The validation subsystem is designed to be independent from the HTTP client, authentication layer, and AI subsystem.

---

# Design Goals

The validation engine is built around the following principles:

* Readability
* Reusability
* Type safety
* Clear error reporting
* Extensibility
* Framework independence

Each validator performs a single responsibility and raises meaningful framework-specific exceptions when validation fails.

---

# Validation Architecture

```text
                  HTTP Response
                        │
                        ▼
               Response Validator
                        │
      ┌─────────────────┼─────────────────┐
      ▼                 ▼                 ▼
 Status Code      Headers          Response Time
      ▼                 ▼                 ▼
 JSON Body      JSON Schema     Custom Validators
```

Every validator operates on the response object and can be used independently or combined within the same test.

---

# Validation Lifecycle

A typical validation flow looks like this:

```text
Send Request

      │

      ▼

Receive Response

      │

      ▼

Execute Validator

      │

      ▼

Validation Passed
        │
        └──────────────► Continue Test


OR


Validation Failed

      │

      ▼

Raise ValidationException

      │

      ▼

(Optional)

AI Failure Analysis
```

Validators stop execution immediately when a validation fails, making failures easy to locate.

---

# Status Code Validation

Status code validation verifies that the server returned the expected HTTP status.

Example:

```python
response.validate_status_code(200)
```

Typical use cases include:

* Successful GET requests
* Resource creation (201)
* Deletion (204)
* Client errors (400, 404)
* Authorization failures (401, 403)
* Server errors (500)

Example:

```python
response = client.get("/users")

response.validate_status_code(200)
```

---

# Header Validation

Header validation verifies response headers.

Example:

```python
response.validate_header(
    "Content-Type",
    "application/json",
)
```

Typical headers include:

* Content-Type
* Cache-Control
* ETag
* Authorization
* Location
* Server

Header validation is useful for verifying API contracts beyond the response body.

---

# JSON Body Validation

Most REST APIs return JSON.

PyRestKit allows validation of JSON values.

Example:

```python
response.json()["name"] == "John"
```

or

```python
response.validate_json(...)
```

Depending on the project, validation may include:

* required fields
* optional fields
* nested objects
* arrays
* data types
* business rules

---

# JSON Schema Validation

JSON Schema validation verifies that a response conforms to a predefined schema.

Example:

```python
response.validate_schema(
    "schemas/user.json",
)
```

Benefits include:

* contract verification
* regression detection
* documentation consistency
* reusable schemas

PyRestKit uses the JSON Schema standard for structural validation.

---

# Response Time Validation

Performance is often as important as correctness.

Example:

```python
response.validate_response_time(
    max_time_ms=500,
)
```

Typical thresholds depend on the application and environment.

Examples:

| Environment | Typical Target |
| ----------- | -------------- |
| Local       | < 300 ms       |
| QA          | < 500 ms       |
| Production  | < 200 ms       |

Response time validation helps detect performance regressions early.

---

# Custom Validators

Projects often require validations specific to their business domain.

Custom validators allow teams to encapsulate reusable validation logic.

Example:

```python
class UserValidator:
    def validate(self, response): ...
```

Typical examples include:

* Account state
* Order totals
* Business rules
* Domain-specific constraints

---

# Combining Validators

Multiple validations can be applied to the same response.

Example:

```python
response.validate_status_code(200)

response.validate_header(
    "Content-Type",
    "application/json",
)

response.validate_schema(
    "schemas/user.json",
)
```

Each validator focuses on a single concern.

---

# Exception Model

Validation failures raise dedicated framework exceptions.

Example:

```text
ValidationException

↓

Status Code Validation Failed

Expected: 201

Actual: 400
```

Framework-specific exceptions provide clearer diagnostics than generic assertion failures.

---

# AI Integration

The validation engine operates independently from AI.

When enabled, AI can analyze validation failures after an exception occurs.

Flow:

```text
Validation Failed

↓

ValidationException

↓

AIFailureAnalyzer

↓

Root Cause Explanation
```

This design keeps validation deterministic while allowing AI to provide additional insight.

---

# Best Practices

### Validate Status First

Status code validation should generally be the first assertion.

Example:

```python
response.validate_status_code(200)
```

Subsequent validations assume the expected response type.

---

### Validate Contracts

Use JSON Schema validation whenever stable API contracts exist.

Benefits include:

* consistency
* maintainability
* easier regression testing

---

### Keep Validators Focused

Each validator should verify one responsibility.

Avoid validators that perform multiple unrelated checks.

---

### Reuse Validators

Shared validators reduce duplication across test suites.

Examples include:

* UserValidator
* OrderValidator
* ProductValidator

---

### Avoid Over-Validation

Not every response requires every possible validation.

Validate only what is meaningful for the scenario under test.

---

# Testing Validators

Validator implementations should be unit tested independently.

Recommended scenarios include:

* valid response
* invalid response
* missing fields
* invalid headers
* incorrect status codes
* malformed JSON
* invalid schema
* boundary conditions

Independent testing improves confidence and simplifies maintenance.

---

# Extending the Validation Engine

New validators should follow the existing design principles.

Responsibilities should include only:

* reading the response
* verifying expectations
* raising meaningful exceptions

Validators should not:

* send HTTP requests
* authenticate users
* perform AI analysis
* modify responses

Keeping validators focused improves composability.

---

# Future Enhancements

The validation subsystem is designed to support future capabilities, including:

* JSONPath assertions
* XPath validation
* XML schema validation
* GraphQL response validation
* OpenAPI contract validation
* Soft assertions
* Validation reporting
* Assertion grouping
* Snapshot testing

These enhancements can be added while preserving the current validation architecture.

---

# Summary

The validation engine is the foundation of PyRestKit.

By separating validation into focused, reusable components, the framework enables clear, maintainable, and expressive API tests while remaining independent of transport, authentication, and AI analysis.

Whether validating HTTP status codes, response headers, JSON payloads, schemas, or performance, PyRestKit provides a consistent validation experience that scales from simple projects to enterprise automation suites.
