"""create email table

Revision ID: 5c8ff5298885
Revises: 0cb463fadd24
Create Date: 2023-08-27 01:11:20.676076

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5c8ff5298885"
down_revision: Union[str, None] = "0cb463fadd24"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "email",
        sa.Column("seq", sa.Integer, primary_key=True, comment="시퀀스"),
        sa.Column("email", sa.String(128), comment="이메일"),
        sa.Column("is_verified", sa.String(256), comment="인증 여부"),
        sa.Column(
            "expired_at", sa.DateTime, server_default=sa.sql.func.now(), comment="만료 시간"
        ),
    )


def downgrade() -> None:
    op.drop_table("email")
