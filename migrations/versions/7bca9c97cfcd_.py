"""empty message

Revision ID: 7bca9c97cfcd
Revises: 751641e0748b
Create Date: 2022-04-04 22:04:13.119905

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7bca9c97cfcd'
down_revision = '751641e0748b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('filament', sa.Column('fil_status', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'filament', 'status', ['fil_status'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'filament', type_='foreignkey')
    op.drop_column('filament', 'fil_status')
    # ### end Alembic commands ###
