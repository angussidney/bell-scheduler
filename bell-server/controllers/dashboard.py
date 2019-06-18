from flask import (
    Blueprint
)

bp = Blueprint('dashboard', __name__)


@bp.route('/')
def hello_world():
    return 'Hello World! Dashboard time!'
