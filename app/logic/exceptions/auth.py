from dataclasses import dataclass
from datetime import datetime
from typing import Any

from app.logic.exceptions.base import LogicException


@dataclass(eq=False, frozen=True)
class AuthException(LogicException):
    def __str__(self) -> str:
        return "A error occurred during the authorization"


@dataclass(eq=False, frozen=True)
class EmptyAuthTokenException(AuthException):
    def __str__(self) -> str:
        return "The token has not been provided"


@dataclass(eq=False, frozen=True)
class InvalidAuthTokenException(AuthException):
    token: str

    def __str__(self) -> str:
        return f"The token `{self.token} is invalid`"


@dataclass(eq=False, frozen=True)
class InvalidJWTPayloadException(InvalidAuthTokenException):
    payload: dict[str, Any]

    def __str__(self) -> str:
        return f"The token `{self.token} has invalid payload`"


@dataclass(eq=False, frozen=True)
class AuthTokenExpired(InvalidAuthTokenException):
    expired_at: datetime

    def __str__(self) -> str:
        return f"The token `{self.token}` has expired at {self.expired_at}"


@dataclass(eq=False, frozen=True)
class InvalidAuthCredentialsException(AuthException):
    email: str
    password: str

    def __str__(self) -> str:
        return f"Email or password is invalid"
