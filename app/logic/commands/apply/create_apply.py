from dataclasses import dataclass

from app.domain.entities.apply import ApplyEntity
from app.infrastructure.repositories.apply import IApplyRepository
from app.infrastructure.repositories.employee import IEmployeeRepository
from app.infrastructure.repositories.job import IJobRepository
from app.infrastructure.repositories.user import IUserRepository
from app.logic.commands.base import ICommand, IUseCase
from app.logic.exceptions.apply import ApplyExistsException
from app.logic.exceptions.employee import EmployeeExistsException
from app.logic.exceptions.job import JobNotFoundException
from app.logic.exceptions.user import UserNotFoundException


@dataclass(frozen=True)
class CreateApplyCommand(ICommand):
    job_id: str
    user_id: str


@dataclass(eq=False, frozen=True)
class CreateApplyUseCase(IUseCase[ApplyEntity]):
    apply_repository: IApplyRepository
    employee_repository: IEmployeeRepository
    job_repository: IJobRepository
    user_repository: IUserRepository

    async def execute(self, command: CreateApplyCommand) -> ApplyEntity:
        job = await self.job_repository.get(command.job_id)
        if not job:
            raise JobNotFoundException(job_id=command.job_id)

        user = await self.user_repository.get(command.user_id)
        if not user:
            raise UserNotFoundException(user_id=command.user_id)

        if await self.employee_repository.check_exists(job_id=command.job_id, user_id=command.user_id):
            raise EmployeeExistsException(job_id=command.job_id, user_id=command.user_id)

        if await self.apply_repository.check_exists(job_id=command.job_id, user_id=command.user_id):
            raise ApplyExistsException(job_id=command.job_id, user_id=command.user_id)

        apply = ApplyEntity(user=user, job=job)
        await self.apply_repository.create(apply)

        return apply
