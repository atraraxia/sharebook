
from flask import Blueprint, render_template

web = Blueprint('views', __name__)


@web.app_errorhandler(404)
def not_fond(e):
    print(e)
    return render_template('404.html'), 404
