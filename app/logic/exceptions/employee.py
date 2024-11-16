from dataclasses import dataclass

from app.logic.exceptions.base import ObjectExistsException, ObjectNotFoundException


@dataclass(eq=False, frozen=True)
class EmployeeExistsException(ObjectExistsException):
    user_id: str
    org_id: str

    def __str__(self) -> str:
        return f"Employee user<{self.user_id}> for org<{self.org_id}> already exists"


@dataclass(eq=False, frozen=True)
class EmployeeNotFoundException(ObjectNotFoundException):
    employee_id: str

    def __str__(self) -> str:
        return f"Employee with ID<{self.employee_id}> not found"
