import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    if app.debug:
        app.config.from_object('config.DevelopmentConfig')
    else:
        app.config.from_object('config.ProductionConfig')

    # Import of 'models' module is necessary
    # so that Flask-Migrate detects changes there
    from . import models, main, auth

    # Initialize database and migrations
    db.init_app(app)
    migrate.init_app(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def login_user(user_id):
        return models.User.query.get(int(user_id))

    # Enable CSRF-protection globally for application
    csrf.init_app(app)

    # Register blueprints
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)

    return app
