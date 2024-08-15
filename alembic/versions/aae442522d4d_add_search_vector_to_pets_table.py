"""add search vector to pets table

Revision ID: aae442522d4d
Revises: 3ae1d166277e
Create Date: 2024-08-13 14:51:34.021739

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy_utils import TSVectorType


# revision identifiers, used by Alembic.
revision: str = 'aae442522d4d'
down_revision: Union[str, None] = '3ae1d166277e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('pets', sa.Column('search_vector', TSVectorType('name', 'species', 'description'), nullable = True))


def downgrade():
    op.drop_column('pets', 'search_vector')
