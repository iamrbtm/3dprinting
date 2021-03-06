"""empty message

Revision ID: 19666a59fa53
Revises: 7bca9c97cfcd
Create Date: 2022-04-04 22:46:52.487366

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19666a59fa53'
down_revision = '7bca9c97cfcd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer', sa.Column('company', sa.String(length=150), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('customer', 'company')
    # ### end Alembic commands ###
