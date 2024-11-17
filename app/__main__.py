from fastapi import FastAPI

from app.application.api import create_app as _create_app
from app.container import init_container
from app.settings import Settings

settings = Settings()  # type: ignore


def create_app() -> FastAPI:
    container = init_container(settings)
    app = _create_app(container)

    return app


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(create_app(), host='0.0.0.0', port=8000)
