"""add user_seq field of club

Revision ID: cd94c65116b7
Revises: 8ff415cb2ace
Create Date: 2024-01-28 22:53:52.146943

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cd94c65116b7"
down_revision: Union[str, None] = "8ff415cb2ace"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
