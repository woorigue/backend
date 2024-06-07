"""create firebase table

Revision ID: 58d44d965ece
Revises: abffbe477b7a
Create Date: 2024-05-26 17:40:11.913659

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "58d44d965ece"
down_revision: Union[str, None] = "abffbe477b7a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "firebase",
        sa.Column(
            "seq", sa.Integer, primary_key=True, autoincrement=True, comment="시퀀스"
        ),
        sa.Column(
            "user_seq",
            sa.Integer,
            sa.ForeignKey("users.seq", ondelete="CASCADE"),
            nullable=False,
            comment="유저 시퀸스",
        ),
        sa.Column(
            "refresh_token", sa.String(128), nullable=False, comment="리프레시 토큰"
        ),
    )


def downgrade() -> None:
    op.drop_table("firebase")
