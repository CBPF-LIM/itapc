import json
from datetime import datetime
from app.models import Experiment, Device, Data, ApiKey
from app.data_processor import success, error

def create_data(data):
  experiment_id = data.get('exp')

  experiment = Experiment.find(experiment_id)
  if not experiment:
    return {'error': f'Experiment id={experiment_id} not found!'}

  device_id = data.get('device')
  device = Device.find(device_id)
  if not device:
    return {'error': f'Device id={device_id} not found!'}

  if not check_api_authetication(experiment, data.get("apikey")):
    return {'error': 'Unauthorized!'}

  Data.create(
    experiment=experiment,
    device=device,
    t0=data["t0"],
    t1=data["t1"],
    timestamp=datetime.now(),
    _cols=json.dumps(data["cols"])
  )

  return {'experiment_id': experiment.id }

def find_or_create_experiment(data):
    name = data.get('name')

    if not name:
        return {'error': 'Missing experiment name'}

    experiment = Experiment.find_by(name=name)

    if experiment:
        new = False
    else:
        new = True

        try:
            raw_header = data.get('header')
            header = json.dumps(raw_header)
        except:
            return {'error': 'Invalid header: Must be a JSON array'}

        experiment = Experiment.create_with({"name": name, "header": header})

    return { 'id': experiment.id, 'new': new }


def find_or_create_device(data):
    hash = data.get('hash')

    if not hash:
        return {'error': 'Missing unique hash for device'}

    device = Device.get_or_none(Device.hash == hash)

    if not device:
        name = data.get('name', 'Untitled')
        device = Device.create(name=name, hash=hash)
        new = True
    else:
        new = False

    return { 'id': device.id, 'new': new }

def run_exp_cmd(experiment_id, cmd):
    experiment = Experiment.find(experiment_id)

    if not experiment:
        return {'error': f'Experiment id={experiment_id} not found!'}

    if not experiment.setting:
        return {'data': ''}

    if cmd == 'configs':
        return {'data': experiment.setting.config}

def get_exp_config(experiment_id, key):
    experiment = Experiment.find(experiment_id)
    if not experiment:
        return {'error': f'Experiment id={experiment_id} not found!'}
    if not experiment.setting:
        return {'error': 'Experiment has no settings'}

    if not experiment.setting.config:
        return {'error': 'Experiment has no settings config'}

    if key not in experiment.setting.config:
        return {'data': ''}

    return {'data': experiment.setting.config[key]}

def check_api_authetication(experiment, hash):
    settings = experiment.setting
    if settings:
        config = settings.config
        if config:
            api_key_id = config.get('api_key_id')
            if api_key_id:
                api_key = ApiKey.get_or_none(ApiKey.id == api_key_id)
                return hash == api_key.hash
            else:
                return True # No api_key_id? Disable authentication
        else:
            return True # No config? Disable authentication
    else:
        return True # No settings? Disable authentication
