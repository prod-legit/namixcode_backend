from datetime import datetime

from pydantic import BaseModel, UUID4

from app.application.api.schemas.job import JobSchema
from app.application.api.schemas.user import UserSchema
from app.domain.entities.apply import ApplyEntity


class ApplySchema(BaseModel):
    job: JobSchema
    user: UserSchema
    date: datetime

    @classmethod
    def from_entity(cls, entity: ApplyEntity) -> "ApplySchema":
        return cls(
            job=JobSchema.from_entity(entity.job),
            user=UserSchema.from_entity(entity.user),
            date=entity.date,
        )


class CreateApplySchema(BaseModel):
    job_id: UUID4


class AcceptApplySchema(BaseModel):
    job_id: UUID4
    head_id: UUID4 | None = None
