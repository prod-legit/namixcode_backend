from abc import abstractmethod, ABC
from dataclasses import dataclass

from sqlalchemy import select, delete, exists
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.org import OrgEntity
from app.infrastructure.gateways.postgresql.mappers.org import OrgORMMapper
from app.infrastructure.gateways.postgresql.models import OrgORM


@dataclass(eq=False, frozen=True)
class IOrgRepository(ABC):
    @abstractmethod
    async def create(self, entity: OrgEntity) -> None: ...

    @abstractmethod
    async def get(self, id_: str) -> OrgEntity | None: ...

    @abstractmethod
    async def get_all(self) -> list[OrgEntity]: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> OrgEntity | None: ...

    @abstractmethod
    async def check_exists_by_email(self, email: str) -> bool: ...

    @abstractmethod
    async def delete(self, id_: str) -> None: ...


@dataclass(eq=False, frozen=True)
class SQLAlchemyOrgRepository(IOrgRepository):
    session: AsyncSession

    async def create(self, entity: OrgEntity) -> None:
        db_org = OrgORMMapper.from_entity(entity)
        self.session.add(db_org)

    async def get(self, id_: str) -> OrgEntity | None:
        stmt = select(OrgORM).where(OrgORM.id == id_)
        if db_org := await self.session.scalar(stmt):
            return OrgORMMapper.to_entity(db_org)

    async def get_all(self) -> list[OrgEntity]:
        db_orgs = await self.session.scalars(select(OrgORM))
        return [OrgORMMapper.to_entity(db_org) for db_org in db_orgs]

    async def get_by_email(self, email: str) -> OrgEntity | None:
        stmt = select(OrgORM).where(OrgORM.email == email)
        if db_org := await self.session.scalar(stmt):
            return OrgORMMapper.to_entity(db_org)

    async def check_exists_by_email(self, email: str) -> bool:
        stmt = select(exists(OrgORM)).where(OrgORM.email == email)
        return await self.session.scalar(stmt)

    async def delete(self, id_: str) -> None:
        stmt = delete(OrgORM).where(OrgORM.id == id_)
        await self.session.execute(stmt)
