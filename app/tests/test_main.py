import pytest
from flask import Response
from werkzeug.security import generate_password_hash
from .conftest import AuthActions
from .. import db
from ..models import User, Question


def test_index(client, auth: AuthActions):
    response: Response = client.get('/')
    assert response.status_code == 200
    assert b'Register' in response.data
    assert b'Login' in response.data

    auth.login()
    response: Response = client.get('/')
    assert response.status_code == 200
    assert b'Logout' in response.data
    assert b'Change profile' in response.data


def test_post_question(client, auth: AuthActions):
    auth.login()
    assert client.get('/questions/ask/').status_code == 200
    response: Response = client.post('/questions/ask/',
                                     data={'title': 'How to iterate through Python List?',
                                           'details': 'I am only starting to learn Python,\
                                do not know how to iterate through list',
                                           'tags': 'python, iteration, programming'})
    with client.session_transaction() as session:
        messages = dict(session['_flashes'])
    assert response.status_code == 302
    assert response.headers['Location'] == '/'
    assert messages['success'] == 'You successfully asked new question!'


@pytest.mark.parametrize(('title', 'message'),
                         (
    ('', b'Title is required to post a question.'),
    ('dfrg',  b'Title is too short.')
))
def test_post_question_validate_input(client, auth: AuthActions, title, message):
    auth.login()
    response: Response = client.post('/questions/ask/',
                                     data={'title': title,
                                           'details': '',
                                           'tags': ''})
    assert response.status_code == 200
    assert message in response.data


def test_post_question_for_not_logged_user(client):
    response = client.get('/questions/ask/')
    with client.session_transaction() as session:
        messages = dict(session['_flashes'])
    assert response.status_code == 302
    assert response.headers['Location'] == '/'
    assert messages['info'] == 'You need to be authenticated to ask a question.'


def test_update_question(client, app, auth: AuthActions):
    with app.app_context():
        test_user = db.session.query(User).\
            filter_by(username='test_user').first()
        question = Question(user=test_user,
                            title='How to iterate through Python List?')
        db.session.add(question)
        db.session.commit()
        db.session.refresh(question)

    auth.login()
    assert client.get(f'/questions/{question.id}/update/').status_code == 200
    response = client.post(f'/questions/{question.id}/update/',
                           data={'title': 'How to create index for a row in MySQL?',
                                 'details': '',
                                 'tags': ''})
    with client.session_transaction() as session:
        messages = dict(session['_flashes'])
    assert response.status_code == 302
    assert response.headers['Location'] == f'/questions/{question.id}/'
    assert messages['success'] == 'You successfully updated your question.'
    with app.app_context():
        question = db.session.query(Question).\
            filter_by(title='How to create index for a row in MySQL?').first()
        assert question != None
        assert question.updated != None


@pytest.mark.parametrize(('title', 'message'),
                         (
    ('', b'Title is required.'),
    ('dfrg', b'Title is too short.')
))
def test_update_question_validate_input(app, client, auth: AuthActions, title, message):
    with app.app_context():
        test_user = db.session.query(User).\
            filter_by(username='test_user').first()
        question = Question(user=test_user,
                            title='How to iterate through Python List?')
        db.session.add(question)
        db.session.commit()
        db.session.refresh(question)

    auth.login()
    assert client.get(f'/questions/{question.id}/update/').status_code == 200
    response = client.post(f'/questions/{question.id}/update/',
                           data={'title': title,
                                 'details': '',
                                 'tags': ''})
    assert response.status_code == 200
    assert message in response.data


def test_update_question_by_user_that_does_not_own_question(app, client, auth: AuthActions):
    with app.app_context():
        test_user = db.session.query(User).\
            filter_by(username='test_user').first()
        question = Question(user=test_user,
                            title='How to iterate through Python List?')
        new_user = User(username='some_user',
                        email='some_user@gmail.com',
                        password=generate_password_hash('34somepassword34'))
        db.session.add(question)
        db.session.add(new_user)
        db.session.commit()
        db.session.refresh(question)

    auth.login(email='some_user@gmail.com', password='34somepassword34')
    assert client.get(f'/questions/{question.id}/update/').status_code == 403


def test_update_question_for_not_logged_user(client, app):
    with app.app_context():
        test_user = db.session.query(User).\
            filter_by(username='test_user').first()
        question = Question(user=test_user,
                            title='How to iterate through Python List?')
        db.session.add(question)
        db.session.commit()
        db.session.refresh(question)

    response = client.get(f'/questions/{question.id}/update/')
    assert response.status_code == 302
    assert (response.headers["Location"].startswith('/auth/login/'))


def test_update_nonexistent_question(client, app, auth: AuthActions):
    auth.login()
    response = client.get('/questions/7890/update/')
    assert response.status_code == 404
