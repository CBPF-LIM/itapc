import json
from flask import redirect, flash
from app.models import Device
from tools.flasktools import *
from tools.shortcuts import b

bp = auto_blueprint()

# index route
@bp.route('/')
def index():
    devices = Device.select()
    return render('index', devices=devices)

# show route
@bp.route('/<int:id>')
def show(id):
    device = Device.get_or_none(Device.id == id)

    return render('show', device=device)


# new route
@bp.route('/new')
def new():
    device = Device()
    return render('new', device=device)


# create route
@bp.route('/', methods=['POST'])
def create():
    device = Device()
    device.name = request.form.get('name', '')
    device.hash = request.form.get('hash', '')
    device.save()
    flash('Device created successfully.', 'success')

    return redirect(url_for('.index'))


# edit route
@bp.route('/<int:id>/edit')
def edit(id):
    device = Device.get_or_none(Device.id == id)

    if not device:
        flash('Device not found.', 'error')
        return redirect(url_for('.index'))

    return render('edit', device=device)


# update route
@bp.route('/<int:id>', methods=['POST'])
def update(id):
    device = Device.get_or_none(Device.id == id)
    if not device:
        flash('Device not found.', 'error')
        return redirect(url_for('.index'))

    device.name = request.form.get('name', '')
    device.hash = request.form.get('hash', '')

    device.save()
    flash('Device updated successfully.', 'success')

    return redirect(url_for('.index'))


# destroy route
@bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    device = Device.get_or_none(Device.id == id)
    if device:
        device.delete_instance()

        flash('Device deleted successfully.', 'success')
    else:
        flash('Device not found.', 'error')

    return redirect(url_for('.index'))
