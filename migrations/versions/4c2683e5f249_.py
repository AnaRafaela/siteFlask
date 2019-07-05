"""empty message

Revision ID: 4c2683e5f249
Revises: 249ea66a1377
Create Date: 2019-06-07 13:14:06.987561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c2683e5f249'
down_revision = '249ea66a1377'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('agenda',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name_event', sa.String(length=64), nullable=True),
    sa.Column('local', sa.String(length=64), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('agenda')
    # ### end Alembic commands ###
