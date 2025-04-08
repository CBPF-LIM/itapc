import os
import json
from flask import Blueprint, render_template, current_app
from ita.models import Experiment
from flasktools import *

bp = auto_blueprint()

@bp.route('/')
def index():
    experiments = Experiment.select()
    return render('index', experiments=experiments)

@bp.route('/<int:id>')
def show(id):
    experiment = Experiment.get_or_none(Experiment.id == id)
    experiment.header = json.loads(experiment.header) if experiment else []

    return render('show', experiment=experiment)
