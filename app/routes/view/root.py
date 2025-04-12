from flask import Blueprint, redirect, render_template, url_for
from flasktools import *

bp = auto_blueprint()

@bp.route('/', methods=['GET'])
def index():
    return redirect(action_for('app/routes/view/experiments.index'))
