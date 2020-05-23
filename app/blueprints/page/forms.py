from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, URL


class SearchForm(FlaskForm):
    search = StringField("Which URL to check", [DataRequired(), Length(3, 512), URL(require_tld=True, message="Must provide a URL")])
