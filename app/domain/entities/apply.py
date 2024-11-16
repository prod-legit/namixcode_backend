from dataclasses import dataclass, field
from datetime import datetime

from app.domain.entities.base import BaseEntity, IDMixin
from app.domain.entities.job import JobEntity
from app.domain.entities.user import UserEntity


@dataclass
class ApplyEntity(BaseEntity, IDMixin):
    job: JobEntity
    user: UserEntity
    date: datetime = field(default_factory=datetime.now, kw_only=True)
