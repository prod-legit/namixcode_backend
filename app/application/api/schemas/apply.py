from pydantic import BaseModel, UUID4

from app.domain.entities.apply import ApplyEntity


class ApplySchema(BaseModel):
    id: UUID4
    org_id: UUID4
    name: str
    phone: str
    email: str
    experience: int
    skills: list[str]
    interests: list[str]

    @classmethod
    def from_entity(cls, entity: ApplyEntity) -> "ApplySchema":
        return cls(
            id=entity.id,
            org_id=entity.org_id,
            name=entity.name,
            phone=entity.phone,
            email=entity.email,
            experience=entity.experience,
            skills=entity.skills,
            interests=entity.interests
        )


class CreateApplySchema(BaseModel):
    org_id: UUID4
    name: str
    phone: str
    email: str
    experience: int
    skills: list[str]
    interests: list[str]
