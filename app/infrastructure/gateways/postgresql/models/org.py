from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.gateways.postgresql.models.base import BaseORM, IDMixin

if TYPE_CHECKING:
    from app.infrastructure.gateways.postgresql.models import EmployeeORM, ApplyORM


class OrgORM(BaseORM, IDMixin):
    __tablename__ = "orgs"

    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

    name: Mapped[str]
    description: Mapped[str]
    location: Mapped[str]
    logo: Mapped[str]
    foundation_year: Mapped[int]
    scope: Mapped[str]

    employees: Mapped[list["EmployeeORM"]] = relationship(back_populates="org")
    applies: Mapped[list["ApplyORM"]] = relationship(back_populates="org")
