import os
import json
from flask import Blueprint, request, jsonify, render_template, redirect, current_app, url_for
from ita.models import Experiment, Device, Data
from flasktools import *

bp = auto_blueprint()

@bp.route('/')
def index():
    experiments = Experiment.select()
    return render('index', experiments=experiments)

@bp.route('/<int:id>')
def show(id):
    experiment = Experiment.get_or_none(Experiment.id == id)

    return render('show', experiment=experiment)
