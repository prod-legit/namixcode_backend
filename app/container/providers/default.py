from collections.abc import AsyncIterator

from app.settings import Settings
from dishka import Provider, Scope, from_context, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


class DefaultProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_session_maker(self, settings: Settings) -> async_sessionmaker:
        engine = create_async_engine(settings.database.url, pool_pre_ping=True)
        session_maker = async_sessionmaker(bind=engine)

        return session_maker

    @provide(scope=Scope.REQUEST)
    async def get_database_session(
            self, session_maker: async_sessionmaker
    ) -> AsyncIterator[AsyncSession]:
        async with session_maker() as session:
            async with session.begin():
                yield session
