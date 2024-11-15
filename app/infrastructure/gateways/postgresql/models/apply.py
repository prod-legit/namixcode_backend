from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.gateways.postgresql.models.base import BaseORM, IDMixin


class UserSkillORM(BaseORM, IDMixin):
    __tablename__ = "user_skills"

    apply_id: Mapped[str] = mapped_column(ForeignKey("applies.id", ondelete="CASCADE"))
    skill: Mapped[str]


class UserInterestORM(BaseORM, IDMixin):
    __tablename__ = "user_interests"

    apply_id: Mapped[str] = mapped_column(ForeignKey("applies.id", ondelete="CASCADE"))
    interest: Mapped[str]


class ApplyORM(BaseORM, IDMixin):
    __tablename__ = "applies"

    org_id: Mapped[str] = mapped_column(ForeignKey("orgs.id", ondelete="CASCADE"))
    name: Mapped[str]
    phone: Mapped[str]
    email: Mapped[str]
    experience: Mapped[int]

    skills: Mapped[list[UserSkillORM]] = relationship(UserSkillORM, backref="apply")
    interests: Mapped[list[UserInterestORM]] = relationship(UserInterestORM, backref="apply")
