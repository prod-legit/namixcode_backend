from dataclasses import dataclass

from app.domain.entities.apply import ApplyEntity
from app.infrastructure.repositories.apply import IApplyRepository
from app.infrastructure.repositories.org import IOrgRepository
from app.logic.exceptions.org import OrgNotFoundException
from app.logic.queries.base import IQuery, IUseCase


@dataclass(frozen=True)
class GetOrgAppliesQuery(IQuery):
    org_id: str


@dataclass(eq=False, frozen=True)
class GetOrgAppliesUseCase(IUseCase[list[ApplyEntity]]):
    org_repository: IOrgRepository
    apply_repository: IApplyRepository

    async def execute(self, query: GetOrgAppliesQuery) -> list[ApplyEntity]:
        if not await self.org_repository.get(query.org_id):
            raise OrgNotFoundException(org_id=query.org_id)

        applies = await self.apply_repository.get_by_org_id(query.org_id)
        return applies
