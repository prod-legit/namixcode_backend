from dataclasses import dataclass

from app.logic.exceptions.base import ObjectExistsException, ObjectNotFoundException


@dataclass(eq=False, frozen=True)
class ApplyExistsException(ObjectExistsException):
    user_id: str
    job_id: str

    def __str__(self) -> str:
        return f"Apply of user<{self.user_id}> for job<{self.job_id}> already exists"


@dataclass(eq=False, frozen=True)
class ApplyNotFoundException(ObjectNotFoundException):
    user_id: str
    job_id: str

    def __str__(self) -> str:
        return f"Apply of user<{self.user_id}> for job<{self.job_id}> not found"
