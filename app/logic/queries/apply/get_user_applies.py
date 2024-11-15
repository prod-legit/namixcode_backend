from dataclasses import dataclass

from app.domain.entities.apply import ApplyEntity
from app.infrastructure.repositories.apply import IApplyRepository
from app.infrastructure.repositories.user import IUserRepository
from app.logic.exceptions.user import UserNotFoundException
from app.logic.queries.base import IQuery, IUseCase


@dataclass(frozen=True)
class GetUserAppliesQuery(IQuery):
    user_id: str


@dataclass(eq=False, frozen=True)
class GetUserAppliesUseCase(IUseCase[list[ApplyEntity]]):
    user_repository: IUserRepository
    apply_repository: IApplyRepository

    async def execute(self, query: GetUserAppliesQuery) -> list[ApplyEntity]:
        if not await self.user_repository.get(query.user_id):
            raise UserNotFoundException(user_id=query.user_id)

        applies = await self.apply_repository.get_by_user_id(query.user_id)
        return applies
