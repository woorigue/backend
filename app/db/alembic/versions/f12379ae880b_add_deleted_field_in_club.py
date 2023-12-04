"""add_deleted_field_in_club

Revision ID: f12379ae880b
Revises: a656e43b0139
Create Date: 2023-11-30 21:31:12.221178

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f12379ae880b"
down_revision: Union[str, None] = "a656e43b0139"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("clubs", sa.Column("deleted", sa.Boolean, comment="삭제 여부"))


def downgrade() -> None:
    op.drop_column("clubs", "deleted")
