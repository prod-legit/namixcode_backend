from abc import abstractmethod, ABC
from dataclasses import dataclass

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.entities.user import UserEntity
from app.infrastructure.gateways.postgresql.mappers.user import UserORMMapper
from app.infrastructure.gateways.postgresql.models import UserORM


@dataclass(eq=False, frozen=True)
class IUserRepository(ABC):
    @abstractmethod
    async def create(self, entity: UserEntity) -> None: ...

    @abstractmethod
    async def get(self, id_: str) -> UserEntity | None: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> UserEntity | None: ...

    @abstractmethod
    async def delete(self, id_: str) -> None: ...


@dataclass(eq=False, frozen=True)
class SQLAlchemyUserRepository(IUserRepository):
    session: AsyncSession

    async def create(self, entity: UserEntity) -> None:
        db_user = UserORMMapper.from_entity(entity)
        self.session.add(db_user)

    async def get(self, id_: str) -> UserEntity | None:
        stmt = (
            select(UserORM)
            .where(UserORM.id == id_)
            .options(
                selectinload(UserORM.skills),
                selectinload(UserORM.interests)
            )
        )
        if db_user := await self.session.scalar(stmt):
            return UserORMMapper.to_entity(db_user)

    async def get_by_email(self, email: str) -> UserEntity | None:
        stmt = (
            select(UserORM)
            .where(UserORM.email == email)
            .options(
                selectinload(UserORM.skills),
                selectinload(UserORM.interests)
            )
        )
        if db_user := await self.session.scalar(stmt):
            return UserORMMapper.to_entity(db_user)

    async def delete(self, id_: str) -> None:
        stmt = delete(UserORM).where(UserORM.id == id_)
        await self.session.execute(stmt)
