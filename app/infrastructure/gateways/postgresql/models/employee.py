from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.gateways.postgresql.models.base import BaseORM, IDMixin

if TYPE_CHECKING:
    from app.infrastructure.gateways.postgresql.models import OrgORM
    from app.infrastructure.gateways.postgresql.models import UserORM


class EmployeeORM(BaseORM, IDMixin):
    __tablename__ = "employees"

    org_id: Mapped[str] = mapped_column(ForeignKey("orgs.id", ondelete="CASCADE"))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    head_id: Mapped[str | None] = mapped_column(ForeignKey("employees.id", ondelete="CASCADE"), nullable=True)
    date: Mapped[datetime] = mapped_column(default=func.now(), server_default=func.now())

    org: Mapped["OrgORM"] = relationship(back_populates="employees")
    user: Mapped["UserORM"] = relationship(back_populates="employments")
    head: Mapped["EmployeeORM"] = relationship(back_populates="slaves", remote_side="EmployeeORM.id")
    slaves: Mapped[list["EmployeeORM"]] = relationship(back_populates="head")
