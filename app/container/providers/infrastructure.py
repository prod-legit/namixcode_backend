from dishka import Provider, provide, Scope

from app.infrastructure.repositories.apply import SQLAlchemyApplyRepository, IApplyRepository
from app.infrastructure.repositories.org import IOrgRepository, SQLAlchemyOrgRepository
from app.infrastructure.services.gpt_tarologue import IGPTTarologue, YandexGPTTarologue
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

    @provide(scope=Scope.REQUEST)
    def gpt_tarologue(self, settings: Settings) -> IGPTTarologue:
        return YandexGPTTarologue(
            api_url=settings.yandex_gpt.APi_URL,
            api_key=settings.yandex_gpt.API_KEY,
            folder_id=settings.yandex_gpt.FOLDER_ID
        )
