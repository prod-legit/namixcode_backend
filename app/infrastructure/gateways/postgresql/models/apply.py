from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.gateways.postgresql.models.base import BaseORM, IDMixin

if TYPE_CHECKING:
    from app.infrastructure.gateways.postgresql.models import OrgORM, UserORM


class ApplyORM(BaseORM, IDMixin):
    __tablename__ = "applies"

    org_id: Mapped[str] = mapped_column(ForeignKey("orgs.id", ondelete="CASCADE"))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    date: Mapped[datetime] = mapped_column(default=func.now(), server_default=func.now())

    org: Mapped["OrgORM"] = relationship(back_populates="applies")
    user: Mapped["UserORM"] = relationship(backref="applies")

    UniqueConstraint("org_id", "user_id")
