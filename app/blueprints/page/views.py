from flask import Blueprint, render_template, request, flash, url_for, redirect

from app.blueprints.page.forms import SearchForm
from app.blueprints.redirect.redirect import RedirectChecker

page = Blueprint('page', __name__, template_folder='templates')


@page.route('/', methods=['GET','POST'])
def home():
    form = SearchForm()
    response = None

    if form.validate_on_submit():
        url = form.search.data
        redirects = RedirectChecker(url)
        print(redirects.json_list)
        # todo: return json objects or json error
        response = redirects.json_list

    return render_template('page/home.html', form=form, response=response)


@page.route('/terms')
def terms():
    return render_template('page/terms.html')


@page.route('/privacy')
def privacy():
    return render_template('page/privacy.html')
