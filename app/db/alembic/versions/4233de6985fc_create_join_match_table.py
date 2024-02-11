"""create_join_match_table

Revision ID: 4233de6985fc
Revises: e872f6d57c2a
Create Date: 2024-02-02 22:49:06.244000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4233de6985fc"
down_revision: Union[str, None] = "e872f6d57c2a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "join_match",
        sa.Column("seq", sa.Integer, primary_key=True, comment="시퀀스"),
        sa.Column("match_seq", sa.Integer, comment="매치 시퀸스"),
        sa.Column("user_seq", sa.Integer, comment="유저 시퀸스"),
        sa.Column("accepted", sa.Boolean, comment="수락 여부"),
    )


def downgrade() -> None:
    op.drop_table("join_match")
