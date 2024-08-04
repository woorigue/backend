import os

from pydantic_settings import BaseSettings
from app.core import secret_manager


class Settings(BaseSettings):
    USERNAME: str = secret_manager.get("USERNAME")
    PASSWORD: str = secret_manager.get("PASSWORD")
    DATABASE: str = secret_manager.get("DATABASE")
    PORT: str = secret_manager.get("PORT")
    HOST: str = secret_manager.get("HOST")

    SQLALCHEMY_DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}",
    )
    RABBITMQ_URL: str = "amqp://guest:guest@54.180.94.130/"

    # TODO: To use in cors function
    CORS_ORIGINS: list[str] = ["*"]
    CORS_METHODS: list[str] = ["*"]
    CORS_HEADERS: list[str] = ["*"]


settings = Settings()
