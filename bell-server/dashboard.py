from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

bp = Blueprint('dashboard', __name__)


@bp.route('/')
def hello_world():
    return 'Hello World!'
