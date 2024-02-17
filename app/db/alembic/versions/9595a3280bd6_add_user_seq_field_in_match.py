"""add user_seq field in match

Revision ID: 9595a3280bd6
Revises: 04214ef83305
Create Date: 2024-02-16 21:09:46.769181

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9595a3280bd6"
down_revision: Union[str, None] = "04214ef83305"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "match",
        sa.Column("user_seq", sa.Integer, nullable=False, comment="원정팀 시퀸스"),
    )


def downgrade() -> None:
    op.drop_column("match", "user_seq")
