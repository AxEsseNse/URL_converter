"""add to table alemurl column date_last_use

Revision ID: cd48b53cb918
Revises: 886c2c531b2a
Create Date: 2023-04-12 02:44:09.067930

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = 'cd48b53cb918'
down_revision = '886c2c531b2a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('alemurl', sa.Column('date_last_use', sa.Float(), default=datetime.timestamp(datetime.utcnow())))


def downgrade() -> None:
    op.drop_column('alemurl', 'date_last_use')
