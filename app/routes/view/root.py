from flask import Blueprint, redirect, render_template, url_for

BLUEPRINT = 'view_root'
TEMPLATE_BASE = 'view/root'
bp = Blueprint(BLUEPRINT, __name__)

def render(template_name, *args, **kwargs):
    return render_template(f'{TEMPLATE_BASE}/{template_name}.html', *args, **kwargs)

@bp.route('/', methods=['GET'])
def index():
    return redirect(url_for('view_table.index'))
