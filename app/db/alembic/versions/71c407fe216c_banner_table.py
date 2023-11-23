"""banner table

Revision ID: 71c407fe216c
Revises: eeed23f6b95d
Create Date: 2023-11-05 10:03:28.932207

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision: str = '71c407fe216c'
down_revision: Union[str, None] = 'eeed23f6b95d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "banner",
        sa.Column("id", sa.Integer, primary_key=True, comment="아이디"),
        sa.Column("url", sa.String(255), nullable=False, comment="주소"),
        sa.Column("create_date", sa.DateTime, nullable=False, server_default=func.now(), comment="생성일자")
    )


def downgrade() -> None:
    op.drop_table('banner')
