"""empty message

Revision ID: 0d6cb1488d95
Revises: 103ffd276d4b
Create Date: 2022-04-17 00:39:36.098545

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0d6cb1488d95'
down_revision = '103ffd276d4b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'c_subtotal')
    op.drop_column('orders', 'c_total')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('c_total', mysql.FLOAT(), nullable=True))
    op.add_column('orders', sa.Column('c_subtotal', mysql.FLOAT(), nullable=True))
    # ### end Alembic commands ###
