from dataclasses import dataclass

from app.domain.entities.base import BaseEntity, IDMixin


@dataclass
class ApplyEntity(BaseEntity, IDMixin):
    name: str
    phone: str
    email: str
    experience: int
    skills: list[str]
    interests: list[str]
