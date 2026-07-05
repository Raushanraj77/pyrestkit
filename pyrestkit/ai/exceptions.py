class AIError(Exception):
    """
    Base exception for AI integration failures.
    """


class AIConfigurationError(AIError):
    """
    Raised when AI provider configuration is missing or invalid.
    """


class AIProviderError(AIError):
    """
    Raised when an AI provider request fails.
    """


class AIResponseParseError(AIError):
    """
    Raised when an AI response cannot be parsed into the expected shape.
    """
