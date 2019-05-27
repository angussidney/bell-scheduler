from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

bp = Blueprint('templates', __name__, url_prefix='/templates')


@bp.route('/create')
def create():
    return render_template('templates/create.html')
