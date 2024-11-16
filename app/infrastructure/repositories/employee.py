from abc import abstractmethod, ABC
from dataclasses import dataclass

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.domain.entities.employee import EmployeeEntity
from app.infrastructure.gateways.postgresql.mappers.employee import EmployeeORMMapper
from app.infrastructure.gateways.postgresql.models import EmployeeORM, UserORM


@dataclass(eq=False, frozen=True)
class IEmployeeRepository(ABC):
    @abstractmethod
    async def create(self, entity: EmployeeEntity) -> None: ...

    @abstractmethod
    async def check_exists(self, org_id: str, user_id: str) -> bool: ...

    @abstractmethod
    async def get(self, org_id: str, user_id: str) -> EmployeeEntity | None: ...

    @abstractmethod
    async def get_by_user_id(self, id_: str) -> list[EmployeeEntity]: ...

    @abstractmethod
    async def get_by_org_id(self, org_id: str) -> list[EmployeeEntity]: ...

    @abstractmethod
    async def delete(self, org_id: str, user_id: str) -> None: ...


@dataclass(eq=False, frozen=True)
class SQLAlchemyEmployeeRepository(IEmployeeRepository):
    session: AsyncSession

    async def create(self, entity: EmployeeEntity) -> None:
        db_employee = EmployeeORMMapper.from_entity(entity)
        self.session.add(db_employee)

    async def check_exists(self, org_id: str, user_id: str) -> bool:
        stmt = (
            select(select(EmployeeORM))
            .where(
                EmployeeORM.org_id == org_id,
                EmployeeORM.user_id == user_id
            )
        )
        return await self.session.scalar(stmt)

    async def get(self, org_id: str, user_id: str) -> EmployeeEntity | None:
        stmt = (
            select(EmployeeORM)
            .where(
                EmployeeORM.org_id == org_id,
                EmployeeORM.user_id == user_id
            )
            .options(
                joinedload(EmployeeORM.org),
                joinedload(EmployeeORM.user).selectinload(UserORM.professions),
                joinedload(EmployeeORM.user).selectinload(UserORM.interests),
                joinedload(EmployeeORM.head).joinedload(EmployeeORM.user).selectinload(UserORM.professions),
                joinedload(EmployeeORM.head).joinedload(EmployeeORM.user).selectinload(UserORM.interests),
                selectinload(EmployeeORM.slaves).joinedload(EmployeeORM.user).selectinload(UserORM.professions),
                selectinload(EmployeeORM.slaves).joinedload(EmployeeORM.user).selectinload(UserORM.interests),
            )
        )
        if db_employee := await self.session.scalar(stmt):
            return EmployeeORMMapper.to_entity(db_employee)

    async def get_by_user_id(self, user_id: str) -> list[EmployeeEntity]:
        stmt = (
            select(EmployeeORM)
            .where(EmployeeORM.user_id == user_id)
            .options(
                joinedload(EmployeeORM.org),
                joinedload(EmployeeORM.user).selectinload(UserORM.professions),
                joinedload(EmployeeORM.user).selectinload(UserORM.interests),
                joinedload(EmployeeORM.head).joinedload(EmployeeORM.user).selectinload(UserORM.professions),
                joinedload(EmployeeORM.head).joinedload(EmployeeORM.user).selectinload(UserORM.interests),
                selectinload(EmployeeORM.slaves).joinedload(EmployeeORM.user).selectinload(UserORM.professions),
                selectinload(EmployeeORM.slaves).joinedload(EmployeeORM.user).selectinload(UserORM.interests),
            )
        )
        db_applies = await self.session.scalars(stmt)
        return [EmployeeORMMapper.to_entity(db_employee) for db_employee in db_applies]

    async def get_by_org_id(self, org_id: str) -> list[EmployeeEntity]:
        stmt = (
            select(EmployeeORM)
            .where(EmployeeORM.org_id == org_id)
            .options(
                joinedload(EmployeeORM.org),
                joinedload(EmployeeORM.user).selectinload(UserORM.professions),
                joinedload(EmployeeORM.user).selectinload(UserORM.interests),
                joinedload(EmployeeORM.head).joinedload(EmployeeORM.user).selectinload(UserORM.professions),
                joinedload(EmployeeORM.head).joinedload(EmployeeORM.user).selectinload(UserORM.interests),
                selectinload(EmployeeORM.slaves).joinedload(EmployeeORM.user).selectinload(UserORM.professions),
                selectinload(EmployeeORM.slaves).joinedload(EmployeeORM.user).selectinload(UserORM.interests),
            )
        )
        db_applies = await self.session.scalars(stmt)
        return [EmployeeORMMapper.to_entity(db_employee) for db_employee in db_applies]

    async def delete(self, org_id: str, user_id: str) -> None:
        stmt = delete(EmployeeORM).where(
            EmployeeORM.org_id == org_id,
            EmployeeORM.user_id == user_id
        )
        await self.session.execute(stmt)
