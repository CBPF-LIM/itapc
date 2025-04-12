import os
from flask import redirect
from tools.flasktools import *

bp = auto_blueprint()

@bp.route('/', methods=['GET'])
def index():
    # open error log if exists
    if os.path.exists('error.log'):
        with open('error.log', 'r') as f:
            logs = f.readlines()
    else:
        logs = []

    return render('index', logs=logs)

@bp.route('/destroy', methods=['GET'])
def destroy():
    with open('error.log', 'w') as f:
        f.write('')

    print('Error log destroyed')

    return redirect(action_for('.index'))
