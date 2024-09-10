"""create device table

Revision ID: c1afb1507725
Revises: 5a80394fe98e
Create Date: 2024-09-08 22:39:57.266534

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c1afb1507725"
down_revision: Union[str, None] = "5a80394fe98e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "device",
        sa.Column("seq", sa.Integer, primary_key=True, comment="시퀀스"),
        sa.Column("user_seq", sa.Integer, comment="유저 시퀸스"),
        sa.Column("token", sa.String(256), comment="기기 토큰"),
    )


def downgrade() -> None:
    op.drop_table("device")
