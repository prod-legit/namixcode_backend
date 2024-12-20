from dataclasses import dataclass

from app.domain.entities.apply import ApplyEntity
from app.domain.entities.employee import EmployeeEntity
from app.infrastructure.repositories.apply import IApplyRepository
from app.infrastructure.repositories.employee import IEmployeeRepository
from app.infrastructure.repositories.org import IOrgRepository
from app.logic.commands.base import ICommand, IUseCase
from app.logic.exceptions.apply import ApplyNotFoundException
from app.logic.exceptions.employee import EmployeeNotFoundException, EmployeeExistsException


@dataclass(frozen=True)
class AcceptApplyCommand(ICommand):
    job_id: str
    user_id: str
    head_id: str | None


@dataclass(eq=False, frozen=True)
class AcceptApplyUseCase(IUseCase[ApplyEntity]):
    apply_repository: IApplyRepository
    employee_repository: IEmployeeRepository
    org_repository: IOrgRepository

    async def execute(self, command: AcceptApplyCommand) -> None:
        apply = await self.apply_repository.get(job_id=command.job_id, user_id=command.user_id)
        if not apply:
            raise ApplyNotFoundException(job_id=command.job_id, user_id=command.user_id)

        if await self.employee_repository.check_exists(
                job_id=command.job_id,
                user_id=command.user_id
        ):
            raise EmployeeExistsException(job_id=command.job_id, user_id=command.user_id)

        head = None
        if command.head_id is not None:
            head = await self.employee_repository.get(job_id=command.job_id, user_id=command.head_id)
            if not head:
                raise EmployeeNotFoundException(command.head_id)

        employee = EmployeeEntity(
            job=apply.job,
            user=apply.user,
            head=head
        )
        await self.employee_repository.create(employee)
        await self.apply_repository.delete(apply.id)
