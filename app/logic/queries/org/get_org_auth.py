from dataclasses import dataclass

from app.domain.entities.org import OrgEntity
from app.infrastructure.repositories.org import IOrgRepository
from app.logic.exceptions.auth import InvalidAuthCredentialsException
from app.logic.queries.base import IQuery, IUseCase
from app.logic.utils.auth.password import verify_password


@dataclass(frozen=True)
class GetOrgAuthQuery(IQuery):
    email: str
    password: str


@dataclass(eq=False, frozen=True)
class GetOrgAuthUseCase(IUseCase[OrgEntity]):
    org_repository: IOrgRepository

    async def execute(self, query: GetOrgAuthQuery) -> OrgEntity:
        org = await self.org_repository.get_by_email(query.email)
        if not org:
            raise InvalidAuthCredentialsException(email=query.email, password=query.password)
        if not verify_password(password=query.password, hashed_password=org.hashed_password):
            raise InvalidAuthCredentialsException(email=query.email, password=query.password)

        return org
