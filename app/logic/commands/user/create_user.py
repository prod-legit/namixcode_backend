from dataclasses import dataclass

from app.domain.entities.user import UserEntity
from app.infrastructure.repositories.user import IUserRepository
from app.logic.commands.base import ICommand, IUseCase
from app.logic.exceptions.user import UserExistsException
from app.logic.utils.auth.password import hash_password


@dataclass(frozen=True)
class CreateUserCommand(ICommand):
    email: str
    password: str

    name: str
    phone: str
    experience: int
    skills: list[str]
    interests: list[str]


@dataclass(eq=False, frozen=True)
class CreateUserUseCase(IUseCase[UserEntity]):
    user_repository: IUserRepository

    async def execute(self, command: CreateUserCommand) -> UserEntity:
        if await self.user_repository.get_by_email(command.email):
            raise UserExistsException(command.email)

        user = UserEntity(
            email=command.email,
            hashed_password=hash_password(command.password),
            name=command.name,
            phone=command.phone,
            experience=command.experience,
            skills=command.skills,
            interests=command.interests,
        )
        await self.user_repository.create(user)

        return user
