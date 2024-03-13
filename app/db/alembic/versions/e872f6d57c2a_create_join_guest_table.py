"""create_join_guest_table

Revision ID: e872f6d57c2a
Revises: f80b89f6a792
Create Date: 2024-01-30 21:24:38.472899

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e872f6d57c2a"
down_revision: Union[str, None] = "cd94c65116b7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "join_guest",
        sa.Column("seq", sa.Integer, primary_key=True, comment="시퀀스"),
        sa.Column("guest_seq", sa.Integer, comment="게스트 시퀸스"),
        sa.Column("user_seq", sa.Integer, comment="유저 시퀸스"),
        sa.Column("accepted", sa.Boolean, comment="수락 여부"),
    )


def downgrade() -> None:
    op.drop_table("join_guest")
