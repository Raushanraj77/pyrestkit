Our Goal

By the end, you'll have an enterprise-grade API automation framework that supports:

✅ REST APIs
✅ Multiple environments (DEV, QA, UAT, PROD)
✅ Database validation
✅ Authentication
✅ Logging
✅ Reporting
✅ JSON Schema validation
✅ CI/CD integration
✅ Docker (optional later)
✅ Extensible architecture
Phase 1 - Environment Setup
Step 1: Open the project
cd python-api-framework

Verify you're inside the project:

pwd
Step 2: Create a Virtual Environment

Never install packages globally for a project.

Run:

python3 -m venv .venv

You should now have:

python-api-framework
│
├── .venv
Step 3: Activate the Virtual Environment

On macOS/Linux:

source .venv/bin/activate

Your terminal should change to something like:

(.venv) MacBook-Pro python-api-framework %

This means you're working inside the project's isolated Python environment.

Step 4: Upgrade pip
python -m pip install --upgrade pip
Step 5: Install the Initial Dependencies

For now, install only the essentials:

pip install pytest requests python-dotenv

We'll add more libraries later as we need them.

Step 6: Freeze Dependencies
pip freeze > requirements.txt

Now anyone can recreate your environment with:

pip install -r requirements.txt
Step 7: Create the Initial Folder Structure

Run these commands:

mkdir config
mkdir core
mkdir clients
mkdir database
mkdir models
mkdir schemas
mkdir testdata
mkdir tests
mkdir utils
mkdir validations
mkdir reports
mkdir logs
Step 8: Create the Initial Files
touch pytest.ini
touch README.md
touch .gitignore
touch .env
Your project should now look like this
python-api-framework/
│
├── src/
│   ├── config/
│   ├── core/
│   ├── clients/
│   ├── database/
│   ├── models/
│   ├── utils/
│   └── validations/
│
├── tests/
├── schemas/
├── testdata/
├── reports/
├── logs/
├── requirements.txt
├── pytest.ini
└── README.md
Why This Structure?

Create Package Files

Run:

touch src/__init__.py
touch src/config/__init__.py
touch src/core/__init__.py
touch src/clients/__init__.py
touch src/database/__init__.py
touch src/models/__init__.py
touch src/utils/__init__.py
touch src/validations/__init__.py

These files mark the directories as Python packages.

A common mistake is putting everything under a single tests/ folder. That works for small projects but becomes difficult to maintain as the framework grows.

Instead, we separate responsibilities:

Folder	Purpose
core	Shared framework code (API client, auth, logging, retry logic)
clients	Endpoint-specific clients (Users, Orders, Payments, etc.)
database	Database connection and repository classes
models	Request and response data models
schemas	JSON Schema files for response validation
testdata	Input payloads and test data
tests	Test cases only
utils	General helper functions
validations	Reusable validation logic
config	Environment-specific configuration

This separation keeps the framework organized and scalable.

Before we continue

Please run the setup steps above and tell me:

Are you using VS Code?
Does your prompt show (.venv) after activation?
Paste the output of:
python --version
pip --version
pytest --version

-----

Sprint 1: Framework Foundation

We're not writing tests yet.

We'll build the foundation first.

Framework
│
├── Configuration Manager
├── Logger
├── API Client
├── Response Validator
├── Authentication
├── Base Test
└── Utilities

Think of it like building a house—you don't start with the roof.

Step 1: Configuration Management
Why do we need it?

Imagine your company has:

DEV
QA
UAT
PRE-PROD
PROD

Each environment has different:

Base URL
Database
Username
Password
API Keys
Timeouts

If you hardcode them:

BASE_URL = "https://qa.company.com"

every environment change requires code changes.

Instead, we'll separate configuration from code.

Create the Configuration Files

Inside the config folder, create:

config/
│
├── config.py
├── dev.json
├── qa.json
├── uat.json
└── prod.json

Why JSON?

Some companies use YAML, TOML, or environment variables. JSON is simple and familiar, making it a good starting point. Once the framework is working, it's easy to swap to another configuration format.

Next: config.py

We'll create a reusable class that:

Loads the correct environment file.
Exposes configuration values to the rest of the framework.
Ensures the file is read only once.

We'll also use Python type hints and encapsulation to keep it clean.

Rather than jumping straight into code, I want to explain the design first.

Why not just do this?
import json

with open("config/dev.json") as f:
    config = json.load(f)

Because if 50 different files all read the JSON independently:

The file is opened 50 times.
Every module has duplicate code.
Future changes become difficult.

Instead, we'll build a Configuration Manager.

API Client
        │
        │
Response Validator
        │
        │
Authentication
        │
        │
Database
        │
        ▼
 Configuration Manager

Every component asks the Configuration Manager for values instead of reading files directly.

This gives us:

Single responsibility
Centralized configuration
Easier testing
Easier maintenance

-----------------

>>>
🚀 Sprint 1 - Module 1
Build the Configuration Manager

Before writing code, I want you to think like a Software Engineer, not just an Automation Engineer.

Suppose tomorrow your company says:

Run against DEV

Next day:

Run against QA

Next day:

Run against UAT

Should we modify Python code?

No.

Instead, we should simply change:

pytest --env=qa

or

pytest --env=dev

Everything else should work automatically.

This is how enterprise frameworks work.

>>>>
First Design Discussion

There are several ways to implement a configuration manager.

Approach 1 (Bad)

Every file reads JSON.

API Client
     ↓
Read JSON

Logger
     ↓
Read JSON

Database
     ↓
Read JSON

Problems:

Reads the same file repeatedly
Duplicate code
Difficult to maintain

>>Approach 2 (Better)

Create one class.

ConfigManager

Every module uses it.

API Client
        │
Logger  │
Database│
Validator
        │
        ▼
 ConfigManager

This is the approach we'll use.

>>What should ConfigManager do?

It should answer questions like:

What's my Base URL?

What's my Timeout?

Which Environment?

What Headers?

What's my Database URL?

without any module knowing where those values come from.

>>
Think Before Coding

Imagine another developer writes:

config = ConfigManager()

url = config.base_url

or

timeout = config.timeout

Wouldn't that look much cleaner than:

with open(...)
json.load(...)
config["base_url"]

Exactly.

This is the benefit of abstraction.

>>>>
Let's Understand Every Line
Why Path instead of "config/dev.json"?

Bad:

open("config/dev.json")

This fails if the working directory changes.

Good:

Path(__file__).parent

It always starts from the location of config.py, making it portable across operating systems.

>>Configure Pytest

Edit pytest.ini so it contains:

[pytest]
pythonpath = .
testpaths = tests
python_files = test_*.py
python_functions = test_*

The pythonpath = . line tells pytest to include the project root on sys.path, allowing src to be imported.

>>>>
What We'll Build Next

Inside:

src/core/

We'll create:

logger.py

It will:

Create log files automatically.
Write logs to both the console and a file.
Format timestamps.
Support different log levels (INFO, WARNING, ERROR).
Be reusable across the entire framework.

Later, the APIClient will use this logger without any extra code in your tests.
>>>>
One Improvement Before We Continue

Since this is a long-term project, I'd like us to adopt a few engineering practices from day one.

We'll use:

PEP 8 coding style.
Type hints everywhere.
Docstrings for all public classes and methods.
One class per file.
SOLID principles where appropriate.
Meaningful commit messages (once we start using Git).

These habits make a huge difference in large codebases.

How I Want to Teach This

Rather than dumping 500 lines of code at you, I'd like each module to follow this pattern:

Problem statement – Why do we need this component?
Design discussion – What are the possible approaches?
Implementation – We write the code together.
Testing – We verify it works.
Refactoring – We improve it if needed.
Interview perspective – How to explain this design in an interview.

This is the same approach I'd use to mentor a new SDET on my team.

>>>>
Design Discussion (Important)

There are two ways to log.

Option 1 (Bad)

Every API method writes logs.

logger.info(...)
logger.info(...)
logger.info(...)

Imagine writing that in 300 API methods.

Not maintainable.

Option 2 (Enterprise)

Only the APIClient logs.

Every request automatically gets logged.

The test doesn't even know logging exists.

Test
 │
 ▼
APIClient
 │
 ├── Logs request
 ├── Sends request
 ├── Logs response
 │
 ▼
returns Response

This is the architecture we'll implement.

>>>
Our Logging Goals

Every API call should automatically produce something like:

==================================================
REQUEST
==================================================
Method      : POST
URL         : https://reqres.in/api/users
Headers     : {...}
Payload     : {...}

==================================================
RESPONSE
==================================================
Status Code : 201
Response Time : 245 ms
Body :
{
    ...
}
==================================================

No print() statements.

Enterprise logging should answer questions like:

Which endpoint failed?
What payload was sent?
Which headers were used?
How long did the request take?
Which test executed it?
Which environment was used?
What correlation ID was returned?

Without rerunning the test.

>>>>
❌ We are NOT building a "Requests Framework"

We're building an Automation Platform.

There's a huge difference.

A beginner framework looks like this:

Test
   │
requests.post()
   │
assert

A professional framework looks like this:

                Tests
                   │
                   ▼
             Business Client
                   │
                   ▼
              API Client
                   │
                   ▼
 Authentication → Retry → Logger → Validator
                   │
                   ▼
                requests

Notice something?

Tests never call requests directly.

That is one of the biggest differences between junior and senior automation engineers.

>>>>
Our Architecture

We're going to follow a layered architecture.

Tests
│
├── UserClient
├── ProductClient
├── PaymentClient
│
▼
APIClient
│
├── Logger
├── Retry
├── Authentication
├── Request Builder
│
▼
requests.Session
│
▼
REST API

Every responsibility has its own layer.

>>>>>>>>>>>
Where We're Heading

By the end, our framework will include:

Framework

├── Configuration Manager
├── Logger
├── API Client
├── Authentication Manager
├── Token Manager
├── Retry Manager
├── Session Manager
├── Database Manager
├── Response Validator
├── JSON Schema Validator
├── Request Builder
├── Report Manager
├── Environment Manager
├── Parallel Execution Support
├── CI/CD Integration
├── Docker Support
├── Mock Server Support
└── Performance Metrics
Here's one thing I'd like to improve over many enterprise frameworks

Most API frameworks grow organically and end up tightly coupled. I'd like us to design ours around a few core principles:

Dependency Injection instead of creating dependencies directly inside classes.
Factory Pattern for authentication and database providers.
Strategy Pattern for different authentication mechanisms and retry policies.
Repository Pattern for database access.
Builder Pattern for constructing complex requests.

The benefit is that when a project moves from API keys to OAuth2, or from PostgreSQL to Oracle, the tests don't change—only the implementation behind the interface does.

>>>>>>>>
Sprint 1 - Module 2
Logging Framework
Why Logging Matters

Imagine a test fails at 2:00 AM in Jenkins.

Without logging, you only see:

AssertionError
Expected 201
Actual 500

Now you're asking:

Which endpoint failed?
What payload was sent?
Which environment?
Which authentication token?
How long did the request take?
What response body came back?

Without logs, you'll rerun the test and hope to reproduce the issue.

That's not acceptable in enterprise automation.

Logging Architecture

Instead of this:

print(response.json())

We'll build this:

Test
 │
 ▼
UserClient
 │
 ▼
APIClient
 │
 ▼
FrameworkLogger
 │
 ▼
logs/framework.log

Notice that tests don't know anything about logging.

That's a key design principle: cross-cutting concerns (like logging) belong in shared infrastructure, not in test cases.

>>>>>
Let's Understand the Design
Why FrameworkLogger?

Could we just write:

logging.basicConfig(...)

Yes.

Should we?

No.

Reasons:

Different modules may configure logging differently.
basicConfig() is global.
It becomes difficult to customize later.

Wrapping it in our own class gives us complete control.

Why Singleton?

Notice this line:

_logger = None

Every module will call:

logger = FrameworkLogger.get_logger()

But only one logger instance will exist.

Without this, each import could add another handler, resulting in duplicated log messages.

Why Check logger.handlers?

This is a subtle but important detail.

If you accidentally configure the logger twice, you'll see:

INFO Request Started
INFO Request Started

Every log appears twice.

Checking logger.handlers prevents duplicate handlers from being added.

>>>>>
Before We Write APIClient

I want to conduct an Architecture Design Review (ADR), exactly like we would in a real company.

Question

Should APIClient know about authentication?

Many frameworks do this:

client.post("/users")

Internally:

APIClient

↓

Create Token

↓

Create Headers

↓

Send Request
I DON'T LIKE THIS DESIGN

Why?

Because now APIClient has two responsibilities:

Sending HTTP requests ❌
Authenticating users ❌

That violates the Single Responsibility Principle (SRP).

Better Architecture
Tests
 │
 ▼
UserClient
 │
 ▼
APIClient
 │
 ▼
RequestBuilder
 │
 ├── Authentication
 ├── Headers
 ├── Query Params
 ├── Payload
 └── Timeout
 │
 ▼
requests.Session
Responsibilities

APIClient

Knows how to send HTTP requests.
Doesn't know where the token came from.

TokenManager

Knows how to obtain, cache, and refresh tokens.

RequestBuilder

Combines headers, auth, params, payload, and timeout into a request.

This separation keeps each component focused.

Another Architecture Decision
Should tests create headers?
headers = {
    "Authorization": "...",
    "Content-Type": "application/json"
}
❌ No.

Tests should focus on business intent, not transport details.

Instead:

user_client.create_user(user)

The framework handles everything else.

Enterprise Design

Our framework will look like this:

                 Tests
                   │
                   ▼
            Business Clients
     ┌─────────┼───────────┐
     ▼         ▼           ▼
 UserClient OrderClient PaymentClient
            │
            ▼
        APIClient
            │
     ┌──────┼──────────┐
     ▼      ▼          ▼
 RequestBuilder Logger SessionManager
     │
     ▼
AuthenticationManager
     │
     ▼
 TokenManager
     │
     ▼
 requests.Session
The Most Important Class

This class is going to determine whether our framework scales.

That class is:

APIClient

We are going to spend several lessons designing it properly.

Here's How We'll Build It
Version 1 (Simple)

Support:

GET
POST
PUT
PATCH
DELETE

That's all.

Version 2

Add:

Timeouts
Logging
Retries
Version 3

Add:

Authentication
Session reuse
Hooks
Version 4

Add:

Parallel execution
Correlation IDs
Metrics
Version 5

Add:

Plugins
Middleware
Request interceptors
Response interceptors

Exactly how mature frameworks evolve.

Our First Design Pattern

Today we'll introduce our first design pattern.

Facade Pattern

Tests see:

response = user_client.create_user(user)

They never see:

api_client.post(...)
request_builder(...)
token_manager(...)
logger(...)
session_manager(...)

The UserClient acts as a Facade, hiding the complexity of the underlying framework.

>>>>>>>>>>
🚀 Sprint 1 - Module 3
Session Management

Most tutorials do this:

response = requests.get(url)

or

requests.post(...)
requests.put(...)
requests.delete(...)

Looks harmless...

But under the hood, every call creates a new HTTP connection.

Imagine:

1000 Tests

↓

requests.get()

↓

Open TCP Connection

↓

Close TCP Connection

Now multiply that by 10,000 tests.

That's a lot of unnecessary overhead.

Enterprise Solution

We use requests.Session.

Test

↓

APIClient

↓

SessionManager

↓

requests.Session

↓

REST API

One session...

Many requests.

Benefits:

✅ Connection Pooling

✅ Cookie Persistence

✅ Default Headers

✅ Better Performance

But Wait...

Here's the first architecture discussion.

Should SessionManager be

Option 1
session = requests.Session()

Every APIClient creates one.

Option 2

Singleton Session

Entire framework shares one session.

Option 3

Session Factory

SessionManager

↓

Create Session

↓

Return Session

↓

Reuse Session
Which One Should We Choose?

My answer:

Option 3 (Session Factory)

Because later we can support:

Parallel workers
Multiple users
Multiple environments
Different authentication contexts

without changing the APIClient.

Why This Seems "Too Simple"

You may be thinking:

"This class is tiny."

Exactly.

A well-designed class doesn't need to be large.

Its responsibility is very focused:

Create a session.
Expose it.
Close it.

Nothing more.

Where This Class Will Grow

Later, SessionManager will handle:

Proxy configuration
SSL verification
Client certificates
Default headers
Connection pooling settings
Worker-specific sessions
Session metrics
Cleanup hooks

We'll extend it without changing the public interface.

Architecture Discussion

I also want your opinion on something.

Many frameworks use inheritance:

class UserClient(APIClient):
    ...

I prefer composition:

class UserClient:
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
Why?

Because composition gives us:

Easier testing (we can inject a mock APIClient)
Better flexibility
Lower coupling
Simpler evolution

This follows the principle:

Favor composition over inheritance.

It's one of the most useful object-oriented design principles you'll encounter.

>>>>>>>>
Sprint 1 - Module 4
APIClient (Core Engine)

This is the most important class in the entire framework.

If we design this correctly, everything else becomes much easier.

Step 0 - Design First

Before writing any code, let's answer four questions.

Responsibility

APIClient should:

Send HTTP requests.
Use the existing SessionManager.
Use the framework logger.
Read configuration values (timeout, base URL, default headers).

It should not:

Create tokens.
Validate responses.
Query databases.
Know business endpoints (Users, Orders, Payments).
Dependencies

APIClient depends on:

ConfigManager
SessionManager
FrameworkLogger
requests

Notice what is not here:

UserClient
Database
Validators

Keeping it independent makes it reusable.

Public API

For Version 1, we'll support:

get()
post()
put()
patch()
delete()

Internally, all of them will call a single private method:

_send_request()

This avoids duplicating code across five HTTP methods.

Future Growth

In later sprints, _send_request() will gain:

Authentication
Retry logic
Correlation IDs
Metrics
Request/response hooks
Middleware

The public API won't change.

Why _send_request()?

Imagine we didn't have it.

You would write logging, timeout handling, header handling, and request execution in all five methods.

That means five places to maintain.

Instead:

GET
POST
PUT
PATCH
DELETE
      │
      ▼
_send_request()

One implementation.

############################################
| Sprint   | Module                | Status |
| -------- | --------------------- | ------ |
| Sprint 1 | Project Setup         | ✅      |
| Sprint 1 | Configuration Manager | ✅      |
| Sprint 1 | Logger V1             | ✅      |
| Sprint 1 | Session Manager       | ✅      |
| Sprint 1 | APIClient V1          | ✅      |
#############################################

🏗️ Now We Enter Sprint 2

Sprint 1 was about Infrastructure.

Sprint 2 is about Business Layer.

This is where most frameworks start to look professional.

Sprint 2 Roadmap
Sprint 2

├── Endpoint Management
├── Business Clients
├── Response Validators
├── JSON Schema Validation
├── Request Models
└── Test Data Management
First Question

Where should endpoints live?

Many frameworks do this:

response = api_client.get("/users/2")
Problems

If tomorrow:

/users

becomes

/v2/users

You now have to search the entire project.

Not good.

Enterprise Approach

We'll create an Endpoint Catalog.

src/

endpoints/

    base_endpoints.py

    user_endpoints.py

    order_endpoints.py

    payment_endpoints.py

Notice something?

Earlier we didn't even have an endpoints package.

Now we do.

This is how frameworks evolve.

Why Separate Endpoints?

Imagine this:

Users

Orders

Payments

Invoices

Products

Notifications

Would you rather have:

500 endpoint strings

inside client classes?

Or:

UserEndpoints

OrderEndpoints

PaymentEndpoints

Much cleaner.

Example

Instead of

"/users"

we'll use

UserEndpoints.USERS

Instead of

f"/users/{id}"

we'll use

UserEndpoints.USER_BY_ID(user_id)

Notice...

No string concatenation inside tests.

Another Improvement

Instead of constants

USERS = "/users"

I'd rather write methods.

Example

class UserEndpoints:

    @staticmethod
    def list_users():
        return "/users"

    @staticmethod
    def get_user(user_id):
        return f"/users/{user_id}"

Why?

Because some endpoints become very dynamic.

Example

/users/{id}/orders/{orderId}/payments/{paymentId}

Methods make that much easier to manage.

Folder Structure
src/

endpoints/

    __init__.py

    user_endpoints.py
First Business Client

Now

src/

clients/

    user_client.py

Instead of

api_client.get(...)

the test becomes

user_client.get_user(2)

This is much closer to the language of the business.

What UserClient Should Do

Responsibilities:

Create User

Update User

Delete User

Get User

List Users

It should not:

Create tokens.
Validate responses.
Know about retries.
Manage sessions.

It simply maps business operations to HTTP calls.

Looking Ahead

Once UserClient is ready, adding another client becomes almost mechanical.

OrderClient

PaymentClient

InvoiceClient

All of them will reuse the same APIClient.

One Architecture Improvement I'd Like to Make

Now that Sprint 1 is complete, I'd like to start introducing interfaces (using Python abstract base classes) where they add value.

For example, every business client could implement a common contract for CRUD-style operations where appropriate.

That gives us:

Consistent APIs across clients.
Easier mocking in tests.
Better extensibility if different services expose similar resources.

We won't force abstraction everywhere, but we'll introduce it when it makes the design cleaner.

📌 Your Next Task (Sprint 2 - Module 1)

Let's start small.

Create a new package:
src/endpoints/

Inside it:

__init__.py
user_endpoints.py

In user_endpoints.py, implement a UserEndpoints class with methods like:

list_users()
get_user(user_id)
create_user()
update_user(user_id)
delete_user(user_id)

Keep it focused on endpoint construction only—no HTTP logic.

Once that's done, we'll build UserClient on top of it.

>>>>>>>

Sprint 2 - Module 3
Pytest Fixtures & Dependency Injection

This is one of the most important modules in the framework.

Once we finish this module:

No more creating ConfigManager() in every test
No more creating SessionManager() in every test
No more creating APIClient() in every test
No more repetitive setup code

Instead, pytest will automatically inject dependencies.

Current Situation

Every test looks like this:

config = ConfigManager("dev")

session_manager = SessionManager()

api_client = APIClient(config, session_manager)

user_client = UserClient(api_client)

response = user_client.get_user(user_id=2)

This is okay for 10 tests.

Imagine writing 5,000 tests.

Enterprise Solution

Our tests should look like this:

def test_get_user(user_client, requests_mock):

    requests_mock.get(
        "https://reqres.in/api/users/2",
        json={"id": 2},
        status_code=200,
    )

    response = user_client.get_user(user_id=2)

    assert response.status_code == 200

That's it.

Notice:

conftest.py

This file is automatically discovered by pytest.

No imports required.

Dependency Flow
ConfigManager
      │
      ▼
SessionManager
      │
      ▼
APIClient
      │
      ▼
UserClient
      │
      ▼
Tests

Exactly like dependency injection frameworks.

Pytest works like this:

Create Session

↓

yield

↓

Run Tests

↓

Cleanup

This ensures the session is closed automatically after all tests finish.

Fixture Scope

This is something every Senior SDET should know.

Scope	Lifetime
function	Every test
class	Every test class
module	Every test module
package	Every package (pytest 7+)
session	Entire execution

For us:

Fixture	Scope
Config	session
SessionManager	session
APIClient	session
UserClient	function
Why is UserClient function?

Because business clients may later contain:

request IDs
temporary state
authentication context
test-specific overrides

Creating a fresh client for each test keeps tests isolated.

Architecture Review

Let's evaluate this change like a pull request.

Before
Test

↓

Config

↓

Session

↓

API

↓

User

Repeated hundreds of times.

After
Fixtures

↓

Dependency Injection

↓

Tests

Tests focus only on business logic.

Future Benefits

When we add authentication, we'll only change one fixture.

>>>>>>>>>>>>

Sprint 2 - Module 4

Now we move to something that many automation frameworks never implement properly.

Request Models
Current
payload = {
    "name": "Raushan",
    "job": "SDET"
}

response = user_client.create_user(payload)

Works...

But after 300 APIs?

payload = {
    "customerName": "...",
    "customerId": "...",
    "customerType": "...",
    ...
}

Nobody remembers all keys.

Enterprise Approach

We'll use dataclasses.

Example:

from dataclasses import dataclass


@dataclass(slots=True)
class CreateUserRequest:
    name: str
    job: str

Now:

request = CreateUserRequest(
    name="Raushan",
    job="SDET"
)

response = user_client.create_user(request)

Much cleaner.

Why Dataclasses?

Benefits:

IDE autocomplete
Type checking
Readable code
Easier refactoring
Less typo-prone
Easier maintenance
Then...

We'll teach APIClient to automatically convert the dataclass into JSON.

So this:

CreateUserRequest(...)

becomes

{
  "name": "...",
  "job": "..."
}

without the test needing to know how.

Then Response Models

Instead of:

response.json()["name"]

you'll write:

user.name

This is exactly how many SDKs and enterprise frameworks work.

Then Validation

Instead of:

assert response.status_code == 200
assert response.json()["id"] == 2
assert response.json()["name"] == "Raushan"

you'll be able to write:

ResponseValidator(response)\
    .status_code(200)\
    .has_key("id")\
    .field("name").equals("Raushan")

or even stronger validation using response models and JSON Schema where appropriate.


