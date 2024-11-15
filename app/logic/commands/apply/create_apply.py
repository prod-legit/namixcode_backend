from dataclasses import dataclass

from app.domain.entities.apply import ApplyEntity
from app.infrastructure.repositories.apply import IApplyRepository
from app.infrastructure.repositories.org import IOrgRepository
from app.logic.commands.base import ICommand, IUseCase
from app.logic.exceptions.org import OrgNotFoundException


@dataclass(frozen=True)
class CreateApplyCommand(ICommand):
    org_id: str
    name: str
    phone: str
    email: str
    experience: int
    skills: list[str]
    interests: list[str]


@dataclass(eq=False, frozen=True)
class CreateApplyUseCase(IUseCase[ApplyEntity]):
    apply_repository: IApplyRepository
    org_repository: IOrgRepository

    async def execute(self, command: CreateApplyCommand) -> ApplyEntity:
        if not await self.org_repository.get(command.org_id):
            raise OrgNotFoundException(org_id=command.org_id)

        apply = ApplyEntity(
            org_id=command.org_id,
            name=command.name,
            phone=command.phone,
            email=command.email,
            experience=command.experience,
            skills=command.skills,
            interests=command.interests,
        )
        await self.apply_repository.create(apply)

        return apply
