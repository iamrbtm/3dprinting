"""empty message

Revision ID: 731af4a8e502
Revises: e31ec4c34797
Create Date: 2022-04-20 00:14:43.662234

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '731af4a8e502'
down_revision = 'e31ec4c34797'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('active', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'active')
    # ### end Alembic commands ###
