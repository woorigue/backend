from alembic import context

from app.core.config import settings

config = context.config

config.set_main_option("sqlalchemy.url", settings.SQLALCHEMY_DATABASE_URL)
