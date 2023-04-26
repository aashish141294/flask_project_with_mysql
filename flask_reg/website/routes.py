from flask import Blueprint

auth = Blueprint('auth', __name__)
views = Blueprint('views', __name__)
app = Blueprint('app', __name__)