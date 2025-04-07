import os
import json
from flask import Blueprint, request, jsonify, render_template, redirect, current_app, url_for
from ita.models import Experiment, Device, Data

BLUEPRINT = 'view_chart'
TEMPLATE_BASE = 'view/chart'
bp = Blueprint(BLUEPRINT, __name__)

def render(template_name, *args, **kwargs):
    return render_template(f'{TEMPLATE_BASE}/{template_name}.html', *args, **kwargs)

@bp.route('/')
def index():
    experiments = Experiment.select()
    return render('index', experiments=experiments)

@bp.route('/<int:id>')
def show(id):
    experiment = Experiment.get_or_none(Experiment.id == id)
    experiment.header = json.loads(experiment.header) if experiment else []

    return render('show', experiment=experiment)
