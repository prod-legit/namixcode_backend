from dataclasses import dataclass

from app.domain.entities.org import OrgEntity
from app.infrastructure.repositories.org import IOrgRepository
from app.logic.commands.base import ICommand, IUseCase
from app.logic.exceptions.org import OrgExistsException
from app.logic.utils.auth.password import hash_password


@dataclass(frozen=True)
class CreateOrgCommand(ICommand):
    email: str
    password: str

    name: str
    description: str
    location: str
    logo: str
    foundation_year: int
    scope: str


@dataclass(eq=False, frozen=True)
class CreateOrgUseCase(IUseCase[OrgEntity]):
    org_repository: IOrgRepository

    async def execute(self, command: CreateOrgCommand) -> OrgEntity:
        if await self.org_repository.get_by_email(command.email):
            raise OrgExistsException(command.email)

        org = OrgEntity(
            email=command.email,
            hashed_password=hash_password(command.password),
            name=command.name,
            description=command.description,
            location=command.location,
            logo=command.logo,
            foundation_year=command.foundation_year,
            scope=command.scope
        )
        await self.org_repository.create(org)

        return org
