import json
from flask import redirect, flash
from app.models import Device
from tools.flasktools import *

bp = auto_blueprint()

# index route
@bp.route('/')
def index():
    devices = Device.all()
    return render('index', devices=devices)

# show route
@bp.route('/<int:id>')
def show(id):
    device = Device.find(id)

    return render('show', device=device)


# new route
@bp.route('/new')
def new():
    device = Device()
    return render('new', device=device)


# create route
@bp.route('/', methods=['POST'])
def create():
    Device.create_with(device_params)
    flash('Device created successfully.', 'success')

    return redirect(url_for('.index'))


# edit route
@bp.route('/<int:id>/edit')
def edit(id):
    device = Device.find(id)

    if not device:
        flash('Device not found.', 'error')
        return redirect(url_for('.index'))

    return render('edit', device=device)


# update route
@bp.route('/<int:id>', methods=['POST'])
def update(id):
    device = Device.find(id)

    if not device:
        flash('Device not found.', 'error')
        return redirect(url_for('.index'))

    device.update_with(device_params)
    flash('Device updated successfully.', 'success')

    return redirect(url_for('.index'))


# destroy route
@bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    device = Device.find(id)
    if device:
        device.destroy()

        flash('Device deleted successfully.', 'success')
    else:
        flash('Device not found.', 'error')

    return redirect(url_for('.index'))


def device_params():
    return params().permit('name', 'hash')
