from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.gateways.postgresql.models.base import BaseORM


class ApplyORM(BaseORM):
    __tablename__ = "applies"

    org_id: Mapped[str] = mapped_column(ForeignKey("orgs.id", ondelete="CASCADE"), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    date: Mapped[datetime] = mapped_column(default=func.now(), server_default=func.now())
