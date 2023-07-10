from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .models import Question, Tag
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

        if title and len(title) < 10:
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

    if request.method == 'GET':
        # Tried to add some optimization on queries using
        # joinedload instead of default lazy
        question = db.session.query(Question).\
            options(db.joinedload(Question.tags), db.joinedload(Question.user)).\
            filter_by(id=id).first()

        if not question:
            return render_template('nonexistent.html')

        if question.user != current_user:
            return render_template('not_allowed.html')

        if question.tags:
            tags_list = list(question.tags)
            for index, tag in enumerate(tags_list):
                tags_list[index] = tag.name
            tags = ','.join(tags_list)

        return render_template('main/update_question.html',
                               question=question,
                               tags=tags)

    if request.method == 'POST':
        question = db.session.query(Question).\
            options(db.joinedload(Question.tags), db.joinedload(Question.user)).\
            filter_by(id=id).first()

        if not question:
            return render_template('nonexistent.html')

        if question.user != current_user:
            return render_template('not_allowed.html')

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
                    db.select(Tag).filter_by(name=tag)).scalar_one_or_none()
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
        options(db.joinedload(Question.tags), db.joinedload(Question.user)).\
        filter_by(id=id).first()

    if not question:
        return render_template('nonexistent.html')

    # if current_user.is_authenticated:
    #     question.times_viewed += 1
    #     db.session.commit()
    # Do not forget to create a button with 'post' method
    # that will send request to a view that will add views to question
    # so that when reloading page on question_detail, views are not
    # increased all the time

    return render_template('main/question_detail.html', question=question)
