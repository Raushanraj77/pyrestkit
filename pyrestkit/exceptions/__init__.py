"""
Custom exceptions used throughout the API automation framework.
"""

from .api_exception import APIException
from .authentication_exception import AuthenticationException
from .configuration_exception import ConfigurationException
from .network_exception import NetworkException
from .response_exception import ResponseException
from .serialization_exception import SerializationException
from .validation_exception import ValidationException

__all__ = [
    "APIException",
    "AuthenticationException",
    "ConfigurationException",
    "NetworkException",
    "ResponseException",
    "SerializationException",
    "ValidationException",
]
