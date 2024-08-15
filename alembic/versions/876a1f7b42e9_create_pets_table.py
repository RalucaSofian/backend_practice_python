"""create pets table

Revision ID: 876a1f7b42e9
Revises: 4f45da764ccf
Create Date: 2024-07-24 15:13:48.353002

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '876a1f7b42e9'
down_revision: Union[str, None] = '4f45da764ccf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'pets',
        sa.Column('id', sa.Integer, primary_key = True),
        sa.Column('name', sa.String(50), index = True),
        sa.Column('species', sa.String(50), index = True, nullable = True),
        sa.Column('gender', sa.String(2), index = True, nullable = True),
        sa.Column('age', sa.Float, nullable = True),
        sa.Column('description', sa.String(100), nullable = True),
    )


def downgrade():
    op.drop_table('pets')
