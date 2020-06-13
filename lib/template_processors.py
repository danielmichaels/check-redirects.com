""" Jinja2 template filters and processors. """
import datetime

import pytz


def current_year():
    """
    Return this year.

    :return: int
    """
    return datetime.datetime.now(pytz.utc).year
