import json
import os
from typing import Any

from authlib.integrations.starlette_client import OAuth
from pydantic_settings import BaseSettings
from starlette.config import Config

from app.core.secrets import get_secret

secret_manager = json.loads(get_secret())


class Settings(BaseSettings):
    # Common
    SERVER_ENV: str = os.getenv("SERVER_ENV", "LOCAL")

    USERNAME: str = secret_manager.get("USERNAME")
    PASSWORD: str = secret_manager.get("PASSWORD")
    DATABASE: str = secret_manager.get("DATABASE")
    PORT: str = secret_manager.get("PORT")
    HOST: str = secret_manager.get("HOST")

    SQLALCHEMY_DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}",
    )
    RABBITMQ_USERNAME: str = secret_manager.get("RABBITMQ_USERNAME")
    RABBITMQ_PASSWORD: str = secret_manager.get("RABBITMQ_PASSWORD")
    RABBITMQ_HOST: str = secret_manager.get("RABBITMQ_HOST")
    RABBITMQ_URL: str = (
        f"amqp://{RABBITMQ_USERNAME}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}/"
    )

    # SNS Settings
    GOOGLE_CLIENT_ID: str = secret_manager.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = secret_manager.get("GOOGLE_CLIENT_SECRET")
    google_config_data: dict = {
        "GOOGLE_CLIENT_ID": GOOGLE_CLIENT_ID,
        "GOOGLE_CLIENT_SECRET": GOOGLE_CLIENT_SECRET,
    }
    google_starlette_config: Any = Config(environ=google_config_data)
    GOOGLE_OAUTH: Any = OAuth(google_starlette_config).register(
        name="google",
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={
            "scope": "openid email profile",
            "access_type": "offline",
            "prompt": "consent",
        },
    )

    # TODO: To use in cors function
    CORS_ORIGINS: list[str] = ["*"]
    CORS_METHODS: list[str] = ["*"]
    CORS_HEADERS: list[str] = ["*"]


settings = Settings()
