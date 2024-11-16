from dataclasses import dataclass

from app.logic.exceptions.base import ObjectNotFoundException


@dataclass(eq=False, frozen=True)
class JobNotFoundException(ObjectNotFoundException):
    job_id: str

    def __str__(self) -> str:
        return f"Job with ID<{self.job_id}> not found"
