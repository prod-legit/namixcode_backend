from dataclasses import dataclass

from app.domain.entities.base import BaseEntity, IDMixin


@dataclass
class OrgEntity(BaseEntity, IDMixin):
    email: str
    hashed_password: str

    name: str
    description: str
    location: str
    logo: str
    foundation_year: int
    scope: str
