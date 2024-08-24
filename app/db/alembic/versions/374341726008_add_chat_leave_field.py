"""add chat leave field

Revision ID: 374341726008
Revises: 1ef70dd3db8b
Create Date: 2024-08-19 00:28:44.914083

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "374341726008"
down_revision: str | None = "1ef70dd3db8b"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "user_chatroom_association",
        sa.Column("leave", sa.Boolean, comment="채팅방 나가기 여부"),
    )


def downgrade() -> None:
    pass
