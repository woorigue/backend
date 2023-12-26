"""create_join_club_posting_table

Revision ID: 50432d531f5c
Revises: d39c4d15bc06
Create Date: 2023-12-26 00:36:56.457219

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "50432d531f5c"
down_revision: Union[str, None] = "d39c4d15bc06"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "join_clubPosting",
        sa.Column("seq", sa.Integer, primary_key=True, comment="시퀀스"),
        sa.Column("club_posting_seq", sa.Integer, comment="클럽 포스팅 시퀸스"),
        sa.Column("club_seq", sa.Integer, comment="클럽 시퀸스"),
        sa.Column("user_seq", sa.Integer, comment="유저 시퀸스"),
        sa.Column("accepted", sa.Boolean, comment="수락 여부"),
    )


def downgrade() -> None:
    op.drop_table("join_clubPosting")
