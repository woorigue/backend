"""add user field in sns

Revision ID: 3fbe5e20d8da
Revises: 9ac87c0a1818
Create Date: 2023-11-11 01:21:41.241752

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3fbe5e20d8da"
down_revision: Union[str, None] = "9ac87c0a1818"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "sns",
        sa.Column("user_seq", sa.Integer, comment="이메일"),
    )


def downgrade() -> None:
    op.drop_column("sns", "user_seq")
