"""create profile table

Revision ID: be01e375b6d9
Revises: 5c8ff5298885
Create Date: 2023-09-03 02:11:48.919667

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "be01e375b6d9"
down_revision: Union[str, None] = "5c8ff5298885"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "profile",
        sa.Column("seq", sa.Integer, primary_key=True, comment="시퀀스"),
        sa.Column("nickname", sa.String(128), comment="이메일"),
        sa.Column("user_seq", sa.Integer, comment="이메일"),
    )


def downgrade() -> None:
    op.drop_table("profile")
