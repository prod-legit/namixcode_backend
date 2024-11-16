from dataclasses import dataclass

from app.domain.entities.employee import EmployeeEntity
from app.infrastructure.repositories.employee import IEmployeeRepository
from app.infrastructure.repositories.user import IUserRepository
from app.logic.exceptions.user import UserNotFoundException
from app.logic.queries.base import IQuery, IUseCase


@dataclass(frozen=True)
class GetUserEmploymentsQuery(IQuery):
    user_id: str


@dataclass(eq=False, frozen=True)
class GetUserEmploymentsUseCase(IUseCase[list[EmployeeEntity]]):
    user_repository: IUserRepository
    employee_repository: IEmployeeRepository

    async def execute(self, query: GetUserEmploymentsQuery) -> list[EmployeeEntity]:
        if not await self.user_repository.get(query.user_id):
            raise UserNotFoundException(user_id=query.user_id)

        employments = await self.employee_repository.get_by_user_id(query.user_id)
        return employments
