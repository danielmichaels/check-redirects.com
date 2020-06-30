""" Page blueprint. """
from app.blueprints.page.forms import SearchForm
from flask import Blueprint, render_template
from lib.redirect import RedirectChecker

page = Blueprint("page", __name__, template_folder="templates")


@page.route("/", methods=["GET", "POST"])
def home():
    """ Landing page. """
    form = SearchForm()
    response = None

    if form.validate_on_submit():
        url = form.search.data
        redirects = RedirectChecker(url)
        response = redirects.response_information

    return render_template("page/home.html", form=form, response=response)


@page.route("/terms")
def terms():
    """ Terms of Service page. """
    return render_template("page/terms.html")


@page.route("/privacy")
def privacy():
    """ Privacy Policy page."""
    return render_template("page/privacy.html")
