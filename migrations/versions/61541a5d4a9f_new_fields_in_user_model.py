"""new fields in user model

Revision ID: 61541a5d4a9f
Revises: 4a879894acdf
Create Date: 2020-06-10 23:03:42.761249

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61541a5d4a9f'
down_revision = '4a879894acdf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about_me', sa.String(length=140), nullable=True))
    op.add_column('user', sa.Column('last_seen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_seen')
    op.drop_column('user', 'about_me')
    # ### end Alembic commands ###
