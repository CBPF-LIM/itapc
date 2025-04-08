import os
from flask import Blueprint, render_template, redirect, current_app, url_for, redirect
from flasktools import *

bp = auto_blueprint()

@bp.route('/', methods=['GET'])
def index():
    return render('index')
