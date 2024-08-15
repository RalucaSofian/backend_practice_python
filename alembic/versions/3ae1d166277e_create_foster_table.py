"""create foster table

Revision ID: 3ae1d166277e
Revises: 04222d27bce9
Create Date: 2024-08-06 13:10:37.461089

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ae1d166277e'
down_revision: Union[str, None] = '04222d27bce9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'foster',
        sa.Column('id', sa.Integer, primary_key = True),
        sa.Column('user_id', sa.Integer, nullable = True),
        sa.ForeignKeyConstraint(('user_id',), ['auth_users.id'],),
        sa.Column('description', sa.String(100), nullable = True),
        sa.Column('pet_id', sa.Integer),
        sa.ForeignKeyConstraint(('pet_id',), ['pets.id'],),
        sa.Column('start_date', sa.Date),
        sa.Column('end_date', sa.Date, nullable = True),
    )


def downgrade():
    op.drop_table('foster')
