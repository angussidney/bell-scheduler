from flask import (
    Blueprint, redirect, render_template, request, url_for
)

bp = Blueprint('settings', __name__, url_prefix='/settings')


@bp.route('/')
def settings():
    return render_template('settings/index.html')
