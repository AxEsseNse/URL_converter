"""init. Create table url

Revision ID: c5fb847f089d
Revises: 
Create Date: 2023-04-12 02:04:05.765839

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = 'c5fb847f089d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('url',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('short_url', sa.Text(), unique=True),
                    sa.Column('url', sa.Text(), unique=True),
                    sa.Column('date_creating', sa.Float(), default=datetime.timestamp(datetime.utcnow())),
                    )

def downgrade() -> None:
    op.drop_table('url')
