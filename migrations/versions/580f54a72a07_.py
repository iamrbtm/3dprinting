"""empty message

Revision ID: 580f54a72a07
Revises: 5c76b887f3e3
Create Date: 2022-04-03 22:28:55.707089

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '580f54a72a07'
down_revision = '5c76b887f3e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order_lineitems', sa.Column('date_needed', sa.Date(), nullable=True))
    op.add_column('order_lineitems', sa.Column('project_name', sa.String(length=100), nullable=True))
    op.add_column('order_lineitems', sa.Column('qty', sa.Integer(), nullable=True))
    op.add_column('order_lineitems', sa.Column('weight_in_g', sa.String(length=10), nullable=True))
    op.add_column('order_lineitems', sa.Column('time_to_print', sa.String(length=50), nullable=True))
    op.add_column('order_lineitems', sa.Column('setuptime', sa.Integer(), nullable=True))
    op.add_column('order_lineitems', sa.Column('taredowntime', sa.Integer(), nullable=True))
    op.create_unique_constraint(None, 'order_lineitems', ['project_name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'order_lineitems', type_='unique')
    op.drop_column('order_lineitems', 'taredowntime')
    op.drop_column('order_lineitems', 'setuptime')
    op.drop_column('order_lineitems', 'time_to_print')
    op.drop_column('order_lineitems', 'weight_in_g')
    op.drop_column('order_lineitems', 'qty')
    op.drop_column('order_lineitems', 'project_name')
    op.drop_column('order_lineitems', 'date_needed')
    # ### end Alembic commands ###
