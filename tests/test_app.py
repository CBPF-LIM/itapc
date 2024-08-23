import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from tools import filelines
import time
from datetime import datetime

os.makedirs('tests/data', exist_ok=True)

os.environ['ITA_OUTPUT_FILE'] = 'tests/data_test.csv'
os.environ['ITA_CONFIG_FILE'] = 'tests/config_test.ini'
os.environ['FLASK_RUN_PORT'] = '5001'

from app import app

endpoint = 'http://localhost:5000/ita/exec'

def formated_time(t):
  dt_object = datetime.fromtimestamp(t)
  formatted = dt_object.strftime('%d/%m/%Y %H:%M:%S')
  return f'"{formatted}"'

def now():
   return formated_time(time.time())

def set_last_index_to(number):
    with open('tests/data_test.csv', 'w') as f:
        f.write('"Timestamp"\t"Index"\t"ms"\t"Col1"\t"Col2"\t"Col3"\n')
        f.write(f'"{now()}"\t{number}\t1000\t100\t200\t300\n')

def set_config_file(content):
    with open('tests/config_test.ini', 'w') as f:
        f.write(content)

def clear_csv():
    with open('tests/data_test.csv', 'w') as f:
        f.write('')

@pytest.fixture
def client():
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

    with open('tests/data_test.csv', 'r') as f:
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

    line = filelines.last('tests/data_test.csv').strip()
    data = line.split('\t')

    assert data[1] == '3'
    assert data[3:7] == ['10', '20', '30', '40']
