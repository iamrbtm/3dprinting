"""empty message

Revision ID: 4973e3592810
Revises: 19666a59fa53
Create Date: 2022-04-05 00:24:04.486784

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4973e3592810'
down_revision = '19666a59fa53'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('order_lineitems_ibfk_4', 'order_lineitems', type_='foreignkey')
    op.drop_constraint('order_lineitems_ibfk_3', 'order_lineitems', type_='foreignkey')
    op.drop_constraint('order_lineitems_ibfk_1', 'order_lineitems', type_='foreignkey')
    op.drop_constraint('order_lineitems_ibfk_2', 'order_lineitems', type_='foreignkey')
    op.drop_column('order_lineitems', 'orderfk')
    op.drop_column('order_lineitems', 'userid')
    op.drop_column('order_lineitems', 'setuptime')
    op.drop_column('order_lineitems', 'time_to_print')
    op.drop_column('order_lineitems', 'machinefk')
    op.drop_column('order_lineitems', 'weight_in_g')
    op.drop_column('order_lineitems', 'project_status')
    op.drop_column('order_lineitems', 'date_created')
    op.drop_column('order_lineitems', 'filamentfk')
    op.drop_column('order_lineitems', 'qty')
    op.drop_column('order_lineitems', 'taredowntime')
    op.drop_column('order_lineitems', 'update_time')
    op.add_column('orders', sa.Column('qty', sa.Integer(), nullable=True))
    op.add_column('orders', sa.Column('weight_in_g', sa.String(length=10), nullable=True))
    op.add_column('orders', sa.Column('time_to_print', sa.String(length=50), nullable=True))
    op.add_column('orders', sa.Column('setuptime', sa.Integer(), nullable=True))
    op.add_column('orders', sa.Column('taredowntime', sa.Integer(), nullable=True))
    op.add_column('orders', sa.Column('machinefk', sa.Integer(), nullable=True))
    op.add_column('orders', sa.Column('filamentfk', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'orders', 'filament', ['filamentfk'], ['id'])
    op.create_foreign_key(None, 'orders', 'machine', ['machinefk'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.drop_column('orders', 'filamentfk')
    op.drop_column('orders', 'machinefk')
    op.drop_column('orders', 'taredowntime')
    op.drop_column('orders', 'setuptime')
    op.drop_column('orders', 'time_to_print')
    op.drop_column('orders', 'weight_in_g')
    op.drop_column('orders', 'qty')
    op.add_column('order_lineitems', sa.Column('update_time', mysql.DATETIME(), nullable=True))
    op.add_column('order_lineitems', sa.Column('taredowntime', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('order_lineitems', sa.Column('qty', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('order_lineitems', sa.Column('filamentfk', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('order_lineitems', sa.Column('date_created', mysql.DATETIME(), nullable=True))
    op.add_column('order_lineitems', sa.Column('project_status', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('order_lineitems', sa.Column('weight_in_g', mysql.VARCHAR(length=10), nullable=True))
    op.add_column('order_lineitems', sa.Column('machinefk', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('order_lineitems', sa.Column('time_to_print', mysql.VARCHAR(length=50), nullable=True))
    op.add_column('order_lineitems', sa.Column('setuptime', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('order_lineitems', sa.Column('userid', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('order_lineitems', sa.Column('orderfk', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key('order_lineitems_ibfk_2', 'order_lineitems', 'filament', ['filamentfk'], ['id'])
    op.create_foreign_key('order_lineitems_ibfk_1', 'order_lineitems', 'machine', ['machinefk'], ['id'])
    op.create_foreign_key('order_lineitems_ibfk_3', 'order_lineitems', 'status', ['project_status'], ['id'])
    op.create_foreign_key('order_lineitems_ibfk_4', 'order_lineitems', 'orders', ['orderfk'], ['id'])
    # ### end Alembic commands ###