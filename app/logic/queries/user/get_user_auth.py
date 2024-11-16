from dataclasses import dataclass

from app.domain.entities.user import UserEntity
from app.infrastructure.repositories.user import IUserRepository
from app.logic.exceptions.auth import InvalidAuthCredentialsException
from app.logic.queries.base import IQuery, IUseCase
from app.logic.utils.auth.password import verify_password


@dataclass(frozen=True)
class GetUserAuthQuery(IQuery):
    email: str
    password: str


@dataclass(eq=False, frozen=True)
class GetUserAuthUseCase(IUseCase[UserEntity]):
    user_repository: IUserRepository

    async def execute(self, query: GetUserAuthQuery) -> UserEntity:
        user = await self.user_repository.get_by_email(query.email)
        if not user:
            raise InvalidAuthCredentialsException(email=query.email, password=query.password)
        if not verify_password(password=query.password, hashed_password=user.hashed_password):
            raise InvalidAuthCredentialsException(email=query.email, password=query.password)

        return user
