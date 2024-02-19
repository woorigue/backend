"""add level field in profile

Revision ID: 77d0de6ef256
Revises: ee57845aec3d
Create Date: 2024-02-13 01:15:08.016723

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "77d0de6ef256"
down_revision: Union[str, None] = "ee57845aec3d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "profile",
        sa.Column("level", sa.Integer, comment="레벨"),
    )


def downgrade() -> None:
    op.drop_column("profile", "level")
