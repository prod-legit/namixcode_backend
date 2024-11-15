from dataclasses import dataclass

from app.domain.entities.org import OrgEntity
from app.infrastructure.repositories.org import IOrgRepository
from app.logic.queries.base import IQuery, IUseCase


@dataclass(frozen=True)
class GetOrgsQuery(IQuery):
    pass


@dataclass(eq=False, frozen=True)
class GetOrgsUseCase(IUseCase[list[OrgEntity]]):
    org_repository: IOrgRepository

    async def execute(self, query: GetOrgsQuery) -> list[OrgEntity]:
        orgs = await self.org_repository.get_all()

        return orgs
