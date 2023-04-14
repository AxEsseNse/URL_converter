"""add table feedback

Revision ID: 0c37f055e73b
Revises: c5fb847f089d
Create Date: 2023-04-12 02:23:14.097023

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '0c37f055e73b'
down_revision = 'c5fb847f089d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('feedback',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('msg', sa.Text(), unique=True),
                    sa.Column('date', sa.Float(), default=datetime.timestamp(datetime.utcnow())),
                    )

def downgrade() -> None:
    op.drop_table('feedback')
