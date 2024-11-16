from pydantic import BaseModel, UUID4

from app.application.api.schemas.org import OrgSchema
from app.domain.entities.job import JobEntity


class JobSchema(BaseModel):
    id: UUID4
    org: OrgSchema
    title: str
    description: str
    pay: str

    @classmethod
    def from_entity(cls, entity: JobEntity) -> "JobSchema":
        return cls(
            id=entity.id,
            org=OrgSchema.from_entity(entity.org),
            title=entity.title,
            description=entity.description,
            pay=entity.pay
        )


class CreateJobSchema(BaseModel):
    title: str
    description: str
    pay: str
