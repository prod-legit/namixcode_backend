from dataclasses import dataclass

from app.domain.entities.job import JobEntity
from app.infrastructure.repositories.job import IJobRepository
from app.logic.queries.base import IQuery, IUseCase


@dataclass(frozen=True)
class GetJobsQuery(IQuery):
    pass


@dataclass(eq=False, frozen=True)
class GetJobsUseCase(IUseCase[list[JobEntity]]):
    job_repository: IJobRepository

    async def execute(self, query: GetJobsQuery) -> list[JobEntity]:
        jobs = await self.job_repository.get_all()
        return jobs
