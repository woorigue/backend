"""add profile img field

Revision ID: eeed23f6b95d
Revises: 7b1ab380a1ca
Create Date: 2023-10-15 23:51:51.569006

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "eeed23f6b95d"
down_revision: Union[str, None] = "7b1ab380a1ca"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "profile",
        sa.Column("img", sa.String(256), nullable=True, comment="프로필 이미지"),
    )


def downgrade() -> None:
    op.drop_column("profile", "img")
