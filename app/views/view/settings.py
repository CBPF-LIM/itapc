from flask import redirect, request, flash
from tools.flasktools import *
from app.models import Setting
import json

bp = auto_blueprint()

@bp.route('/', methods=['GET'])
def index():
    settings = Setting.select()
    return render('index', settings=settings)

@bp.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    setting = Setting.select().where(Setting.id == id).first()
    return render('edit', setting=setting)

@bp.route('/new', methods=['GET'])
def new():
    setting = Setting()
    setting.config = {}
    return render('new', setting=setting)

@bp.route('/', methods=['POST'])
def create():
    setting = Setting()

    name = request.form.get('name', 'Untitled')
    keys = request.form.getlist('keys[]')
    values = request.form.getlist('values[]')

    new_config = generate_config(keys, values)
    if new_config is None:
        return redirect(action_for('.edit', id=id))

    setting.name = name
    setting.config = new_config
    setting.save()

    return redirect(action_for('.index'))

@bp.route('/<int:id>/update', methods=['POST'])
def update(id):
    setting = Setting.select().where(Setting.id == id).first()

    name = request.form.get('name', 'Untitled')
    keys = request.form.getlist('keys[]')
    values = request.form.getlist('values[]')

    new_config = generate_config(keys, values)
    if new_config is None:
        return redirect(action_for('.edit', id=id))

    setting.name = name
    setting.config = new_config
    setting.save()

    return redirect(action_for('.index'))

def generate_config(keys, values):
    config = {}

    for k, v in zip(keys, values):
        if k == '' and v != '':
            flash('Key cannot be empty', 'danger')
            return None

        if k == '':
            continue

        try:
            config[k] = v
        except json.JSONDecodeError:
            flash(f'Invalid JSON for key-value pair: {k}: {v}', 'danger')
            return None

    return config
