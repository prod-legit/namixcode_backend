from dataclasses import dataclass, field
from datetime import datetime

from app.domain.entities.base import BaseEntity, IDMixin


@dataclass
class ApplyEntity(BaseEntity, IDMixin):
    org_id: str
    user_id: str
    date: datetime = field(default_factory=datetime.now, kw_only=True)
