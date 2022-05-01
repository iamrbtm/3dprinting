"""empty message

Revision ID: 448594843acd
Revises: ff1a5a2b6f23
Create Date: 2022-04-28 22:35:16.016832

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '448594843acd'
down_revision = 'ff1a5a2b6f23'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('type', sa.Column('g_per_m', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('type', 'g_per_m')
    # ### end Alembic commands ###