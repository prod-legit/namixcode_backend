from dataclasses import dataclass

from app.domain.entities.job import JobEntity
from app.infrastructure.repositories.job import IJobRepository
from app.infrastructure.repositories.org import IOrgRepository
from app.logic.commands.base import ICommand, IUseCase
from app.logic.exceptions.org import OrgNotFoundException


@dataclass(frozen=True)
class CreateJobCommand(ICommand):
    org_id: str
    title: str
    description: str
    pay: str


@dataclass(eq=False, frozen=True)
class CreateJobUseCase(IUseCase[JobEntity]):
    job_repository: IJobRepository
    org_repository: IOrgRepository

    async def execute(self, command: CreateJobCommand) -> JobEntity:
        org = await self.org_repository.get(command.org_id)
        if not org:
            raise OrgNotFoundException(org_id=command.org_id)

        job = JobEntity(
            org=org,
            title=command.title,
            description=command.description,
            pay=command.pay
        )
        await self.job_repository.create(job)

        return job
