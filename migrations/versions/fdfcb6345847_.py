"""empty message

Revision ID: fdfcb6345847
Revises: dbff74b69a93
Create Date: 2022-04-05 23:29:17.858844

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fdfcb6345847'
down_revision = 'dbff74b69a93'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('machine', sa.Column('c_roi_per_min', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('machine', 'c_roi_per_min')
    # ### end Alembic commands ###
