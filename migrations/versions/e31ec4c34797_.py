"""empty message

Revision ID: e31ec4c34797
Revises: 0504cebc5441
Create Date: 2022-04-18 02:15:56.596787

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e31ec4c34797'
down_revision = '0504cebc5441'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('status', sa.Column('fgcolor', sa.String(length=10), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('status', 'fgcolor')
    # ### end Alembic commands ###
