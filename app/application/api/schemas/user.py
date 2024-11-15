from datetime import date

from pydantic import BaseModel, UUID4

from app.domain.entities.user import UserEntity
from app.domain.values.user import SexEnum


class UserSchema(BaseModel):
    id: UUID4
    name: str
    phone: str
    sex: SexEnum
    birthdate: date
    email: str
    experience: int
    professions: list[str]
    interests: list[str]

    @classmethod
    def from_entity(cls, entity: UserEntity) -> "UserSchema":
        return cls(
            id=entity.id,
            name=entity.name,
            phone=entity.phone,
            sex=SexEnum(entity.sex),
            birthdate=entity.birthdate,
            email=entity.email,
            experience=entity.experience,
            professions=entity.professions,
            interests=entity.interests
        )


class CreateUserSchema(BaseModel):
    email: str
    password: str

    name: str
    phone: str
    sex: SexEnum
    birthdate: date
    experience: int
    professions: list[str]
    interests: list[str]
