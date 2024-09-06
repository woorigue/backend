"""remove unique email

Revision ID: 5a80394fe98e
Revises: 9a8d3cb95b17
Create Date: 2024-09-06 22:09:31.628899

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5a80394fe98e"
down_revision: Union[str, None] = "9a8d3cb95b17"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("users_email_key", "users", type_="unique")


def downgrade() -> None:
    pass
