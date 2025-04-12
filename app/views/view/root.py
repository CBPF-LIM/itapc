from flask import redirect
from flasktools import *

bp = auto_blueprint()

@bp.route('/', methods=['GET'])
def index():
    return redirect(action_for('app/views/view/experiments.index'))
