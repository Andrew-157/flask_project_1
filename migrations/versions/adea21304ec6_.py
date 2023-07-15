"""empty message

Revision ID: adea21304ec6
Revises: 8de3996ff324
Create Date: 2023-07-14 20:48:56.361643

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'adea21304ec6'
down_revision = '8de3996ff324'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('answer', schema=None) as batch_op:
        batch_op.drop_constraint('answer_ibfk_1', type_='foreignkey')
        batch_op.drop_constraint('answer_ibfk_2', type_='foreignkey')
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'])
        batch_op.create_foreign_key(None, 'question', ['question_id'], ['id'])

    with op.batch_alter_table('answer_vote', schema=None) as batch_op:
        batch_op.drop_constraint('answer_vote_ibfk_1', type_='foreignkey')
        batch_op.drop_constraint('answer_vote_ibfk_2', type_='foreignkey')
        batch_op.create_foreign_key(None, 'answer', ['answer_id'], ['id'])
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'])

    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.drop_constraint('question_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'])

    with op.batch_alter_table('question_views', schema=None) as batch_op:
        batch_op.drop_constraint('question_views_ibfk_2', type_='foreignkey')
        batch_op.drop_constraint('question_views_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'question', ['question_id'], ['id'])
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'])

    with op.batch_alter_table('question_vote', schema=None) as batch_op:
        batch_op.drop_constraint('question_vote_ibfk_2', type_='foreignkey')
        batch_op.drop_constraint('question_vote_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'question', ['question_id'], ['id'])
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question_vote', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('question_vote_ibfk_1', 'question', ['question_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
        batch_op.create_foreign_key('question_vote_ibfk_2', 'user', ['user_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')

    with op.batch_alter_table('question_views', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('question_views_ibfk_1', 'question', ['question_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
        batch_op.create_foreign_key('question_views_ibfk_2', 'user', ['user_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')

    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('question_ibfk_1', 'user', ['user_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')

    with op.batch_alter_table('answer_vote', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('answer_vote_ibfk_2', 'user', ['user_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
        batch_op.create_foreign_key('answer_vote_ibfk_1', 'answer', ['answer_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')

    with op.batch_alter_table('answer', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('answer_ibfk_2', 'user', ['user_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
        batch_op.create_foreign_key('answer_ibfk_1', 'question', ['question_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')

    # ### end Alembic commands ###