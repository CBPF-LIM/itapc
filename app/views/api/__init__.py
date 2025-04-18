from flask import request
from app import data_processor
from app.services import ita
from tools.flasktools import *
from app.data_processor import success, error, process_post, process_get

bp = auto_blueprint()

@bp.route('/data', methods=['POST'])
def add_data():
    data = ita.create_data(request.json)

    if data.get('error'):
        payload = error(data['error'], 'POST')
    else:
        experiment_id = data['experiment_id']
        update_experiment_channel(experiment_id)
        payload = success(data, 'POST')

    return process_post(payload)


@bp.route('/exp', methods=['POST'])
def find_or_create_experiment():
    data = ita.find_or_create_experiment(request.json)

    if data.get('error'):
        payload = error(data['error'], 'POST')
    else:
        payload = success(data, 'POST')

    return process_post(payload)


@bp.route('/device', methods=['POST'])
def find_or_create_device():
    data = ita.find_or_create_device(request.json)

    if data.get('error'):
        payload = error(data['error'], 'POST')
    else:
        payload = success(data, 'POST')

    return process_post(payload)


@bp.route('/exp/<int:experiment_id>/cmd/<string:cmd>', methods=['GET'])
def run_exp_cmd(experiment_id, cmd):
    data = ita.run_exp_cmd(experiment_id, cmd)

    if data.get('error'):
        payload = error(data['error'])
    else:
        payload = success(data)

    return process_get(payload)


@bp.route('/exp/<int:experiment_id>/config/<string:key>', methods=['GET'])
def get_exp_config(experiment_id, key):
    data = ita.get_exp_config(experiment_id, key)

    if data.get('error'):
        payload = error(data['error'])
    else:
        payload = success(data)

    return process_get(payload)


def update_experiment_channel(experiment_id):
    if experiment_id:
        channel = f'update-{experiment_id}'
        print(f"Processed: Request: {request.json}")
        emitter(channel, experiment_id)
