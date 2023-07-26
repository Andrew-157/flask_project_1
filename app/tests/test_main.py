import pytest
from flask import Response
from .conftest import AuthActions
from .. import db
from ..models import User


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


@pytest.mark.parametrize(('title', 'details', 'tags', 'message'),
                         (
    ('', '', '', b'Title is required to post a question.'),
    ('dfrg', '', '', b'Title is too short.')
))
def test_post_question_validate_input(client, auth: AuthActions, title, details, tags, message):
    auth.login()
    response: Response = client.post('/questions/ask/',
                                     data={'title': title,
                                           'details': details,
                                           'tags': tags})
    assert response.status_code == 200
    assert message in response.data


def test_post_question_for_not_logged_user(client):
    response = client.get('/questions/ask/')
    with client.session_transaction() as session:
        messages = dict(session['_flashes'])
    assert response.status_code == 302
    assert response.headers['Location'] == '/'
    assert messages['info'] == 'You need to be authenticated to ask a question.'
