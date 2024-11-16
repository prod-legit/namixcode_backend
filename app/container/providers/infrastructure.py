from dishka import Provider, provide, Scope

from app.infrastructure.repositories.apply import SQLAlchemyApplyRepository, IApplyRepository
from app.infrastructure.repositories.employee import SQLAlchemyEmployeeRepository, IEmployeeRepository
from app.infrastructure.repositories.org import IOrgRepository, SQLAlchemyOrgRepository
from app.infrastructure.repositories.user import SQLAlchemyUserRepository, IUserRepository
from app.infrastructure.services.gpt_tarologue import YandexGPTTarologue, IGPTTarologue
from app.settings import Settings


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
    employee_repository = provide(
        SQLAlchemyEmployeeRepository,
        scope=Scope.REQUEST,
        provides=IEmployeeRepository
    )

    @provide(scope=Scope.APP)
    def gpt_tarologue(self, settings: Settings) -> IGPTTarologue:
        return YandexGPTTarologue(
            api_url=settings.yagpt.URL,
            api_key=settings.yagpt.KEY,
            folder_id=settings.yagpt.FOLDER
        )
