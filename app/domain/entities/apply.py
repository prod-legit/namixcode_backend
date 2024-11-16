from dataclasses import dataclass, field
from datetime import datetime

from app.domain.entities.base import BaseEntity, IDMixin
from app.domain.entities.org import OrgEntity
from app.domain.entities.user import UserEntity


@dataclass
class ApplyEntity(BaseEntity, IDMixin):
    org: OrgEntity
    user: UserEntity
    date: datetime = field(default_factory=datetime.now, kw_only=True)
