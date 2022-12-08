"""init migration

Revision ID: fc828bb1ee45
Revises: 
Create Date: 2022-12-08 15:45:37.342389

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc828bb1ee45'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_model',
    sa.Column('UserID', sa.Integer(), nullable=False),
    sa.Column('Username', sa.String(length=16), nullable=False, unique=True),
    sa.Column('Password', sa.String(length=16), nullable=False),
    sa.Column('ImageUrl', sa.String(length=300), nullable=True),
    sa.PrimaryKeyConstraint('UserID')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_model')
    # ### end Alembic commands ###
