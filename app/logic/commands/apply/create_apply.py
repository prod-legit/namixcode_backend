from dataclasses import dataclass

from app.domain.entities.apply import ApplyEntity
from app.infrastructure.repositories.apply import IApplyRepository
from app.infrastructure.repositories.employee import IEmployeeRepository
from app.infrastructure.repositories.org import IOrgRepository
from app.infrastructure.repositories.user import IUserRepository
from app.logic.commands.base import ICommand, IUseCase
from app.logic.exceptions.apply import ApplyExistsException
from app.logic.exceptions.employee import EmployeeExistsException
from app.logic.exceptions.org import OrgNotFoundException
from app.logic.exceptions.user import UserNotFoundException


@dataclass(frozen=True)
class CreateApplyCommand(ICommand):
    org_id: str
    user_id: str


@dataclass(eq=False, frozen=True)
class CreateApplyUseCase(IUseCase[ApplyEntity]):
    apply_repository: IApplyRepository
    employee_repository: IEmployeeRepository
    org_repository: IOrgRepository
    user_repository: IUserRepository

    async def execute(self, command: CreateApplyCommand) -> ApplyEntity:
        org = await self.org_repository.get(command.org_id)
        if not org:
            raise OrgNotFoundException(org_id=command.org_id)

        user = await self.user_repository.get(command.user_id)
        if not user:
            raise UserNotFoundException(user_id=command.user_id)

        if await self.employee_repository.check_exists(org_id=command.org_id, user_id=command.user_id):
            raise EmployeeExistsException(org_id=command.org_id, user_id=command.user_id)

        if await self.apply_repository.check_exists(org_id=command.org_id, user_id=command.user_id):
            raise ApplyExistsException(org_id=command.org_id, user_id=command.user_id)

        apply = ApplyEntity(user=user, org=org)
        await self.apply_repository.create(apply)

        return apply
