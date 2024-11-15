from abc import abstractmethod, ABC
from dataclasses import dataclass

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.entities.apply import ApplyEntity
from app.infrastructure.gateways.postgresql.mappers.apply import ApplyORMMapper
from app.infrastructure.gateways.postgresql.models import ApplyORM


@dataclass(eq=False, frozen=True)
class IApplyRepository(ABC):
    @abstractmethod
    async def create(self, entity: ApplyEntity) -> None: ...

    @abstractmethod
    async def get(self, id_: str) -> ApplyEntity | None: ...

    @abstractmethod
    async def get_by_org_id(self, org_id: str) -> list[ApplyEntity]: ...

    @abstractmethod
    async def delete(self, id_: str) -> None: ...


@dataclass(eq=False, frozen=True)
class SQLAlchemyApplyRepository(IApplyRepository):
    session: AsyncSession

    async def create(self, entity: ApplyEntity) -> None:
        db_apply = ApplyORMMapper.from_entity(entity)
        self.session.add(db_apply)

    async def get(self, id_: str) -> ApplyEntity | None:
        stmt = (
            select(ApplyORM)
            .where(ApplyORM.id == id_)
            .options(
                selectinload(ApplyORM.skills),
                selectinload(ApplyORM.interests)
            )
        )
        if db_apply := await self.session.scalar(stmt):
            return ApplyORMMapper.to_entity(db_apply)

    async def get_by_org_id(self, org_id: str) -> list[ApplyEntity]:
        stmt = (
            select(ApplyORM)
            .where(ApplyORM.org_id == org_id)
            .options(
                selectinload(ApplyORM.skills),
                selectinload(ApplyORM.interests)
            )
        )
        db_applies = await self.session.scalars(stmt)
        return [ApplyORMMapper.to_entity(db_apply) for db_apply in db_applies]

    async def delete(self, id_: str) -> None:
        stmt = delete(ApplyORM).where(ApplyORM.id == id_)
        await self.session.execute(stmt)
