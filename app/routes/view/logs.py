import os
from flask import Blueprint, render_template, redirect, current_app, url_for, redirect

BLUEPRINT = 'view_logs'
TEMPLATE_BASE = 'view/logs'
bp = Blueprint(BLUEPRINT, __name__)

def render(template_name, *args, **kwargs):
    return render_template(f'{TEMPLATE_BASE}/{template_name}.html', *args, **kwargs)

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

    return redirect(url_for('view_logs.index'))
