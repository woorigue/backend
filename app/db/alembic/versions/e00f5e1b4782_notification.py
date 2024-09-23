"""notification

Revision ID: e00f5e1b4782
Revises: c1afb1507725
Create Date: 2024-09-23 01:50:17.648320

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e00f5e1b4782"
down_revision: str | None = "c1afb1507725"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "notification",
        sa.Column("seq", sa.Integer, autoincrement=True, nullable=False, comment="시퀀스"),
        sa.Column("type", sa.String(128), nullable=True, comment="알림 타입"),
        sa.Column("from_user_seq", sa.Integer, nullable=True),
        sa.Column("to_user_seq", sa.Integer, nullable=True),
        sa.Column("title", sa.String(128), nullable=True, comment="제목"),
        sa.Column("message", sa.String(128), nullable=True, comment="메시지"),
        sa.Column("data", sa.JSON, nullable=True, comment="데이터"),
        sa.Column("is_read", sa.Boolean, default=False, comment="읽음 처리"),
        sa.Column(
            "created_at", sa.DateTime, server_default=sa.func.now(), comment="생성 시간"
        ),
        sa.Column(
            "updated_at",
            sa.DateTime,
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            comment="업데이트 시간",
        ),
        sa.ForeignKeyConstraint(["from_user_seq"], ["users.seq"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["to_user_seq"], ["users.seq"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("seq"),
    )


def downgrade() -> None:
    pass
