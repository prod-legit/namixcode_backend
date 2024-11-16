from dataclasses import dataclass

from app.domain.entities.job import JobEntity
from app.infrastructure.repositories.job import IJobRepository
from app.infrastructure.repositories.org import IOrgRepository
from app.logic.exceptions.org import OrgNotFoundException
from app.logic.queries.base import IQuery, IUseCase


@dataclass(frozen=True)
class GetOrgJobsQuery(IQuery):
    org_id: str


@dataclass(eq=False, frozen=True)
class GetOrgJobsUseCase(IUseCase[list[JobEntity]]):
    org_repository: IOrgRepository
    job_repository: IJobRepository

    async def execute(self, query: GetOrgJobsQuery) -> list[JobEntity]:
        if not await self.org_repository.get(query.org_id):
            raise OrgNotFoundException(org_id=query.org_id)

        jobs = await self.job_repository.get_by_org_id(query.org_id)
        return jobs
