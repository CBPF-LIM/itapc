import json
from flask import redirect, flash
from app.models import Experiment, Data, Setting
from flasktools import *

bp = auto_blueprint()

# index route
@bp.route('/')
def index():
    experiments = Experiment.select()
    return render('index', experiments=experiments)


# show route
@bp.route('/<int:id>')
def show(id):
    experiment = Experiment.get_or_none(Experiment.id == id)

    return render('show', experiment=experiment)


# show_table route
@bp.route('/table/<int:id>')
def show_table(id):
    experiment = Experiment.get_or_none(Experiment.id == id)

    return render('show_table', experiment=experiment)


# show_chart route
@bp.route('/chart/<int:id>')
def show_chart(id):
    experiment = Experiment.get_or_none(Experiment.id == id)

    return render('show_chart', experiment=experiment)


# new route
@bp.route('/new')
def new():
    experiment = Experiment()
    experiment.header = {}
    settings = Setting.select()
    return render('new', experiment=experiment, settings=settings)


# create route
@bp.route('/', methods=['POST'])
def create():
    experiment = Experiment()
    experiment.name = request.form.get('name', '')
    experiment.header = json.loads(request.form.get('header', '{}'))

    setting_id = request.form.get('setting')
    experiment.setting = Setting.get_or_none(Setting.id == setting_id)

    if experiment.setting:
        experiment.setting_id = experiment.setting.id

    if experiment.name == '':
        flash('Experiment name is required.', 'error')
        return redirect(url_for('.new'))

    experiment.save()
    flash('Experiment created successfully.', 'success')

    return redirect(url_for('.index'))


# edit route
@bp.route('/<int:id>/edit')
def edit(id):
    experiment = Experiment.get_or_none(Experiment.id == id)
    settings = Setting.select()

    if not experiment:
        flash('Experiment not found.', 'error')
        return redirect(url_for('.index'))

    return render('edit', experiment=experiment, settings=settings)


# update route
@bp.route('/<int:id>', methods=['POST'])
def update(id):
    experiment = Experiment.get_or_none(Experiment.id == id)
    if not experiment:
        flash('Experiment not found.', 'error')
        return redirect(url_for('.index'))

    experiment.name = request.form.get('name', '')
    experiment.header = json.loads(request.form.get('header', '{}'))

    setting_id = request.form.get('setting')
    experiment.setting = Setting.get_or_none(Setting.id == setting_id)

    if experiment.setting:
        experiment.setting_id = experiment.setting.id

    if experiment.name == '':
        flash('Experiment name is required.', 'error')
        return redirect(url_for('.edit', id=id))

    experiment.save()
    flash('Experiment updated successfully.', 'success')

    return redirect(url_for('.show', id=id))


# destroy route
@bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    experiment = Experiment.get_or_none(Experiment.id == id)
    if experiment:
        Data.delete().where(Data.experiment == experiment).execute()
        experiment.delete_instance()

        flash('Experiment deleted successfully.', 'success')
    else:
        flash('Experiment not found.', 'error')

    return redirect(url_for('.index'))
