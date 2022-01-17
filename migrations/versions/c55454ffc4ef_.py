"""empty message

Revision ID: c55454ffc4ef
Revises: 
Create Date: 2022-01-17 00:46:18.772306

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c55454ffc4ef'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'filament', 'vendors', ['vendorfk'], ['id'])
    op.create_foreign_key(None, 'filament', 'type', ['typefk'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'filament', type_='foreignkey')
    op.drop_constraint(None, 'filament', type_='foreignkey')
    # ### end Alembic commands ###
