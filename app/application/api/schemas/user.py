from pydantic import BaseModel, UUID4

from app.domain.entities.user import UserEntity


class UserSchema(BaseModel):
    id: UUID4
    name: str
    phone: str
    email: str
    experience: int
    skills: list[str]
    interests: list[str]

    @classmethod
    def from_entity(cls, entity: UserEntity) -> "UserSchema":
        return cls(
            id=entity.id,
            name=entity.name,
            phone=entity.phone,
            email=entity.email,
            experience=entity.experience,
            skills=entity.skills,
            interests=entity.interests
        )


class CreateUserSchema(BaseModel):
    email: str
    password: str

    name: str
    phone: str
    experience: int
    skills: list[str]
    interests: list[str]
