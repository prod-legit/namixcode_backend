from dataclasses import dataclass, asdict

from app.domain.entities.org import OrgEntity
from app.infrastructure.repositories.org import IOrgRepository
from app.logic.commands.base import ICommand, IUseCase
from app.logic.exceptions.base import EmptySearchParamsException
from app.logic.exceptions.org import OrgNotFoundException


@dataclass(frozen=True)
class GetOrgQuery(ICommand):
    org_id: str | None = None
    email: str | None = None


@dataclass(eq=False, frozen=True)
class GetOrgUseCase(IUseCase[OrgEntity]):
    org_repository: IOrgRepository

    async def execute(self, query: GetOrgQuery) -> OrgEntity:
        if query.org_id is not None:
            org = await self.org_repository.get(query.org_id)
        elif query.email is not None:
            org = await self.org_repository.get_by_email(query.email)
        else:
            raise EmptySearchParamsException()

        if org is None:
            raise OrgNotFoundException(search_params=asdict(query))

        return org
