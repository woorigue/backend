"""add match type

Revision ID: 240f608b8121
Revises: f94d26f2f139
Create Date: 2024-06-21 00:28:14.728916

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "240f608b8121"
down_revision: Union[str, None] = "f94d26f2f139"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "match",
        sa.Column(
            "match_type",
            sa.String(24),
            nullable=False,
            server_default="default_value",
            comment="매치유형",
        ),
    )
    # 기본 값 제거
    op.alter_column("match", "match_type", server_default=None)


def downgrade() -> None:
    pass
