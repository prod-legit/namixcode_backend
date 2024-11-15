from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.gateways.postgresql.models.base import BaseORM, IDMixin


class UserProfessionORM(BaseORM, IDMixin):
    __tablename__ = "user_professions"

    apply_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    profession: Mapped[str]


class UserInterestORM(BaseORM, IDMixin):
    __tablename__ = "user_interests"

    apply_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    interest: Mapped[str]


class UserORM(BaseORM, IDMixin):
    __tablename__ = "users"

    email: Mapped[str]
    hashed_password: Mapped[str]

    name: Mapped[str]
    phone: Mapped[str]
    sex: Mapped[str]
    birthdate: Mapped[date]
    experience: Mapped[int]

    professions: Mapped[list[UserProfessionORM]] = relationship(UserProfessionORM, backref="user")
    interests: Mapped[list[UserInterestORM]] = relationship(UserInterestORM, backref="user")
