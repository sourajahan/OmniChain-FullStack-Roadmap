class DomainError(Exception):
    """Base class for domain-level errors."""


class EmailAlreadyExistsError(DomainError):
    """Raised when registering with an email that already exists."""


class InvalidCredentialsError(DomainError):
    """Raised when email or password is invalid, or user is inactive."""


class InvalidRefreshTokenError(DomainError):
    """Raised when a refresh token is missing, unknown, or expired."""


class TokenReuseDetectedError(DomainError):
    """Raised when a revoked refresh token is reused (replay attack)."""
