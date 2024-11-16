from dataclasses import dataclass

from app.domain.entities.employee import EmployeeEntity
from app.infrastructure.repositories.employee import IEmployeeRepository
from app.infrastructure.repositories.org import IOrgRepository
from app.logic.exceptions.org import OrgNotFoundException
from app.logic.queries.base import IQuery, IUseCase


@dataclass(frozen=True)
class GetOrgEmployeesQuery(IQuery):
    org_id: str


@dataclass(eq=False, frozen=True)
class GetOrgEmployeesUseCase(IUseCase[list[EmployeeEntity]]):
    org_repository: IOrgRepository
    employee_repository: IEmployeeRepository

    async def execute(self, query: GetOrgEmployeesQuery) -> list[EmployeeEntity]:
        if not await self.org_repository.get(query.org_id):
            raise OrgNotFoundException(org_id=query.org_id)

        employees = await self.employee_repository.get_by_org_id(query.org_id)
        return employees
