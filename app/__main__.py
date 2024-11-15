import argparse

import uvicorn
from fastapi import FastAPI

from app.application.api import create_app as _create_app
from app.container import init_container
from app.settings import Settings

settings = Settings()  # type: ignore


def create_app() -> FastAPI:
    container = init_container(settings)
    app = _create_app(container)

    return app


def main(reload: bool = False) -> None:
    uvicorn.run(
        app="app.__main__:create_app",
        factory=True,
        host="0.0.0.0",
        port=settings.SERVICE_PORT,
        reload=reload,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reload", action="store_true")
    args = parser.parse_args()

    main(reload=args.reload)
