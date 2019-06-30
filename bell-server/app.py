from flask import Flask, url_for
from flask_security import Security, MongoEngineUserDatastore
import os

from helpers import system_wide_template_variables


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        MONGODB_SETTINGS={
            'db': 'bell_server'
        },
        MAX_CONTENT_LENGTH=(16 * 1024 * 1024),
        UPLOAD_FOLDER=os.path.join(app.instance_path, "data"),

        SECURITY_PASSWORD_SALT="dev",
        SECURITY_CONFIRMABLE=False,
        SECURITY_CHANGEABLE=True,
        SECURITY_SEND_REGISTER_EMAIL=False,
        SECURITY_SEND_PASSWORD_CHANGE_EMAIL=False,
        SECURITY_SEND_PASSWORD_RESET_EMAIL=False,
        SECURITY_SEND_PASSWORD_RESET_NOTICE_EMAIL=False,
        SECURITY_POST_LOGIN_VIEW="users.check_password",
        SECURITY_POST_CHANGE_VIEW="users.successful_reset",

        SECURITY_MSG_LOGIN=('Please log in to access this page.', 'error')
    )

    from models import db, User, Role
    db.init_app(app)
    user_datastore = MongoEngineUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
        os.makedirs(app.config['UPLOAD_FOLDER'])
    except OSError:
        pass

    from controllers import dashboard, schedule, templates, settings, users
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(schedule.bp)
    app.register_blueprint(templates.bp)
    app.register_blueprint(settings.bp)
    app.register_blueprint(users.bp)
    app.add_url_rule('/', endpoint='index')

    app.context_processor(system_wide_template_variables)

    return app
