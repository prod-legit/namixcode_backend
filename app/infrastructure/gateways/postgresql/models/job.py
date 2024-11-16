from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.gateways.postgresql.models.base import BaseORM, IDMixin

if TYPE_CHECKING:
    from app.infrastructure.gateways.postgresql.models import OrgORM, ApplyORM, EmployeeORM


class JobORM(BaseORM, IDMixin):
    __tablename__ = "jobs"

    org_id: Mapped[str] = mapped_column(ForeignKey("orgs.id", ondelete="CASCADE"))
    title: Mapped[str]
    description: Mapped[str]
    pay: Mapped[str]

    org: Mapped["OrgORM"] = relationship(back_populates="jobs")
    applies: Mapped["ApplyORM"] = relationship(back_populates="job")
    employees: Mapped["EmployeeORM"] = relationship(back_populates="job")
