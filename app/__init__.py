# -*- coding: utf-8 -*-

import os

import logging
from logging.handlers import RotatingFileHandler, SMTPHandler

import rq
from flask import Flask, current_app
from flask import request

from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_babel import Babel
from flask_babel import lazy_gettext as _l
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

from elasticsearch import Elasticsearch
from redis import Redis

from config import Config

app = Flask(__name__)
# Flask extensions
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
# login.login_message = 'your msg'
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
socketio = SocketIO()

# for generate pot: pybabel extract -F babel.cfg -k _l -o messages.pot .
# for generate mo: pybabel init -i messages.pot -d app/translations -l <needed lang>
# for update mo: pybabel update -i messages.pot -d app/translations
# for compile po: pybabel compile -d app/translations
babel = Babel()


def create_app(config_class=Config):
    _app = Flask(__name__)
    _app.config.from_object(config_class)

    db.init_app(_app)
    migrate.init_app(_app, db)
    login.init_app(_app)
    mail.init_app(_app)
    bootstrap.init_app(_app)
    moment.init_app(_app)
    babel.init_app(_app)
    socketio.init_app(_app)
    _app.elasticsearch = Elasticsearch([_app.config['ELASTICSEARCH_URL']]) if _app.config['ELASTICSEARCH_URL'] else None
    _app.redis = Redis.from_url(_app.config['REDIS_URL'])
    _app.task_queue = rq.Queue('blogeek-tasks', connection=_app.redis)


    # register scheme of app
    from app.errors import bp as errors_bp
    _app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    _app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    _app.register_blueprint(main_bp)

    from app.api import bp as api_bp
    _app.register_blueprint(api_bp, url_prefix='/api')

    if not _app.debug and not _app.testing:
        # send mails
        if _app.config['MAIL_SERVER']:
            auth = None
            if _app.config['MAIL_USERNAME'] or _app.config['MAIL_PASSWORD']:
                auth = (_app.config['MAIL_USERNAME'], _app.config['MAIL_PASSWORD'])
            secure = None
            if _app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(_app.config['MAIL_SERVER'], _app.config['MAIL_PORT']),
                fromaddr='no-reply@' + _app.config['MAIL_SERVER'],
                toaddrs=_app.config['ADMINS'], subject='Blogeek Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            _app.logger.addHandler(mail_handler)

        # write to file
        if _app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/blogeek.log', maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            _app.logger.addHandler(file_handler)

    return _app


# for auto choice lang
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])


from app import models
