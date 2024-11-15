from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.application.api.endpoints import routers
from app.application.api.middlewares import ExceptionMiddleware


def create_app(container: AsyncContainer) -> FastAPI:
    app = FastAPI()
    app.add_middleware(ExceptionMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"]
    )
    setup_dishka(container=container, app=app)

    for router in routers:
        app.include_router(router)

    return app
