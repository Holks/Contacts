import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.jinja_env.globals.update(enumerate=enumerate)
    db.init_app(app)

    migrate.init_app(app, db)
    login.init_app(app)
    login.login_view = 'auth.login'

    from app.registry import bp as registry_bp
    app.register_blueprint(registry_bp, url_prefix='/registry')

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')


    return app

from app import models
