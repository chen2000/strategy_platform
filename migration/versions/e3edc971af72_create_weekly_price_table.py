"""create weekly price table

Revision ID: e3edc971af72
Revises: 553899dcc4a6
Create Date: 2017-06-24 18:40:19.735804

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3edc971af72'
down_revision = '553899dcc4a6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'weekly_price',
        sa.Column('ind', sa.String(15), primary_key=True),
        sa.Column('symbol', sa.String(10), primary_key=True),
        sa.Column('date', sa.Date, primary_key=True),
        sa.Column('high', sa.Float),
        sa.Column('low', sa.Float),
        sa.Column('open', sa.Float),
        sa.Column('close', sa.Float),
        sa.Column('volume', sa.BigInteger)
    )

def downgrade():
    op.drop_table('weekly_price')
