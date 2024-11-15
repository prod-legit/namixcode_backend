from dataclasses import dataclass

from app.logic.exceptions.base import ObjectExistsException, ObjectNotFoundException


@dataclass(eq=False, frozen=True)
class OrgExistsException(ObjectExistsException):
    email: str

    def __str__(self) -> str:
        return f"Organization with email `{self.email}` already exists"


@dataclass(eq=False, frozen=True)
class OrgNotFoundException(ObjectNotFoundException):
    search_params: dict

    def __str__(self) -> str:
        return "Organization with this search parameters not found"
