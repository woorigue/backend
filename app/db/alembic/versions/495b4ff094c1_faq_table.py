"""faq_table

Revision ID: 495b4ff094c1
Revises: be5f47a13ece
Create Date: 2023-11-24 20:23:39.872663

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision: str = "495b4ff094c1"
down_revision: Union[str, None] = "71c407fe216c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "faq",
        sa.Column("seq", sa.Integer, primary_key=True, comment="아이디"),
        sa.Column("title", sa.String(255), nullable=False, comment="제목"),
        sa.Column("body", sa.String(255), nullable=False, comment="본문"),
        sa.Column(
            "create_date",
            sa.DateTime,
            nullable=False,
            server_default=func.now(),
            comment="생성일자",
        ),
    )


def downgrade() -> None:
    op.drop_table("faq")
