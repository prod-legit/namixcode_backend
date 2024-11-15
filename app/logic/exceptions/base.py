from dataclasses import dataclass

from app.domain.exceptions.base import AppException


@dataclass(eq=False, frozen=True)
class LogicException(AppException):
    def __str__(self) -> str:
        return "A logic error occurred during the application execution"


@dataclass(eq=False, frozen=True)
class EmptySearchParamsException(AppException):
    def __str__(self) -> str:
        return "Empty search parameters"


@dataclass(eq=False, frozen=True)
class ObjectNotFoundException(LogicException):
    def __str__(self) -> str:
        return "Object not found"


@dataclass(eq=False, frozen=True)
class ObjectExistsException(LogicException):
    def __str__(self) -> str:
        return "Object already exists"


@dataclass(eq=False, frozen=True)
class AccessForbiddenException(LogicException):
    def __str__(self) -> str:
        return "Access forbidden"
