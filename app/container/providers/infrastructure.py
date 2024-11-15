from dishka import Provider, provide, Scope

from app.infrastructure.repositories.apply import SQLAlchemyApplyRepository, IApplyRepository


class InfrastructureProvider(Provider):
    apply_repository = provide(
        SQLAlchemyApplyRepository,
        scope=Scope.REQUEST,
        provides=IApplyRepository
    )
