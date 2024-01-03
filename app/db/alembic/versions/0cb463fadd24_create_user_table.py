"""create user table

Revision ID: 0cb463fadd24
Revises: 
Create Date: 2023-08-19 19:14:40.813580

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0cb463fadd24"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """create user table

    Revision ID: 0cb463fadd24
    Revises:
    Create Date: 2023-08-19 19:14:40.813580
    """


from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0cb463fadd24"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("seq", sa.Integer, primary_key=True, comment="시퀀스"),
        sa.Column("email", sa.String(128), unique=True, comment="이메일"),
        sa.Column("password", sa.String(256), comment="비밀번호"),
        sa.Column("is_active", sa.Boolean, default=True, comment="활성화 여부"),
    )


def downgrade() -> None:
    op.drop_table("users")

    op.create_table(
        "users",
        sa.Column("seq", sa.Integer, primary_key=True, comment="시퀀스"),
        sa.Column("email", sa.String(128), unique=True, comment="이메일"),
        sa.Column("password", sa.String(256), comment="비밀번호"),
        sa.Column("is_active", sa.Boolean, default=True, comment="활성화 여부"),
    )


def downgrade() -> None:
    op.drop_table("users")
