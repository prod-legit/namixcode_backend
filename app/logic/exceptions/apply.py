from dataclasses import dataclass

from app.logic.exceptions.base import ObjectExistsException, ObjectNotFoundException


@dataclass(eq=False, frozen=True)
class ApplyExistsException(ObjectExistsException):
    user_id: str
    org_id: str

    def __str__(self) -> str:
        return f"Apply of user<{self.user_id}> for org<{self.org_id}> already exists"


@dataclass(eq=False, frozen=True)
class ApplyNotFoundException(ObjectNotFoundException):
    user_id: str
    org_id: str

    def __str__(self) -> str:
        return f"Apply of user<{self.user_id}> for org<{self.org_id}> not found"
