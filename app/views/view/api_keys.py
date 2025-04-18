from flask import redirect, flash
from app.models import ApiKey
from tools.flasktools import *
import secrets
import string

bp = auto_blueprint()

# index route
@bp.route('/')
def index():
    api_keys = ApiKey.all()
    return render('index', api_keys=api_keys)

# show route
@bp.route('/<int:id>')
def show(id):
    api_key = ApiKey.find(id)

    return render('show', api_key=api_key)


# new route
@bp.route('/new')
def new():
    api_key = ApiKey()
    return render('new', api_key=api_key)


# create route
@bp.route('/', methods=['POST'])
def create():
    api_key = ApiKey.new_with(api_key_params)
    api_key.hash = secure_token()
    api_key.save()

    flash('ApiKey created successfully.', 'success')

    return redirect(url_for('.index'))


# edit route
@bp.route('/<int:id>/edit')
def edit(id):
    api_key = ApiKey.find(id)

    if not api_key:
        flash('ApiKey not found.', 'error')
        return redirect(url_for('.index'))

    return render('edit', api_key=api_key)


# update route
@bp.route('/<int:id>', methods=['POST'])
def update(id):
    api_key = ApiKey.find(id)

    if not api_key:
        flash('ApiKey not found.', 'error')
        return redirect(url_for('.index'))

    api_key.update_with(api_key_params)
    flash('ApiKey updated successfully.', 'success')

    return redirect(url_for('.index'))


# destroy route
@bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    api_key = ApiKey.find(id)
    if api_key:
        api_key.destroy()

        flash('ApiKey deleted successfully.', 'success')
    else:
        flash('ApiKey not found.', 'error')

    return redirect(url_for('.index'))


def api_key_params():
    return params().permit('name')

def secure_token(length=22):
    alphabet = string.ascii_letters + string.digits
    part1 = ''.join(secrets.choice(alphabet) for _ in range(4))
    part2 = ''.join(secrets.choice(alphabet) for _ in range(4))
    part3 = ''.join(secrets.choice(alphabet) for _ in range(4))
    part4 = ''.join(secrets.choice(alphabet) for _ in range(4))
    return '_'.join([part1, part2, part3, part4])
