from dishka import Provider, provide, Scope

from app.infrastructure.repositories.apply import SQLAlchemyApplyRepository, IApplyRepository
from app.infrastructure.repositories.org import IOrgRepository, SQLAlchemyOrgRepository


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
