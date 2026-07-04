# 🚀 Python API Automation Framework

> A production-ready, scalable, and type-safe REST API automation framework built with Python.

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![Pytest](https://img.shields.io/badge/Tested%20With-Pytest-green.svg)
![Ruff](https://img.shields.io/badge/Lint-Ruff-orange.svg)
![MyPy](https://img.shields.io/badge/Type%20Checked-MyPy-blueviolet.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 📖 Overview

Python API Automation Framework is a modern automation framework designed for testing REST APIs with clean architecture, fluent APIs, and strong type safety.

The framework is built around maintainability, scalability, and developer productivity. It provides reusable components for API clients, authentication, response validation, schema validation, retry mechanisms, hooks, request builders, and business-layer clients.

Whether you are testing a small REST API or building an enterprise automation suite, the framework provides a structured and extensible foundation.

---

## ✨ Key Features

### 🔹 Fluent Request Builder

Create readable API requests using a fluent interface.

```python
response = (
    api_client.request()
    .post("/users")
    .json(payload)
    .header("Authorization", token)
    .timeout(30)
    .send()
)
```

---

### 🔹 Multiple Authentication Strategies

Supports multiple authentication mechanisms out of the box.

* Bearer Token Authentication
* Basic Authentication
* API Key Authentication
* Authentication Manager
* Token Cache
* Token Manager

---

### 🔹 Strongly Typed Responses

Work with Python models instead of raw dictionaries.

```python
user = response.as_model(UserResponse)

print(user.email)
```

---

### 🔹 Fluent Response Assertions

Readable assertions for API validation.

```python
response.should.have_status(200)

response.should.be_successful()

response.should.have_json(
    "data.email",
    "janet@example.com",
)

response.should.match_schema(
    "schemas/user.json",
)
```

---

### 🔹 Response Wrapper

Provides a rich response abstraction.

* Status Code
* Headers
* Response Body
* Response Time
* JSON Access
* Model Serialization

---

### 🔹 JSON Schema Validation

Validate responses against JSON Schema.

```python
SchemaValidator.validate(
    response,
    "schemas/user.json",
)
```

---

### 🔹 Retry Mechanism

Automatically retry failed requests using configurable retry policies.

Ideal for handling:

* Temporary network failures
* Server-side transient errors
* Rate limiting
* Flaky environments

---

### 🔹 Hook System

Execute custom logic before and after API requests.

Examples include:

* Logging
* Request modification
* Metrics collection
* Reporting
* Custom validation

---

### 🔹 Business API Clients

Encapsulate endpoint logic into reusable business clients.

```python
user_client.list_users()

user_client.get_user(2)

user_client.create_user(request)
```

---

### 🔹 Test Data Factories

Generate reusable request payloads.

```python
UserFactory.random()

UserFactory.admin()

UserFactory.load_from_file(...)
```

---

### 🔹 Clean Architecture

The framework follows a layered architecture with clear separation of responsibilities.

* Configuration
* Authentication
* HTTP Client
* Request Builder
* Business Clients
* Validators
* Assertions
* Response Models
* Retry
* Hooks
* Factories

---

### 🔹 Production Quality

The project follows modern Python development practices.

* ✅ Strict MyPy type checking
* ✅ Ruff linting
* ✅ Pytest test suite
* ✅ Type hints throughout
* ✅ Modular architecture
* ✅ Extensible design
* ✅ Clean coding standards

---

## 🎯 Goals

This framework aims to:

* Simplify REST API automation.
* Promote reusable and maintainable test code.
* Encourage strong typing and clean architecture.
* Reduce boilerplate in API tests.
* Provide a scalable foundation for enterprise automation projects.

---

## 🚀 Getting Started

Clone the repository:

```bash
git clone <repository-url>

cd python-api-framework
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment:

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Verify the installation:

```bash
ruff check .

mypy .

pytest -v
```

Expected output:

```text
All checks passed!
Success: no issues found
All tests passed
```
#### PART 2 ###

---

# 📂 Project Structure

```text
python-api-framework/
│
├── src/
│   ├── assertions/
│   ├── auth/
│   ├── builder/
│   ├── clients/
│   ├── config/
│   ├── constants/
│   ├── core/
│   ├── database/
│   ├── endpoints/
│   ├── exceptions/
│   ├── factories/
│   ├── hooks/
│   ├── models/
│   │   ├── request/
│   │   └── response/
│   ├── pipeline/
│   ├── response/
│   ├── retry/
│   ├── serializers/
│   ├── types/
│   ├── utils/
│   └── validators/
│
├── schemas/
├── tests/
├── docs/
├── logs/
├── requirements.txt
├── pyproject.toml
├── pytest.ini
└── README.md
```

---

# 🏗 Architecture

The framework follows a layered architecture.

```text
                Test Cases
                     │
                     ▼
             Business Clients
                     │
                     ▼
          Fluent Request Builder
                     │
                     ▼
               API Client
                     │
                     ▼
          Authentication Layer
                     │
                     ▼
            Request Executor
                     │
                     ▼
               HTTP Session
                     │
                     ▼
                 REST API
                     │
                     ▼
           FrameworkResponse
                     │
                     ▼
    Assertions • Validators • Models
```

Each layer has a single responsibility, making the framework easy to extend and maintain.

---

# ⚙️ Configuration

Framework configuration is managed through `ConfigManager`.

Example:

```python
from src.config import ConfigManager

config = ConfigManager("dev")
```

Example configuration file:

```json
{
    "base_url": "https://reqres.in/api",
    "timeout": 30,
    "verify_ssl": true,
    "auto_raise_exceptions": true
}
```

You can maintain separate configurations for different environments:

```text
config/
├── dev.json
├── qa.json
├── stage.json
└── prod.json
```

---

# 🚀 Creating an API Client

Create a reusable API client for your application.

```python
from src.auth import BearerAuth
from src.config import ConfigManager
from src.core import APIClient
from src.core import SessionManager

config = ConfigManager("dev")

session = SessionManager()

auth = BearerAuth(
    token="your-access-token",
)

client = APIClient(
    config=config,
    session_manager=session,
    auth_strategy=auth,
)
```

The client is intended to be created once and reused throughout your test suite.

---

# 🔐 Authentication

The framework supports multiple authentication strategies.

## Bearer Token

```python
from src.auth import BearerAuth

auth = BearerAuth(
    token="your-token",
)
```

---

## Basic Authentication

```python
from src.auth import BasicAuth

auth = BasicAuth(
    username="admin",
    password="password",
)
```

---

## API Key Authentication

```python
from src.auth import APIKeyAuth

auth = APIKeyAuth(
    key="your-api-key",
    header_name="X-API-Key",
)
```

Authentication can be plugged into the API client without changing test code.

---

# ✨ Fluent Request Builder

The framework provides a fluent API for constructing requests.

### GET Request

```python
response = (
    client.request()
    .get("/users")
    .send()
)
```

---

### GET with Query Parameters

```python
response = (
    client.request()
    .get("/users")
    .query(
        page=2,
        per_page=5,
    )
    .send()
)
```

---

### POST Request

```python
response = (
    client.request()
    .post("/users")
    .json(
        {
            "name": "John",
            "job": "Engineer",
        }
    )
    .send()
)
```

---

### Custom Headers

```python
response = (
    client.request()
    .get("/users")
    .header(
        "X-Request-Id",
        "12345",
    )
    .send()
)
```

---

### Multiple Headers

```python
response = (
    client.request()
    .post("/users")
    .headers(
        {
            "X-App": "Demo",
            "X-Version": "1.0",
        }
    )
    .send()
)
```

---

### Request Timeout

```python
response = (
    client.request()
    .get("/users")
    .timeout(15)
    .send()
)
```

---

# 👨‍💼 Business Clients

Business clients encapsulate API endpoints into reusable methods.

Example:

```python
from src.clients import UserClient

user_client = UserClient(client)

response = user_client.list_users()
```

Retrieve a single user:

```python
response = user_client.get_user(2)
```

Create a user:

```python
from src.models import CreateUserRequest

request = CreateUserRequest(
    name="John",
    job="Engineer",
)

response = user_client.create_user(request)
```

Update a user:

```python
from src.models import UpdateUserRequest

request = UpdateUserRequest(
    name="John Updated",
    job="Senior Engineer",
)

response = user_client.update_user(
    2,
    request,
)
```

Delete a user:

```python
response = user_client.delete_user(2)
```

Using business clients keeps test cases concise and separates business logic from HTTP implementation details.

### PART 3 ###

---

# 📦 Response Handling

Instead of working directly with `requests.Response`, the framework returns a `FrameworkResponse` object that provides additional functionality while preserving compatibility with the original response.

```python
response = user_client.get_user(2)
```

---

## Status Code

```python
assert response.status == 200

# or

assert response.status_code == 200
```

---

## Headers

```python
print(response.headers)

content_type = response.headers["Content-Type"]
```

---

## Response Time

```python
print(response.elapsed)
```

---

## Raw Response

Access the original `requests.Response` object whenever needed.

```python
raw = response.raw

print(raw.cookies)
print(raw.history)
```

---

## JSON Response

Retrieve the response body as a Python object.

```python
body = response.json()

print(body)
```

---

# 📄 ResponseBody

`ResponseBody` provides convenient access to JSON responses using dot notation.

Instead of writing:

```python
response.json()["data"]["email"]
```

you can simply write:

```python
response.body.data.email
```

Example:

```python
response = user_client.get_user(2)

print(response.body.data.id)
print(response.body.data.email)
print(response.body.data.first_name)
print(response.body.data.last_name)
```

Lists are also supported.

```python
users = response.body.data

print(users[0].email)
print(users[0].first_name)
```

Convert the response back to a dictionary when needed.

```python
dictionary = response.body.to_dict()
```

---

# 🧩 Model Serialization

Deserialize API responses into strongly typed Python models.

Example response model:

```python
@dataclass(slots=True)
class UserResponse:
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: str
```

Deserialize a single object.

```python
user = response.as_model(UserResponse)

print(user.email)
print(user.first_name)
```

Deserialize a list of objects.

```python
users = response.as_list(UserResponse)

print(users[0].email)
```

Using typed models improves readability, IDE auto-completion, and static type checking.

---

# ✅ Fluent Assertions

The framework provides expressive assertions that make API tests easier to read.

## Status Code

```python
response.should.have_status(200)
```

---

## Successful Response

```python
response.should.be_successful()
```

---

## Header Validation

```python
response.should.have_header(
    "Content-Type",
    "application/json",
)
```

---

## JSON Value

Validate values using dot notation.

```python
response.should.have_json(
    "data.email",
    "janet@example.com",
)
```

---

## JSON Array Count

```python
response.should.have_json_count(
    "data",
    6,
)
```

---

## JSON Contains

```python
response.should.have_json_contains(
    "support.text",
    "ReqRes",
)
```

---

## Response Time

```python
response.should.respond_within(1000)
```

Validates that the response is received within the specified number of milliseconds.

---

## Schema Validation

```python
response.should.match_schema(
    "schemas/user_schema.json",
)
```

This validates the response against a JSON Schema and raises an exception if the response structure does not match the schema.

---

# 📋 Validators

The framework also provides standalone validators for situations where assertions are not required.

## Response Validator

```python
from src.validators import ResponseValidator

ResponseValidator.validate_status(
    response,
    200,
)
```

---

## JSON Schema Validator

```python
from src.validators import SchemaValidator

SchemaValidator.validate(
    response,
    "schemas/user_schema.json",
)
```

These validators can be used independently in utility functions, pipelines, or custom test frameworks.

---

# 🏭 Test Data Factories

Factories simplify the creation of reusable test data.

Example:

```python
from src.factories import UserFactory

request = UserFactory.random()
```

Create predefined users.

```python
admin = UserFactory.admin()

guest = UserFactory.guest()
```

Factories help eliminate duplicated request payloads and keep tests concise.

---

# 🔄 Retry Support

Retry policies improve reliability when interacting with unstable services.

Example:

```python
retry_handler = RetryHandler(
    max_retries=3,
    delay=2,
)
```

Typical retry scenarios include:

* Temporary network failures
* HTTP 5xx responses
* Rate limiting
* Service warm-up periods

---

# 🪝 Hooks

Hooks allow custom logic to be executed during request processing.

Available hook points:

* Before Request
* After Response

Example:

```python
hook_manager.before_request(...)

hook_manager.after_response(...)
```

Typical use cases include:

* Logging
* Reporting
* Metrics
* Custom authentication
* Request modification
* Response auditing

---

# 🧪 Running Tests

Run the complete quality suite before committing changes.

```bash
ruff check .

mypy .

pytest -v
```

Expected output:

```text
All checks passed!

Success: no issues found

===================== test session starts =====================

...

===================== 100% passed =====================
```

The project follows strict quality gates:

* Ruff for linting
* MyPy for static type checking
* Pytest for automated testing

### PART 4 ###

---

# 🎯 Design Principles

The framework is built around a few core principles.

### Readability First

Tests should be easy to read and understand.

```python
response.should.have_status(200)
```

is much easier to understand than multiple low-level assertions.

---

### Strong Typing

The framework embraces Python type hints to provide:

* Better IDE support
* Static analysis with MyPy
* Safer refactoring
* Improved developer experience

---

### Clean Architecture

Each component has a single responsibility.

```
Configuration
        │
Authentication
        │
HTTP Client
        │
Request Builder
        │
Business Client
        │
Response Wrapper
        │
Assertions & Validators
```

This makes the framework modular and easy to extend.

---

### Reusability

Common functionality is centralized into reusable components such as:

* Business Clients
* Validators
* Assertions
* Factories
* Authentication Strategies
* Hooks
* Retry Policies

---

# 📈 Roadmap

The following features are planned for future releases.

## Version 1.1

* Async API Client (`httpx`)
* OAuth2 Authentication
* Cookie Authentication
* Multipart File Upload Support
* Enhanced Logging

---

## Version 1.2

* GraphQL Client
* XML Response Support
* XML Assertions
* XML Schema Validation

---

## Version 2.0

* OpenAPI / Swagger Client Generation
* Allure Reporting Integration
* HTML Reporting
* Parallel Execution Utilities
* Plugin System
* CLI Support

---

# 🤝 Contributing

Contributions are welcome!

If you would like to improve the project:

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Ensure all quality checks pass.
5. Submit a Pull Request.

Before submitting code, please run:

```bash
ruff check .

mypy .

pytest -v
```

Every contribution should maintain the project's coding standards and test coverage.

---

# 🏷 Versioning

This project follows **Semantic Versioning (SemVer)**.

```
MAJOR.MINOR.PATCH
```

Examples:

```
1.0.0
1.1.0
1.1.1
2.0.0
```

* **MAJOR** – Breaking API changes
* **MINOR** – New backward-compatible features
* **PATCH** – Bug fixes and small improvements

---

# 📄 License

This project is licensed under the MIT License.

You are free to use, modify, and distribute this software in accordance with the terms of the license.

---

# 🙏 Acknowledgements

This framework is built using several excellent open-source Python libraries.

* Requests
* Pytest
* Requests-Mock
* JSONSchema
* MyPy
* Ruff

A big thank you to the maintainers and contributors of these projects.

---

# ⭐ Support

If you find this project useful:

* ⭐ Star the repository
* 🐞 Report bugs
* 💡 Suggest new features
* 🤝 Contribute improvements

Your feedback helps improve the framework.

---

# 📬 Contact

If you have questions, suggestions, or ideas for improvement, feel free to open an issue or start a discussion in the repository.

---

# 🎉 Conclusion

Python API Automation Framework is designed to provide a clean, scalable, and maintainable approach to REST API automation.

By combining:

* Fluent APIs
* Strong typing
* Business-layer clients
* Rich response handling
* Fluent assertions
* Schema validation
* Authentication strategies
* Retry mechanisms
* Hook support
* Test data factories

the framework helps teams write expressive, reliable, and maintainable API tests while following modern Python best practices.

Happy Testing! 🚀