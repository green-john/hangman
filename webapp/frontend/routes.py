from flask import send_file
from webapp.frontend import bp


@bp.route('/')
def index():
    return send_file('frontend/templates/home.html')
