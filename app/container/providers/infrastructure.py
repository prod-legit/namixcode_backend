from dishka import Provider, provide, Scope

from app.infrastructure.repositories.apply import SQLAlchemyApplyRepository, IApplyRepository
from app.infrastructure.repositories.org import IOrgRepository, SQLAlchemyOrgRepository
from app.infrastructure.repositories.user import SQLAlchemyUserRepository, IUserRepository


class InfrastructureProvider(Provider):
    apply_repository = provide(
        SQLAlchemyApplyRepository,
        scope=Scope.REQUEST,
        provides=IApplyRepository
    )
    org_repository = provide(
        SQLAlchemyOrgRepository,
        scope=Scope.REQUEST,
        provides=IOrgRepository
    )
    user_repository = provide(
        SQLAlchemyUserRepository,
        scope=Scope.REQUEST,
        provides=IUserRepository
    )
