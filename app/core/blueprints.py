from fastapi import FastAPI

from app.rest_api.api import rest_router


def register_router(application: FastAPI) -> None:
    application.include_router(rest_router)
