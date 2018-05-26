from flask import Blueprint

bp = Blueprint('frontend', __name__)

from webapp.frontend import routes
