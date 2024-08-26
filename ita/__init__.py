import os
import time
from tools import filelines
from tools.shortcuts import b
from datetime import datetime

settings = {}

def use_settings(new_settings):
    global settings
    settings = new_settings

def success(data, type='GET'):
    return { 'response': 'success', 'type': type, 'data': data}

def error(message=None, type='GET'):
    return { 'response': 'error', 'type': type, 'message': message or 'Something went wrong' }

def last_index():
    if not os.path.isfile(settings['output']):
        return 0
    line = filelines.last(settings['output'])
    return 0 if line == None else int(line.split('\t')[1])

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

def save_data(data):
    #try:

    #print('settings', settings)
    with open(settings['output'], 'a') as f:
      t = time.time()

      index = data[0]
      if index == last_index():
         return error(f'Index <{index}> already exists')

      dt_object = datetime.fromtimestamp(t)
      formatted_t = dt_object.strftime('%d/%m/%Y %H:%M:%S')
      formatted_t = f'"{formatted_t}"'

      content = [formatted_t, index]

      for item in data[1:]:
         if type(item) == str:
            content.append(f'"{item}"')
         else:
            content.append(item)

      if index == 1:
        col_timestamp = f'"{config("col_timestamp") or "Timestamp"}"'
        col_index = f'"{config("col_index") or "Index"}"'
        col_ms = f'"{config("col_ms") or "ms"}"'

        col_names = [col_timestamp, col_index, col_ms]
        for n in range(1, len(data[1:])):
          col_name = config('col' + str(n))
          if col_name:
            col_names.append(f'"{col_name}"')
          else:
            col_names.append(f'"col{n}"')

        f.write('\t'.join(col_names) + '\n')

      joined_string = '\t'.join(str(item) for item in content)

      f.write(joined_string + '\n')
    return success(True)
    #except:
    #  return None

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
        return save_data(data['cols'])

    return error('Invalid data: cols key not found in JSON')
