"""add_role_field_in_join_club

Revision ID: a656e43b0139
Revises: ddbd6b831a6b
Create Date: 2023-11-30 00:11:16.333313

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a656e43b0139"
down_revision: Union[str, None] = "ddbd6b831a6b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("join_club", sa.Column("role", sa.String(24), comment="역할"))


def downgrade() -> None:
    op.drop_column("join_club", "role")
