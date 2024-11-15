from dataclasses import dataclass

from app.domain.entities.apply import ApplyEntity
from app.infrastructure.repositories.apply import IApplyRepository
from app.infrastructure.repositories.org import IOrgRepository
from app.logic.commands.base import ICommand, IUseCase
from app.logic.exceptions.apply import ApplyExistsException
from app.logic.exceptions.org import OrgNotFoundException


@dataclass(frozen=True)
class CreateApplyCommand(ICommand):
    org_id: str
    user_id: str


@dataclass(eq=False, frozen=True)
class CreateApplyUseCase(IUseCase[ApplyEntity]):
    apply_repository: IApplyRepository
    org_repository: IOrgRepository

    async def execute(self, command: CreateApplyCommand) -> ApplyEntity:
        if not await self.org_repository.get(command.org_id):
            raise OrgNotFoundException(org_id=command.org_id)

        if await self.apply_repository.get(org_id=command.org_id, user_id=command.user_id):
            raise ApplyExistsException(org_id=command.org_id, user_id=command.user_id)

        apply = ApplyEntity(user_id=command.user_id, org_id=command.org_id)
        await self.apply_repository.create(apply)

        return apply
