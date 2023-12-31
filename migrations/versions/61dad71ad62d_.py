"""empty message

Revision ID: 61dad71ad62d
Revises: a8e8a8c399b9
Create Date: 2023-07-11 20:14:55.134189

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '61dad71ad62d'
down_revision = 'a8e8a8c399b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('answer_vote', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_upvote', sa.Boolean(), nullable=False))
        batch_op.drop_column('value')

    with op.batch_alter_table('question_vote', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_upvote', sa.Boolean(), nullable=False))
        batch_op.drop_column('value')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question_vote', schema=None) as batch_op:
        batch_op.add_column(sa.Column('value', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
        batch_op.drop_column('is_upvote')

    with op.batch_alter_table('answer_vote', schema=None) as batch_op:
        batch_op.add_column(sa.Column('value', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
        batch_op.drop_column('is_upvote')

    # ### end Alembic commands ###
