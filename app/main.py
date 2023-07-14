from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .models import Question, Tag, QuestionViews, Answer, QuestionVote, AnswerVote
from . import db

bp = Blueprint('main', __name__)


def split_tags_string(tags: str):
    # Takes a string of tags as an argument
    # and returns list of edited tags
    # For example:
    # 'python 3.x, javascript, ruby on rails ' will be
    # turned in ['python-3.x', 'javascript', 'ruby-on-rails']
    # and returned

    if tags[-1] == ',':
        tags = tags[:-1]
    if tags[0] == ',':
        tags = tags[1:]
    tags_list = tags.split(',')
    for index, tag in enumerate(tags_list):
        tags_list[index] = tag.strip()

    for index, tag in enumerate(tags_list):
        if ' ' in tag:
            tags_list[index] = '-'.join(tag.split(' '))

    return tags_list


def upvote_downvote_question(question_id: int, user_id: int, is_upvote: bool):
    # pass to this function only existing questions
    # and authenticated users
    existing_vote = db.session.query(QuestionVote).\
        filter((QuestionVote.user_id == user_id) &
               QuestionVote.question_id == question_id).first()
    if not existing_vote:
        vote = QuestionVote(user_id=user_id,
                            question_id=question_id,
                            is_upvote=is_upvote)
        db.session.add(vote)
        db.session.commit()
        return None

    if existing_vote:
        if existing_vote.is_upvote == True:
            if is_upvote == True:
                db.session.delete(existing_vote)
                db.session.commit()
                return None
            elif is_upvote == False:
                existing_vote.is_upvote = False
                db.session.commit()
                return None
        elif existing_vote.is_upvote == False:
            if is_upvote == False:
                db.session.delete(existing_vote)
                db.session.commit()
                return None
            elif is_upvote == True:
                existing_vote.is_upvote = True
                db.session.commit()
                return None


def upvote_downvote_answer(answer_id: int, user_id: int, is_upvote: bool):
    existing_vote = db.session.query(AnswerVote).\
        filter((AnswerVote.answer_id == answer_id) &
               (AnswerVote.user_id == user_id)).first()

    if not existing_vote:
        vote = AnswerVote(
            answer_id=answer_id,
            user_id=user_id,
            is_upvote=is_upvote
        )
        db.session.add(vote)
        db.session.commit()
        return None

    if existing_vote:
        if existing_vote.is_upvote == True:
            if is_upvote == True:
                db.session.delete(existing_vote)
                db.session.commit()
                return None
            if is_upvote == False:
                existing_vote.is_upvote = False
                db.session.commit()
                return None
        if existing_vote.is_upvote == False:
            if is_upvote == False:
                db.session.delete(existing_vote)
                db.session.commit()
                return None
            if is_upvote == True:
                existing_vote.is_upvote = True
                db.session.commit()
                return None


@bp.route('/')
def index():
    return render_template('main/index.html')


@bp.route('/questions/ask', methods=['GET', 'POST'])
@login_required
def post_question():
    if request.method == 'POST':
        title = request.form['title']
        details = request.form['details']
        tags = request.form['tags']
        errors = False

        if not title:
            flash('Title is required to post a question.')
            errors = True

        if title and len(title) > 300:
            flash('Title is too long.')
            errors = True

        if title and len(title) < 15:
            flash('Title is too short')
            errors = True

        if errors:
            return render_template('main/post_question.html',
                                   title=title, details=details, tags=tags)

        question = Question(title=title,
                            details=details if details else None,
                            user_id=current_user.id)
        db.session.add(question)

        if tags:
            tags = split_tags_string(tags)
            for tag in tags:
                existing_tag = db.session.execute(
                    db.select(Tag).filter_by(name=tag)).scalar_one_or_none()
                if existing_tag:
                    question.tags.append(existing_tag)
                else:
                    new_tag = Tag(name=tag)
                    question.tags.append(new_tag)
                    db.session.add(new_tag)

        db.session.commit()

        flash('You successfully asked new question!', 'success')
        return redirect(url_for('main.index'))

    return render_template('main/post_question.html')


@bp.route('/questions/<int:id>/update/', methods=['GET', 'POST'])
@login_required
def update_question(id):
    question = db.session.query(Question).\
        options(db.joinedload(Question.tags)).\
        filter_by(id=id).first()

    if not question:
        return render_template('nonexistent.html')

    if question.user != current_user:
        return render_template('not_allowed.html')

    if request.method == 'GET':

        if question.tags:
            tags_list = list(question.tags)
            for index, tag in enumerate(tags_list):
                tags_list[index] = tag.name
            tags = ','.join(tags_list)

        return render_template('main/update_question.html',
                               question=question,
                               tags=tags)

    if request.method == 'POST':

        title = request.form['title']
        details = request.form['details']
        tags = request.form['tags']
        errors = False

        if not title:
            flash('Title is required')
            errors = True

        if title and len(title) > 300:
            flash('Title is too long.')
            errors = True

        if title and len(title) < 10:
            flash('Title is too short.')
            errors = True

        if errors:
            return render_template('main/update_question.html',
                                   question=question, tags=tags)

        question.title = title
        question.details = details
        question.updated = datetime.utcnow()

        if tags:
            tags = split_tags_string(tags)
            tag_objects = []
            for tag in tags:
                existing_tag = db.session.execute(
                    db.select(Tag).filter_by(name=tag)).first()
                if existing_tag:
                    tag_objects.append(existing_tag)
                else:
                    new_tag = Tag(name=tag)
                    tag_objects.append(new_tag)
                    db.session.add(new_tag)

            question.tags.clear()

            for tag_object in tag_objects:
                question.tags.append(tag_object)

        db.session.commit()
        flash('You successfully updated your question.', 'success')
        return redirect(url_for('main.index'))


@bp.route('/questions/<int:id>/', methods=['GET'])
def question_detail(id):

    question = db.session.query(Question).\
        options(db.joinedload(Question.times_viewed), db.joinedload(Question.user)).\
        filter_by(id=id).first()

    if not question:
        return render_template('nonexistent.html')

    upvotes = db.session.query(QuestionVote).filter(
        (QuestionVote.question_id == question.id) &
        (QuestionVote.is_upvote == True)
    ).count()
    downvotes = db.session.query(QuestionVote).\
        filter(
        (QuestionVote.question_id == question.id) &
        (QuestionVote.is_upvote == False)
    ).count()

    if current_user.is_authenticated:
        question_views_obj = QuestionViews.query.filter(
            (QuestionViews.user_id == current_user.id)
            & (QuestionViews.question_id == question.id)
        ).first()
        if not question_views_obj:
            question_views_obj = QuestionViews(
                user_id=current_user.id,
                question_id=question.id
            )
            db.session.add(question_views_obj)
            db.session.commit()

        voting_status = db.session.query(QuestionVote).filter(
            (QuestionVote.question_id == question.id) &
            (QuestionVote.user_id == current_user.id)
        ).first()

    else:
        voting_status = None

    answers = db.session.query(Answer).options(
        db.joinedload(Answer.user)
    ).filter_by(question_id=question.id).all()

    answers_upvotes = {}
    answers_downvotes = {}
    for answer in answers:
        answers_upvotes[answer.id] = db.session.query(AnswerVote).filter(
            (AnswerVote.answer_id == answer.id) &
            (AnswerVote.is_upvote == True)
        ).count()
        answers_downvotes[answer.id] = db.session.query(AnswerVote).filter(
            (AnswerVote.answer_id == answer.id) &
            (AnswerVote.is_upvote == False)
        ).count()

    answer_votes_user = {}
    for answer in answers:
        user_vote = db.session.query(AnswerVote).filter(
            (AnswerVote.answer_id == answer.id) &
            (AnswerVote.user_id == current_user.id)
        ).first()
        if user_vote:
            answer_votes_user[answer.id] = user_vote

    return render_template('main/question_detail.html', question=question,
                           voting_status=voting_status, upvotes=upvotes,
                           downvotes=downvotes,
                           answers=answers,
                           answers_upvotes=answers_upvotes,
                           answers_downvotes=answers_downvotes,
                           answer_votes_user=answer_votes_user)


@bp.route('/questions/<int:id>/delete/', methods=['GET', 'POST'])
@login_required
def delete_question(id):
    if request.method == 'POST':
        question = db.session.query(Question).\
            filter_by(id=id).first()

        if not question:
            return render_template('nonexistent.html')

        if question.user_id != current_user.id:
            return render_template('not_allowed.html')

        db.session.delete(question)
        db.session.commit()

        flash('You successfully deleted your question.', 'success')
        return redirect(url_for('main.index'))

    if request.method == 'GET':
        return render_template('not_allowed.html')


@bp.route('/questions/<int:id>/upvote/', methods=['POST', 'GET'])
def upvote_question(id):
    if request.method == 'POST':
        question = db.session.query(Question).filter_by(id=id).first()

        if not question:
            return render_template('nonexistent.html')

        if not current_user.is_authenticated:
            flash('You have to authenticate to vote for a question', 'info')
        else:
            upvote_downvote_question(question_id=question.id,
                                     user_id=current_user.id, is_upvote=True)

        return redirect(url_for('main.question_detail', id=question.id))

    elif request.method == 'GET':
        return render_template('main/not_allowed.html')


@bp.route('/questions/<int:id>/downvote/', methods=['POST', 'GET'])
def downvote_question(id):
    if request.method == 'POST':
        question = db.session.query(Question).filter_by(id=id).first()

        if not question:
            return render_template('nonexistent.html')

        if not current_user.is_authenticated:
            flash('You have to authenticate to vote for a question', 'info')
        else:
            upvote_downvote_question(question_id=question.id,
                                     user_id=current_user.id, is_upvote=False)

        return redirect(url_for('main.question_detail', id=question.id))

    elif request.method == 'GET':
        return render_template('main/not_allowed.html')


@bp.route('/tags/<tag>/', methods=['GET'])
def questions_by_tag(tag):
    tag_object = db.session.query(Tag).\
        filter_by(name=tag).first()

    if not tag_object:
        return render_template('main/questions_by_tag.html', tag=tag, questions=[])

    questions = db.session.query(Question).\
        options(db.joinedload(Question.tags),
                db.joinedload(Question.user),
                db.joinedload(Question.times_viewed)).\
        filter(Question.tags.contains(tag_object)).\
        order_by(Question.asked.desc()).\
        all()

    answers_count = {}
    votes_count = {}
    for question in questions:
        answers_count[question.id] = db.session.query(Answer). \
            filter_by(question_id=question.id).count()
        votes_count[question.id] = db.session.query(QuestionVote).\
            filter_by(question_id=question.id).count()

    return render_template('main/questions_by_tag.html', tag=tag,
                           questions=questions,
                           answers_count=answers_count,
                           votes_count=votes_count)


@bp.route('/questions/<int:question_id>/answer/', methods=['POST', 'GET'])
def post_answer(question_id):
    if request.method == 'POST':
        question = db.session.query(Question).\
            filter_by(id=question_id).first()

        if not question:
            return render_template('nonexistent.html')

        if not current_user.is_authenticated:
            flash(
                'To leave an answer for a question, become an authenticated user.', 'info')
            return redirect(url_for('main.question_detail', id=question.id))

        content = request.form['content']
        errors = False

        if not content:
            flash('To publish an answer, you need to provide content for it.')
            errors = True

        if content and len(content) < 15:
            flash('Content of your answer is too short.')
            errors = True

        if errors:
            return render_template('main/post_answer.html',
                                   content=content,
                                   question=question)

        answer = Answer(content=content,
                        user_id=current_user.id,
                        question_id=question.id)

        db.session.add(answer)
        db.session.commit()

        flash('You successfully published your answer.', 'success')

        return redirect(url_for('main.question_detail', id=question.id))

    if request.method == 'GET':
        question = db.session.query(Question).\
            filter_by(id=question_id).first()

        if not question:
            return render_template('nonexistent.html')

        if not current_user.is_authenticated:
            flash(
                'To leave an answer for a question, become an authenticated user.', 'info'
            )
            return redirect('main.question_detail', id=question.id)

        return render_template('main/post_answer.html',
                               question=question)


@bp.route('/answers/<int:id>/update/', methods=['POST', 'GET'])
@login_required
def update_answer(id):
    answer = db.session.query(Answer).\
        options(db.joinedload(Answer.question)).\
        filter_by(id=id).first()

    if not answer:
        return render_template('main/nonexistent.html')

    if answer.user_id != current_user.id:
        return render_template('main/not_allowed.html')

    if request.method == 'POST':
        content = request.form['content']
        errors = False

        if not content:
            flash('You cannot update your answer to be empty.')
            errors = True

        if content and len(content) < 15:
            flash('Content of your answer is too short.')
            errors = True

        if errors:
            return render_template('main/update_answer.html',
                                   content=content,
                                   answer=answer,
                                   question=answer.question)

        answer.content = content
        answer.updated = datetime.utcnow()

        db.session.commit()

        flash('You successfully updated your answer.', 'success')

        return redirect(url_for('main.question_detail', id=answer.question_id))

    if request.method == 'GET':
        return render_template('main/update_answer.html', content=answer.content,
                               answer=answer,
                               question=answer.question)


@bp.route('/answers/<int:id>/delete/', methods=['GET', 'POST'])
@login_required
def delete_answer(id):
    if request.method == 'POST':
        answer = db.session.query(Answer).\
            filter_by(id=id).first()

        if not answer:
            return render_template('nonexistent.html')

        if current_user.id != answer.user_id:
            return render_template('not_allowed.html')

        question_id = answer.question_id

        db.session.delete(answer)
        db.session.commit()

        flash('You successfully deleted your answer.', 'success')

        return redirect(url_for('main.question_detail', id=question_id))

    if request.method == 'GET':
        return render_template('not_allowed.html')


@bp.route('/answers/<int:id>/upvote/', methods=['GET', 'POST'])
def upvote_answer(id):
    if request.method == 'POST':
        answer = db.session.query(Answer).\
            filter_by(id=id).first()

        if not answer:
            return render_template('main/nonexistent.html')

        if not current_user.is_authenticated:
            flash('To vote for an answer, become authenticated user.', 'info')
        else:
            upvote_downvote_answer(answer.id, current_user.id, is_upvote=True)

        return redirect(url_for('main.question_detail', id=answer.question_id))

    if request.method == 'GET':
        return render_template('main/not_allowed.html')


@bp.route('/answers/<int:id>/downvote/', methods=['GET', 'POST'])
def downvote_answer(id):
    if request.method == 'POST':
        answer = db.session.query(Answer).\
            filter_by(id=id).first()

        if not answer:
            return render_template('main/nonexistent.html')

        if not current_user.is_authenticated:
            flash('To vote for an answer, become authenticated user.', 'info')
        else:
            upvote_downvote_answer(answer.id, current_user.id, is_upvote=False)

        return redirect(url_for('main.question_detail', id=answer.question_id))

    if request.method == 'GET':
        return render_template('main/not_allowed.html')
