import os
import time
from tools import filelines
from tools.shortcuts import b
from datetime import datetime

output_file = ""
config_file = ""

if os.path.isfile('app.ini'):
    with open('app.ini', 'r') as f:
        for line in f:
            if line.startswith('output:'):
                output_file = line.split(':')[1].strip()
            if line.startswith('config:'):
                config_file = line.split(':')[1].strip()

if output_file == "":
  output_file = os.getenv('ITA_OUTPUT_FILE', 'data.csv')

if config_file == "":
  config_file = os.getenv('ITA_CONFIG_FILE', 'config.ini')

print('Using output file:', output_file)
print('Using config file:', config_file)

file_folder = 'data'

t0 = 0
first_data = True

def success(data, type='GET'):
    return { 'response': 'success', 'type': type, 'data': data}

def error(message=None, type='GET'):
    return { 'response': 'error', 'type': type, 'message': message or 'Something went wrong' }

def last_index():
    if not os.path.isfile(output_file):
        return 0
    line = filelines.last(output_file)
    return 0 if line == None else int(line.split('\t')[1])

def configs():
    try:
      with open(config_file, 'r') as f:
        return ''.join(f.readlines())
    except:
      return None

def config(key):
    try:
      with open(config_file, 'r') as f:
        for line in f:
          k, v =  line.split(':')
          k = k.strip()
          v = v.strip()
          if k == key:
            return v
    except:
      return None

def save_data(data):
    global first_data
    global t0
    #try:

    with open(output_file, 'a') as f:
      if first_data:
        t0 = time.time()

      t1 = time.time()
      millis = round((t1 - t0)*1000)

      index = last_index() + 1

      dt_object = datetime.fromtimestamp(t1)
      formatted_t1 = dt_object.strftime('%d/%m/%Y %H:%M:%S')
      formatted_t1 = f'"{formatted_t1}"'

      content = [formatted_t1, index, millis]

      for item in data:
         if type(item) == str:
            content.append(f'"{item}"')
         else:
            content.append(item)

      if index == 1:
        col_ms = f'"{config("col_ms") or "ms"}"'

        col_index = f'"{config("col_index") or "Index"}"'
        col_timestamp = f'"{config("col_timestamp") or "Timestamp"}"'

        col_names = [col_timestamp, col_index, col_ms]
        for n in range(1, len(data) + 1):
          col_name = config('col' + str(n))
          if col_name:
            col_names.append(f'"{col_name}"')
          else:
            col_names.append(f'"col{n}"')

        f.write('\t'.join(col_names) + '\n')

      joined_string = '\t'.join(str(item) for item in content)

      f.write(joined_string + '\n')
      first_data = False
    return True
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
        return success(save_data(data['cols']))

    return error('Invalid data: cols key not found in JSON')
