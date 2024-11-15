from dataclasses import dataclass

from app.logic.exceptions.base import ObjectExistsException, ObjectNotFoundException


@dataclass(eq=False, frozen=True)
class OrgExistsException(ObjectExistsException):
    email: str

    def __str__(self) -> str:
        return f"Organization with email `{self.email}` already exists"


@dataclass(eq=False, frozen=True)
class OrgNotFoundException(ObjectNotFoundException):
    org_id: str | None = None
    email: str | None = None

    def __str__(self) -> str:
        return f"Organization with ID<{self.org_id}> | Email<{self.email}> not found"
