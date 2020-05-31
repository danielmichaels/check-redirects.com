import os
from datetime import timedelta
from distutils.util import strtobool

SITE_NAME = os.getenv("COMPOSE_PROJECT_NAME", "my-site")

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")

SECRET_KEY = os.getenv("SECRET_KEY", None)

SERVER_NAME = os.getenv(
    "SERVER_NAME", "localhost:{0}".format(os.getenv("DOCKER_WEB_PORT", "8000"))
)

# SQLAlchemy.
pg_user = os.getenv("POSTGRES_USER", "app")
pg_pass = os.getenv("POSTGRES_PASSWORD", "password")
pg_host = os.getenv("POSTGRES_HOST", "postgres")
pg_port = os.getenv("POSTGRES_PORT", "5432")
pg_db = os.getenv("POSTGRES_DB", pg_user)
db = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
    pg_user, pg_pass, pg_host, pg_port, pg_db
)
SQLALCHEMY_DATABASE_URI = db
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Celery.
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_REDIS_MAX_CONNECTIONS = 5
# CELERYBEAT_SCHEDULE = {
#     'mark-soon-to-expire-credit-cards': {
#         'task': 'app.blueprints.billing.tasks.mark_old_credit_cards',
#         'schedule': crontab(hour=0, minute=0)
#     },
#     'expire-old-coupons': {
#         'task': 'app.blueprints.billing.tasks.expire_old_coupons',
#         'schedule': crontab(hour=0, minute=1)
#     },
# }

# Flask-Mail.
# MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.sendgrid.net")
MAIL_PORT = os.getenv("MAIL_PORT", 587)
MAIL_USE_TLS = bool(strtobool(os.getenv("MAIL_USE_TLS", "true")))
MAIL_USE_SSL = bool(strtobool(os.getenv("MAIL_USE_SSL", "false")))
MAIL_USERNAME = os.getenv("MAIL_USERNAME", None)
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", None)
MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "smtp.gmail.com")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", None)
SENTRY_DSN = os.getenv("SENTRY_DSN", None)

# Flask-Babel.
LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "de": "German",
}
BABEL_DEFAULT_LOCALE = "en"

# User.
SEED_ADMIN_EMAIL = os.getenv("SEED_ADMIN_EMAIL", "dev@local.host")
SEED_ADMIN_PASSWORD = os.getenv("SEED_ADMIN_PASSWORD", "password")
REMEMBER_COOKIE_DURATION = timedelta(days=90)


# Google Analytics.
ANALYTICS_GOOGLE_UA = os.getenv("ANALYTICS_GOOGLE_UA", None)
