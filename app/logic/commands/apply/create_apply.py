from dataclasses import dataclass

from app.domain.entities.apply import ApplyEntity
from app.infrastructure.repositories.apply import IApplyRepository
from app.logic.commands.base import ICommand, IUseCase


@dataclass(frozen=True)
class CreateApplyCommand(ICommand):
    name: str
    phone: str
    email: str
    experience: int
    skills: list[str]
    interests: list[str]


@dataclass(eq=False, frozen=True)
class CreateApplyUseCase(IUseCase[ApplyEntity]):
    apply_repository: IApplyRepository

    async def execute(self, command: CreateApplyCommand) -> ApplyEntity:
        apply = ApplyEntity(
            name=command.name,
            phone=command.phone,
            email=command.email,
            experience=command.experience,
            skills=command.skills,
            interests=command.interests,
        )
        await self.apply_repository.create(apply)

        return apply
