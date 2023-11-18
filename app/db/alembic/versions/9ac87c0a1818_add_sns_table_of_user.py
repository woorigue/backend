"""add sns table of user

Revision ID: 9ac87c0a1818
Revises: eeed23f6b95d
Create Date: 2023-11-11 01:02:16.170604

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9ac87c0a1818"
down_revision: Union[str, None] = "eeed23f6b95d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "sns",
        sa.Column("seq", sa.Integer, primary_key=True, comment="시퀀스"),
        sa.Column("refresh_token", sa.String(128), comment="이름"),
        sa.Column("sub", sa.String(128), comment="구분 값"),
    )


def downgrade() -> None:
    op.drop_table("sns")
