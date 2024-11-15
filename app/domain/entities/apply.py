from dataclasses import dataclass

from app.domain.entities.base import BaseEntity, IDMixin


@dataclass
class ApplyEntity(BaseEntity, IDMixin):
    org_id: str

    name: str
    phone: str
    email: str
    experience: int
    skills: list[str]
    interests: list[str]
