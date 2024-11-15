from datetime import datetime

from pydantic import BaseModel, UUID4

from app.domain.entities.apply import ApplyEntity


class ApplySchema(BaseModel):
    org_id: UUID4
    user_id: UUID4
    date: datetime

    @classmethod
    def from_entity(cls, entity: ApplyEntity) -> "ApplySchema":
        return cls(
            org_id=entity.org_id,
            user_id=entity.user_id,
            date=entity.date,
        )


class CreateApplySchema(BaseModel):
    org_id: UUID4
