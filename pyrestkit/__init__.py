"""
PyRestKit

Modern Python REST API Automation Toolkit.
"""

from pyrestkit.auth.strategies.api_key_auth import ApiKeyAuth
from pyrestkit.auth.strategies.basic_auth import BasicAuth
from pyrestkit.auth.strategies.bearer_auth import BearerAuth
from pyrestkit.clients.user_client import UserClient
from pyrestkit.config.config import ConfigManager
from pyrestkit.core.api_client import APIClient
from pyrestkit.core.session_manager import SessionManager
from pyrestkit.factories.user_factory import UserFactory
from pyrestkit.models.request.create_user_request import CreateUserRequest
from pyrestkit.models.request.update_user_request import UpdateUserRequest
from pyrestkit.validators.response_validator import ResponseValidator
from pyrestkit.validators.schema_validator import SchemaValidator

__version__ = "1.1.0"

__all__ = [
    "APIClient",
    "SessionManager",
    "ConfigManager",
    "BearerAuth",
    "BasicAuth",
    "ApiKeyAuth",
    "UserClient",
    "CreateUserRequest",
    "UpdateUserRequest",
    "ResponseValidator",
    "SchemaValidator",
    "UserFactory",
]
