import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import pytest
from app.main import create_app
import ita
from tools.shortcuts import b
from tools import filelines
import time
from datetime import datetime

from app import config_parser
from app.main import process_args

with open('app_test.ini', 'w') as f:
    app_ini = """port: 5001
host: localhost
debug: false
output: data_test.csv
output_mode: append
config: config_test.ini
"""
    f.write(app_ini)

from app import main

endpoint = 'http://localhost:5001/ita/exec'

def formated_time(t):
  dt_object = datetime.fromtimestamp(t)
  formatted = dt_object.strftime('%d/%m/%Y %H:%M:%S')
  return f'"{formatted}"'

def now():
   return formated_time(time.time())

def set_last_index_to(number):
    with open('data_test.csv', 'w') as f:
        f.write('"Timestamp"\t"Index"\t"ms"\t"Col1"\t"Col2"\t"Col3"\n')
        f.write(f'"{now()}"\t{number}\t1000\t100\t200\t300\n')

def set_config_file(content):
    with open('config_test.ini', 'w') as f:
        f.write(content)

def clear_csv():
    with open('data_test.csv', 'w') as f:
        f.write('')

@pytest.fixture
def client():
    # this is the copy of app.main() with some adjustments
    app = create_app(ita.processPost, ita.processGet)
    process_args()

    settings = {
      'output': 'data.csv',
      'output_mode': 'append',
      'config': 'config.ini',
      'host': '127.0.0.2',
      'debug': False,
      'port': 5000,
      'app_ini': 'app_test.ini'
    }

    app.settings = config_parser.load(settings)

    print('Ita PC is running')
    print('-' * 25)
    ita.use_settings(app.settings)
    print('-' * 25)
    print('> Starting server')
    print('-' * 25)

    if app.settings['output_mode'] == 'append':
        pass

    if app.settings['output_mode'] == 'fresh':
        try:
            os.remove(app.settings['output'])
        except:
            print(f'>>> Cannot remove file {app.settings["output"]}')

    if app.settings['output_mode'] == 'timestamp':
        filename = app.settings['output']

        dt_object = datetime.fromtimestamp(time.time())
        time_formatted = dt_object.strftime('%Y%m%d%H%M%S')

        app.settings['output'] = f'{filename}_{time_formatted}.csv'

    app.test_client()
    app.testing = True

    return app.test_client()

# Test GET /ita/exec
def test_get(client):
    response = client.get(endpoint)
    assert response.status_code == 200
    assert b'Nothing to do' in response.data

# Test GET /ita/exec?cmd=last-index
def test_get_last_index(client):
    set_last_index_to(0)
    response = client.get(endpoint + '?cmd=last-index')
    assert response.status_code == 200
    assert b'0' in response.data

# Test GET /ita/exec?cmd=last-index
# using a different data file with a different last index
def test_get_last_index_with_data(client):
    set_last_index_to(3)

    response = client.get(endpoint + '?cmd=last-index')
    assert response.status_code == 200
    assert b'3' in response.data

# Test GET /ita/exec?cmd=configs
def test_get_configs(client):
    set_config_file('key1: value1\nkey2: value2')
    response = client.get(endpoint + '?cmd=configs')
    assert response.status_code == 200
    assert b'key1: value1\nkey2: value2' in response.data

# Test GET /ita/exec?cmd=config&key=key1
def test_get_config(client):
    set_config_file('key1: value1\nkey2: value2')
    response = client.get(endpoint + '?config=key1')
    assert response.status_code == 200
    assert b'value1' in response.data

# Test POST /ita/exec
def test_post(client):
    clear_csv()
    response = client.post(endpoint, json={'cols': [1,2,3,4]})
    assert response.status_code == 200

    with open('data_test.csv', 'r') as f:
        f.readline()
        line = f.readline()

    assert '1\t2\t3\t4' in line

# Test POST /ita/exec
# after multiple POST requests
def test_post_multiple(client):
    clear_csv()
    client.post(endpoint, json={'cols': [1,2,3,4]})
    client.post(endpoint, json={'cols': [1,2,3,4]})
    response = client.post(endpoint, json={'cols': [10,20,30,40]})

    line = filelines.last('data_test.csv').strip()
    data = line.split('\t')

    assert data[1] == '3'
    assert data[3:7] == ['10', '20', '30', '40']
