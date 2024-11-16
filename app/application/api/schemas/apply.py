from datetime import datetime

from pydantic import BaseModel, UUID4

from app.application.api.schemas.org import OrgSchema
from app.application.api.schemas.user import UserSchema
from app.domain.entities.apply import ApplyEntity


class ApplySchema(BaseModel):
    org: OrgSchema
    user: UserSchema
    date: datetime

    @classmethod
    def from_entity(cls, entity: ApplyEntity) -> "ApplySchema":
        return cls(
            org=OrgSchema.from_entity(entity.org),
            user=UserSchema.from_entity(entity.user),
            date=entity.date,
        )


class CreateApplySchema(BaseModel):
    org_id: UUID4


class AcceptApplySchema(BaseModel):
    head_id: UUID4 | None = None
