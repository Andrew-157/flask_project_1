"""empty message

Revision ID: 106cbd4b282e
Revises: b835ba6eb212
Create Date: 2023-08-10 17:58:41.108491

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '106cbd4b282e'
down_revision = 'b835ba6eb212'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('answer_vote', schema=None) as batch_op:
        batch_op.create_unique_constraint('user_answer_vote_uc', ['user_id', 'answer_id'])

    with op.batch_alter_table('question_views', schema=None) as batch_op:
        batch_op.create_unique_constraint('user_question_views_uc', ['user_id', 'question_id'])

    with op.batch_alter_table('question_vote', schema=None) as batch_op:
        batch_op.create_unique_constraint('user_question_vote_uc', ['user_id', 'question_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question_vote', schema=None) as batch_op:
        batch_op.drop_constraint('user_question_vote_uc', type_='unique')

    with op.batch_alter_table('question_views', schema=None) as batch_op:
        batch_op.drop_constraint('user_question_views_uc', type_='unique')

    with op.batch_alter_table('answer_vote', schema=None) as batch_op:
        batch_op.drop_constraint('user_answer_vote_uc', type_='unique')

    # ### end Alembic commands ###