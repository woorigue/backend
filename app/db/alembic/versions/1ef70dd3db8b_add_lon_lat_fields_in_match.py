"""add lon lat fields in match

Revision ID: 1ef70dd3db8b
Revises: 255977718c41
Create Date: 2024-08-07 00:21:35.179753

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1ef70dd3db8b"
down_revision: Union[str, None] = "255977718c41"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "match",
        sa.Column("longitude", sa.String(32), nullable=True, comment="경도"),
    )
    op.add_column(
        "match",
        sa.Column("latitude", sa.String(32), nullable=True, comment="위도"),
    )


def downgrade() -> None:
    pass
