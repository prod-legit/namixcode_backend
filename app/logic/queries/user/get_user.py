from dataclasses import dataclass

from app.domain.entities.user import UserEntity
from app.infrastructure.repositories.user import IUserRepository
from app.logic.exceptions.base import EmptySearchParamsException
from app.logic.exceptions.user import UserNotFoundException
from app.logic.queries.base import IQuery, IUseCase


@dataclass(frozen=True)
class GetUserQuery(IQuery):
    user_id: str | None = None
    email: str | None = None


@dataclass(eq=False, frozen=True)
class GetUserUseCase(IUseCase[UserEntity]):
    user_repository: IUserRepository

    async def execute(self, query: GetUserQuery) -> UserEntity:
        if query.user_id is not None:
            user = await self.user_repository.get(query.user_id)
        elif query.email is not None:
            user = await self.user_repository.get_by_email(query.email)
        else:
            raise EmptySearchParamsException()

        if user is None:
            raise UserNotFoundException(user_id=query.user_id, email=query.email)

        return user
