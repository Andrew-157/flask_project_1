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
    if tags:
        if tags[-1] == ',':
            tags = tags[:-1]
        tags_list = tags.split(',')
        print(tags_list)
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
                    continue
                else:
                    tag = Tag(name=tag)
                    question.tags.append(tag)
                    db.session.add(tag)

        db.session.commit()

        flash('You successfully asked new question!', 'success')
        return redirect(url_for('main.index'))

    return render_template('main/post_question.html')
