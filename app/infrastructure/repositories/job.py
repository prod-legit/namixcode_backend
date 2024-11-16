from abc import abstractmethod, ABC
from dataclasses import dataclass

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.domain.entities.job import JobEntity
from app.infrastructure.gateways.postgresql.mappers.job import JobORMMapper
from app.infrastructure.gateways.postgresql.models import JobORM


@dataclass(eq=False, frozen=True)
class IJobRepository(ABC):
    @abstractmethod
    async def create(self, entity: JobEntity) -> None: ...

    @abstractmethod
    async def get(self, id_: str) -> JobEntity | None: ...

    @abstractmethod
    async def get_by_org_id(self, org_id: str) -> list[JobEntity]: ...

    @abstractmethod
    async def get_all(self) -> list[JobEntity]: ...

    @abstractmethod
    async def delete(self, id_: str) -> None: ...


@dataclass(eq=False, frozen=True)
class SQLAlchemyJobRepository(IJobRepository):
    session: AsyncSession

    async def create(self, entity: JobEntity) -> None:
        db_employee = JobORMMapper.from_entity(entity)
        self.session.add(db_employee)

    async def get(self, id_: str) -> JobEntity | None:
        stmt = select(JobORM).where(JobORM.id == id_).options(joinedload(JobORM.org))
        if db_jon := await self.session.scalar(stmt):
            return JobORMMapper.to_entity(db_jon)

    async def get_by_org_id(self, org_id: str) -> list[JobEntity]:
        stmt = (
            select(JobORM)
            .where(JobORM.org_id == org_id)
            .options(joinedload(JobORM.org))
        )
        db_jobs = await self.session.scalars(stmt)
        return [JobORMMapper.to_entity(db_job) for db_job in db_jobs]

    async def get_all(self) -> list[JobEntity]:
        stmt = (
            select(JobORM)
            .options(joinedload(JobORM.org))
        )
        db_jobs = await self.session.scalars(stmt)
        return [JobORMMapper.to_entity(db_job) for db_job in db_jobs]

    async def delete(self, id_: str) -> None:
        stmt = delete(JobORM).where(JobORM.id == id_)
        await self.session.execute(stmt)
