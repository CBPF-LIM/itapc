import json
from tools.shortcuts import b
from datetime import datetime
from app.models import Experiment, Device, Data
from app.data_processor import success, error

def save_data(data):
  experiment = Experiment.get_or_none(Experiment.name == data["experiment"])

  if not experiment:
    number_of_cols = len(data["cols"])
    header = [f"Col {i+1}" for i in range(number_of_cols)]

    experiment = Experiment.create(
        name=data["experiment"],
        header=json.dumps(header)
    )

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
    if 'cmd' in query:
        cmd = query['cmd']
        if cmd == 'last-index':
            return success(last_index())
        elif cmd == 'configs':
            return success(configs())

    elif 'config' in query:
        return success(config(query['config']))

    if query == {}:
        return success('Nothing to do')

    return error('Invalid command')

def processPost(data):
    if 'cols' in data:
        return save_data(data)

    return error('Invalid data')
