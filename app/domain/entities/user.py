from dataclasses import dataclass
from datetime import date

from app.domain.entities.base import BaseEntity, IDMixin


@dataclass
class UserEntity(BaseEntity, IDMixin):
    email: str
    hashed_password: str

    name: str
    phone: str
    sex: str
    birthdate: date
    experience: int
    professions: list[str]
    interests: list[str]
