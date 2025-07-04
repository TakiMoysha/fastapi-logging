from logging import getLogger

logger = getLogger(__name__)


def create_asgi():
    from fastapi import FastAPI

    from app.config import get_config
    from app.server import app_lifespan

    config = get_config()

    app = FastAPI(
        title="FastAPI-News",
        version="0.1.0",
        debug=config.server.debug,
        lifespan=app_lifespan,
        middleware=[],
    )

    from app.server import setup_logging

    setup_logging(app)

    from app.router import root_router

    app.include_router(root_router)

    return app
