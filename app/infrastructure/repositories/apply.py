from abc import abstractmethod, ABC
from dataclasses import dataclass

from sqlalchemy import select, delete, exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.domain.entities.apply import ApplyEntity
from app.infrastructure.gateways.postgresql.mappers.apply import ApplyORMMapper
from app.infrastructure.gateways.postgresql.models import ApplyORM, UserORM, JobORM


@dataclass(eq=False, frozen=True)
class IApplyRepository(ABC):
    @abstractmethod
    async def create(self, entity: ApplyEntity) -> None: ...

    @abstractmethod
    async def check_exists(self, job_id: str, user_id: str) -> bool: ...

    @abstractmethod
    async def get(self, job_id: str, user_id: str) -> ApplyEntity | None: ...

    @abstractmethod
    async def get_by_user_id(self, id_: str) -> list[ApplyEntity]: ...

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

    async def check_exists(self, job_id: str, user_id: str) -> bool:
        stmt = (
            select(exists(ApplyORM))
            .where(
                ApplyORM.job_id == job_id,
                ApplyORM.user_id == user_id
            )
        )
        return await self.session.scalar(stmt)

    async def get(self, job_id: str, user_id: str) -> ApplyEntity | None:
        stmt = (
            select(ApplyORM)
            .where(
                ApplyORM.job_id == job_id,
                ApplyORM.user_id == user_id
            )
            .options(
                joinedload(ApplyORM.job).joinedload(JobORM.org),
                joinedload(ApplyORM.user).selectinload(UserORM.interests),
                joinedload(ApplyORM.user).selectinload(UserORM.professions)
            )
        )
        if db_apply := await self.session.scalar(stmt):
            return ApplyORMMapper.to_entity(db_apply)

    async def get_by_user_id(self, user_id: str) -> list[ApplyEntity]:
        stmt = (
            select(ApplyORM)
            .where(ApplyORM.user_id == user_id)
            .options(
                joinedload(ApplyORM.job).joinedload(JobORM.org),
                joinedload(ApplyORM.user).selectinload(UserORM.interests),
                joinedload(ApplyORM.user).selectinload(UserORM.professions))
        )
        db_applies = await self.session.scalars(stmt)
        return [ApplyORMMapper.to_entity(db_apply) for db_apply in db_applies]

    async def get_by_org_id(self, org_id: str) -> list[ApplyEntity]:
        stmt = (
            select(ApplyORM)
            .where(JobORM.org_id == org_id)
            .options(
                joinedload(ApplyORM.job).joinedload(JobORM.org),
                joinedload(ApplyORM.user).selectinload(UserORM.interests),
                joinedload(ApplyORM.user).selectinload(UserORM.professions))
        )
        db_applies = await self.session.scalars(stmt)
        return [ApplyORMMapper.to_entity(db_apply) for db_apply in db_applies]

    async def delete(self, id_: str) -> None:
        stmt = delete(ApplyORM).where(ApplyORM.id == id_)
        await self.session.execute(stmt)
