"""add to table url column count_use

Revision ID: 886c2c531b2a
Revises: 0c37f055e73b
Create Date: 2023-04-12 02:36:58.591918

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '886c2c531b2a'
down_revision = '0c37f055e73b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('url', sa.Column('count_use', sa.Integer(), default=1))

def downgrade() -> None:
    op.drop_column('url', 'count_use')
