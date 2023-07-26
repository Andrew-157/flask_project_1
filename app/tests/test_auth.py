import pytest
from flask import Response
from flask import Flask
from flask_wtf.csrf import generate_csrf
from .. import db
from ..models import User


def test_register(client, app):
    assert client.get('/auth/register/').status_code == 200
    response: Response = client.post(
        '/auth/register/', data={'username': 'random_user',
                                 'email': 'random@gmail.com',
                                 'password': '34somepassword34',
                                 'password1': '34somepassword34'})
    print(response.data)
    assert response.status_code == 302
    with app.app_context():
        assert db.session.query(User).\
            filter_by(username='random_user').first() is not None
