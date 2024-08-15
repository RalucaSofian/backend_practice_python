"""create clients table

Revision ID: 04222d27bce9
Revises: 876a1f7b42e9
Create Date: 2024-07-25 13:59:44.918270

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey

from models import auth_user


# revision identifiers, used by Alembic.
revision: str = '04222d27bce9'
down_revision: Union[str, None] = '876a1f7b42e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'clients',
        sa.Column('id', sa.Integer, primary_key = True),
        sa.Column('user_id', sa.Integer, nullable = True),
        sa.ForeignKeyConstraint(('user_id',), ['auth_users.id'],),
        sa.Column('description', sa.String(100), nullable = True),
    )


def downgrade():
    op.drop_table('clients')
