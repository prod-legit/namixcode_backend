from pydantic import BaseModel, UUID4, EmailStr

from app.domain.entities.org import OrgEntity


class OrgSchema(BaseModel):
    id: UUID4
    email: EmailStr
    name: str
    description: str
    location: str
    logo: str
    foundation_year: int
    scope: str

    @classmethod
    def from_entity(cls, entity: OrgEntity) -> "OrgSchema":
        return cls(
            id=entity.id,
            name=entity.name,
            email=entity.email,
            description=entity.description,
            location=entity.location,
            logo=entity.logo,
            foundation_year=entity.foundation_year,
            scope=entity.scope
        )


class CreateOrgSchema(BaseModel):
    email: EmailStr
    password: str

    name: str
    description: str
    location: str
    logo: str
    foundation_year: int
    scope: str
