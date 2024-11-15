from dataclasses import dataclass

from app.logic.exceptions.base import ObjectExistsException, ObjectNotFoundException


@dataclass(eq=False, frozen=True)
class UserExistsException(ObjectExistsException):
    email: str

    def __str__(self) -> str:
        return f"User with email `{self.email}` already exists"


@dataclass(eq=False, frozen=True)
class UserNotFoundException(ObjectNotFoundException):
    user_id: str | None = None
    email: str | None = None

    def __str__(self) -> str:
        return f"User with ID<{self.user_id}> | Email<{self.email}> not found"
