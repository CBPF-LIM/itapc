import os
from flask import Blueprint, jsonify, render_template, current_app
from ita.models import Experiment, Device, Data

BLUEPRINT = 'view_table'
TEMPLATE_BASE = 'view/table'

bp = Blueprint(BLUEPRINT, __name__)

def render(template_name, *args, **kwargs):
    return render_template(f'{TEMPLATE_BASE}/{template_name}.html', *args, **kwargs)

def emitter(event, data):
    return current_app.socketio.emit(event, data)

@bp.route('/')
def index():
    experiments = Experiment.select()
    return render('index', experiments=experiments)

@bp.route('/<int:id>')
def show(id):
    experiment = Experiment.get_or_none(Experiment.id == id)

    return render('show', experiment=experiment)


@bp.route('/<int:id>/refresh/<int:index>')
def refresh(id, index):
    rows = Data.select().where(Data.id >= index)
    cols = [ {"id": d.id, "cols": d.cols} for d in rows]
    data = {'response': 'success', 'type': 'GET', 'cols': cols}

    if index == 0:
        data['header'] = rows.first().experiment.header

    return jsonify(data)
