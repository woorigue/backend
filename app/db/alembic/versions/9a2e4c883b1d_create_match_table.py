"""create_match_table

Revision ID: 9a2e4c883b1d
Revises: 495b4ff094c1
Create Date: 2023-12-15 23:13:35.006649

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a2e4c883b1d'
down_revision: Union[str, None] = '495b4ff094c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "match",
        sa.Column('seq', sa.Integer, primary_key=True, comment="시퀀스"),
        sa.Column('match_type', sa.String(24), nullable=False, comment="매치유형"),
        sa.Column('location', sa.String(128), nullable=False, comment="매치장소"),
        sa.Column('match_time', sa.DateTime, nullable=False, comment="매치일정"),
        sa.Column('skill', sa.String(24), nullable=False, comment="레벨"),
        sa.Column('team_size', sa.Integer, comment="매치인원"),
        sa.Column('gender', sa.String(12), nullable=False, comment="성별"),
        sa.Column('match_fee', sa.Integer, nullable=False, comment="매치비용"),
        sa.Column('notice', sa.String(255), nullable=False, comment="공지사항"),
        sa.Column('status', sa.String(24), nullable=False, comment="매치상태"),
        sa.Column('guests', sa.Integer, comment="용병id"),
        sa.Column('club_seq', sa.Integer,  comment="클럽id"),
    )


def downgrade() -> None:
    op.drop_table('match')


