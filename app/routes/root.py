from flask import Blueprint, redirect, url_for

bp = Blueprint('root', __name__)

@bp.route('/', methods=['GET'])
def app_index():
    return redirect(url_for('view.view_route'))
