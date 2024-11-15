from dataclasses import dataclass

from app.domain.entities.base import BaseEntity, IDMixin


@dataclass
class UserEntity(BaseEntity, IDMixin):
    email: str
    hashed_password: str

    name: str
    phone: str
    experience: int
    skills: list[str]
    interests: list[str]
