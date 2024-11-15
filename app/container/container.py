from dishka import AsyncContainer, make_async_container

from app.container.providers import (
    DefaultProvider,
    InfrastructureProvider,
    LogicProvider,
)
from app.settings import Settings


def init_container(settings: Settings) -> AsyncContainer:
    return make_async_container(
        DefaultProvider(),
        InfrastructureProvider(),
        LogicProvider(),
        context={Settings: settings}
    )
