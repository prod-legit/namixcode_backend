from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.gateways.postgresql.models.base import BaseORM, IDMixin

if TYPE_CHECKING:
    from app.infrastructure.gateways.postgresql.models import JobORM, UserORM


class ApplyORM(BaseORM, IDMixin):
    __tablename__ = "applies"

    job_id: Mapped[str] = mapped_column(ForeignKey("jobs.id", ondelete="CASCADE"))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    date: Mapped[datetime] = mapped_column(default=func.now(), server_default=func.now())

    job: Mapped["JobORM"] = relationship(back_populates="applies")
    user: Mapped["UserORM"] = relationship(backref="applies")

    UniqueConstraint("job_id", "user_id")
