from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = "postgresql://postgres:1q2w3e4r##@database-1.c88pfbyh9brw.ap-northeast-2.rds.amazonaws.com:5432/our_league"
    RABBITMQ_URL: str = "amqp://guest:guest@52.79.239.1/"

    # TODO: To use in cors function
    CORS_ORIGINS: list[str] = ["*"]
    CORS_METHODS: list[str] = ["*"]
    CORS_HEADERS: list[str] = ["*"]


settings = Settings()
