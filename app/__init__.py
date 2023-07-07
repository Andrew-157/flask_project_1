import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    if app.debug:
        app.config.from_object('config.DevelopmentConfig')
    else:
        app.config.from_object('config.ProductionConfig')

    # Import of 'models' module is necessary
    # so that Flask-Migrate detects changes there
    from . import models, main

    # Initialize database and migrations
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(main.bp)

    return app
