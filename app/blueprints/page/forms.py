from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, URL


class SearchForm(FlaskForm):
    search = StringField(
        "Enter a URL to check",
        [
            DataRequired(),
            Length(3, 512),
            URL(
                require_tld=True,
                message="URL missing a valid protocol, or trailing top level domain",
            ),
        ],
    )
