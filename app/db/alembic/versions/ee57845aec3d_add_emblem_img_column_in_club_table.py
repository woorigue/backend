"""add emblem_img column in club table

Revision ID: ee57845aec3d
Revises: 294a3ff6e932
Create Date: 2024-02-05 22:13:37.554384

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ee57845aec3d"
down_revision: Union[str, None] = "294a3ff6e932"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "clubs",
        sa.Column("emblem_img", sa.String(256), comment="클럽 엠블럼 이미지"),
    )


def downgrade() -> None:
    op.drop_column("clubs", "emblem_img")
