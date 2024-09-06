"""add user field in sns table

Revision ID: 9a8d3cb95b17
Revises: aadf8eaddc24
Create Date: 2024-09-06 21:45:55.893182

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9a8d3cb95b17"
down_revision: Union[str, None] = "aadf8eaddc24"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "sns",
        sa.Column("user", sa.String, nullable=True, comment="user"),
    )


def downgrade() -> None:
    pass
