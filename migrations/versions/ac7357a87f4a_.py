"""empty message

Revision ID: ac7357a87f4a
Revises: a74b4a0e1c33
Create Date: 2023-07-09 17:52:59.779127

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ac7357a87f4a'
down_revision = 'a74b4a0e1c33'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tag', schema=None) as batch_op:
        batch_op.drop_column('slug')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tag', schema=None) as batch_op:
        batch_op.add_column(sa.Column('slug', mysql.VARCHAR(length=80), nullable=True))

    # ### end Alembic commands ###