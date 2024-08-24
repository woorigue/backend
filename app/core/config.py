import os, json

from pydantic_settings import BaseSettings
from app.core.secrets import get_secret

secret_manager = json.loads(get_secret())


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
    RABBITMQ_URL: str = "amqp://guest:guest@43.201.46.100/"

    # TODO: To use in cors function
    CORS_ORIGINS: list[str] = ["*"]
    CORS_METHODS: list[str] = ["*"]
    CORS_HEADERS: list[str] = ["*"]


settings = Settings()
