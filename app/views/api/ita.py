import os
import json
from tools import filelines
from tools.shortcuts import b
from datetime import datetime
import app.models as models

settings = {}

def use_settings(new_settings):
    global settings
    settings = new_settings

def success(data, type='GET'):
    data = { 'response': 'success', 'type': type, 'data': data}
    print('data: ', data)
    return data

def error(message=None, type='GET'):
    data = { 'response': 'error', 'type': type, 'message': message or 'Something went wrong' }
    return data

def last_index():
    if not os.path.isfile(settings['output']):
        return 0

    line = filelines.tail(settings['output'])
    if line is None:
        return 0

    return 0 if line[0] == None else int(line[0].split('\t')[1])

def configs():
    try:
      with open(settings['config'], 'r') as f:
        return ''.join(f.readlines())
    except:
      return None

def config(key):
    try:
      with open(settings['config'], 'r') as f:
        for line in f:
          k, v =  line.split(':')
          k = k.strip()
          v = v.strip()
          if k == key:
            return v
    except:
      return None

def validate_index(index):
    index = int(index)
    last_file_index = last_index()
    if index == last_file_index:
       return f'Index [{index}] already exists'

    if index < last_file_index:
       return f'Index [{index}] is less than last index [{last_file_index}]'

    if index > last_file_index + 1:
       return f'Received index [{index}] but next index should be [{last_file_index + 1}]'

    return None

def save_data(data):
  experiment = models.Experiment.get_or_none(models.Experiment.name == data["experiment"])

  if not experiment:
    number_of_cols = len(data["cols"])
    header = [f"Col {i+1}" for i in range(number_of_cols)]

    experiment = models.Experiment.create(
        name=data["experiment"],
        header=json.dumps(header)
    )

  device = models.Device.get_or_none(models.Device.hash == data["device"])

  if not device:
    device = models.Device.create(
      hash=data["device"]
    )

  # Create Data entry
  d = models.Data.create(
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
