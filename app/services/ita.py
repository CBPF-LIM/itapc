import json
from datetime import datetime
from app.models import Experiment, Device, Data, ApiKey
from app.data_processor import success, error

def save_data(data):
  experiment_id = data.get("exp")
  experiment = Experiment.get_or_none(Experiment.id == experiment_id)

  if not experiment:
    number_of_cols = len(data["cols"])
    header = [f"Col {i+1}" for i in range(number_of_cols)]

    experiment = Experiment.create(
        name='Untitled Experiment',
        header=json.dumps(header)
    )
  else:
    if not check_api_authetication(experiment, data.get("apikey")):
        return error('Unauthorized!', 'POST')

  device = Device.get_or_none(Device.hash == data["device"])

  if not device:
    device = Device.create(
      hash=data["device"]
    )

  # Create Data entry
  d = Data.create(
      experiment=experiment,
      device=device,
      t0=data["t0"],
      t1=data["t1"],
      timestamp=datetime.now(),
      _cols=json.dumps(data["cols"])
  )

  response = {'channel': f'update-{experiment.id}'}

  # index_error = validate_index(index)
  # if index_error:
  #   return error(index_error, 'POST')

  return success(response, 'POST')

def processGet(query):
    experiment_id = query.get('exp')
    experiment = Experiment.get_or_none(Experiment.id == experiment_id)

    if not experiment:
        return error('Experiment not found')

    if 'cmd' in query:
        cmd = query['cmd']

        if cmd == 'configs':
            return success(experiment.setting.config)

    elif 'config' in query:
        key = query['config']
        value = experiment.setting.config.get(key)

        if value:
            return success(value)
        else:
            return error('Config not found')

    if query == {}:
        return success('Nothing to do')

    return error('Invalid command')

def processPost(data):
    if 'cols' in data:
        return save_data(data)

    return error('Invalid data')

def check_api_authetication(experiment, hash):
    settings = experiment.setting
    print('settings', settings)
    if settings:
        config = settings.config
        print('config', config)
        if config:
            api_key_id = config.get('api_key_id')
            print('api_key_id', api_key_id)
            if api_key_id:
                api_key = ApiKey.get_or_none(ApiKey.id == api_key_id)
                return hash == api_key.hash
            else:
                return True # No api_key_id? Disable authentication
        else:
            return True # No config? Disable authentication
    else:
        return True # No settings? Disable authentication
