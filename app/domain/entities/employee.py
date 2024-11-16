from dataclasses import dataclass, field
from datetime import datetime

from app.domain.entities.base import BaseEntity, IDMixin
from app.domain.entities.org import OrgEntity
from app.domain.entities.user import UserEntity


@dataclass
class EmployeeEntity(BaseEntity, IDMixin):
    org: OrgEntity
    user: UserEntity
    head: "EmployeeEntity | None"
    slaves: list["EmployeeEntity"] = field(default_factory=list)
    date: datetime = field(default_factory=datetime.now, kw_only=True)
