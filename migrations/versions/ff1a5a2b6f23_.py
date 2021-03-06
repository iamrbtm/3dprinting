"""empty message

Revision ID: ff1a5a2b6f23
Revises: 8f005df575b0
Create Date: 2022-04-28 21:54:09.156365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff1a5a2b6f23'
down_revision = '8f005df575b0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('filament', sa.Column('aprox_remaining_length', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('filament', 'aprox_remaining_length')
    # ### end Alembic commands ###
