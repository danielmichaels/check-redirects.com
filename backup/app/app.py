""" Flask App. """
import logging
from logging.handlers import SMTPHandler

import sentry_sdk
from app.blueprints.contact import contact
from app.blueprints.page import page
from app.extensions import (
    debug_toolbar,
    mail,
    csrf,
    db,
    limiter,
    babel,
    flask_static_digest,
)
from celery import Celery
from cli import register_cli_commands
from config.settings import SENTRY_DSN
from flask import Flask, render_template
from lib.template_processors import current_year
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from werkzeug.debug import DebuggedApplication
from werkzeug.middleware.proxy_fix import ProxyFix

sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[
        FlaskIntegration(),
        CeleryIntegration(),
        RedisIntegration(),
        SqlalchemyIntegration(),
    ],
)

CELERY_TASK_LIST = [
    "app.blueprints.contact.tasks",
]


def create_celery_app(app=None):
    """
    Create a new Celery object and tie together the Celery config to the app's
    config. Wrap all tasks in the context of the application.

    :param app: Flask app
    :return: Celery app
    """
    app = app or create_app()

    celery = Celery(
        app.import_name,
        broker=app.config["CELERY_BROKER_URL"],
        include=CELERY_TASK_LIST,
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):  # pylint: disable=too-few-public-methods
        """ Create celery ctx base. """
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__, static_folder="../public", static_url_path="")

    app.config.from_object("config.settings")

    if settings_override:
        app.config.update(settings_override)

    middleware(app)
    error_templates(app)
    exception_handler(app)
    app.register_blueprint(page)
    app.register_blueprint(contact)
    template_processors(app)
    extensions(app)
    register_cli_commands(app)

    if app.debug:
        app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

    return app


def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    debug_toolbar.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    db.init_app(app)
    limiter.init_app(app)
    babel.init_app(app)
    flask_static_digest.init_app(app)


def template_processors(app):
    """
    Register 0 or more custom template processors (mutates the app passed in).

    :param app: Flask application instance
    :return: App jinja environment
    """
    app.jinja_env.globals.update(current_year=current_year)

    return app.jinja_env


def middleware(app):
    """
    Register 0 or more middleware (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    # Swap request.remote_addr with the real IP address even if behind a proxy.
    app.wsgi_app = ProxyFix(app.wsgi_app)


def error_templates(app):
    """
    Register 0 or more custom error pages (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """

    def render_status(status):
        """
         Render a custom template for a specific status.
           Source: http://stackoverflow.com/a/30108946

         :param status: Status as a written name
         :type status: str
         :return: None
         """
        # Get the status code from the status, default to a 500 so that we
        # catch all types of errors and treat them as a 500.
        code = getattr(status, "code", 500)
        return render_template("errors/{0}.html".format(code)), code

    for error in [404, 429, 500]:
        app.errorhandler(error)(render_status)


def exception_handler(app):
    """
    Register 0 or more exception handlers (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    mail_handler = SMTPHandler(
        (app.config.get("MAIL_SERVER"), app.config.get("MAIL_PORT")),
        app.config.get("MAIL_USERNAME"),
        [app.config.get("MAIL_USERNAME")],
        "[Exception handler] A 5xx was thrown",
        (app.config.get("MAIL_USERNAME"), app.config.get("MAIL_PASSWORD")),
        secure=(),
    )

    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(
        logging.Formatter(
            """
    Time:               %(asctime)s
    Message type:       %(levelname)s


    Message:

    %(message)s
    """
        )
    )
    app.logger.addHandler(mail_handler)
