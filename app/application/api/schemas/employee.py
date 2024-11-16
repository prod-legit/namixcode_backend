from datetime import datetime

from pydantic import BaseModel, UUID4

from app.application.api.schemas.user import UserSchema
from app.domain.entities.employee import EmployeeEntity


class EmployeeSchema(BaseModel):
    org_id: UUID4
    user: UserSchema
    head: "EmployeeSchema | None"
    slaves: list["EmployeeSchema"]
    date: datetime

    @classmethod
    def from_entity(cls, entity: EmployeeEntity) -> "EmployeeSchema":
        return cls(
            org_id=entity.org.id,
            user=UserSchema.from_entity(entity.user),
            head=EmployeeSchema.from_entity(entity.head) if entity.head else None,
            slaves=[EmployeeSchema.from_entity(slave) for slave in entity.slaves],
            date=entity.date
        )


class ApplyEmployeeSchema(BaseModel):
    user_id: UUID4
