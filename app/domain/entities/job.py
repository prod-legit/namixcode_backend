from dataclasses import dataclass

from app.domain.entities.base import BaseEntity, IDMixin
from app.domain.entities.org import OrgEntity


@dataclass
class JobEntity(BaseEntity, IDMixin):
    org: OrgEntity
    title: str
    description: str
    pay: str
