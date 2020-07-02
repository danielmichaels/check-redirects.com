from flask_babel import Babel
from flask_debugtoolbar import DebugToolbarExtension
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_static_digest import FlaskStaticDigest
from flask_wtf import CSRFProtect

debug_toolbar = DebugToolbarExtension()
mail = Mail()
csrf = CSRFProtect()
db = SQLAlchemy()
limiter = Limiter(key_func=get_remote_address)
babel = Babel()
flask_static_digest = FlaskStaticDigest()