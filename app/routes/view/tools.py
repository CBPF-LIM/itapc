import os
from flask import Blueprint, render_template, redirect, current_app, url_for, redirect

BLUEPRINT = 'view_tools'
TEMPLATE_BASE = 'view/tools'
bp = Blueprint(BLUEPRINT, __name__)

def render(template_name, *args, **kwargs):
    return render_template(f'{TEMPLATE_BASE}/{template_name}.html', *args, **kwargs)

@bp.route('/', methods=['GET'])
def index():
    return render('index')
