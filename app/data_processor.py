import time
from flask import jsonify

def success(data, type='GET'):
    data = {
        'response': 'success',
        **data
    }
    return data

def error(message=None, type='GET'):
    data = {
        'response': 'error',
        'message': message or 'Something went wrong'
    }
    return data

def log_for(payload, method):
    now = time.strftime('%Y-%m-%d %H:%M:%S')

    if 'error' in payload['response']:
        open('error.log', 'a').write(f'{now}\t{method}\t{payload["message"]}\n')

        return f'error: {payload["message"]}'

def process_get(payload):
    error = log_for(payload, 'GET')
    if error:
        return error

    return str(payload['data']), 200

def process_post(payload):
    error = log_for(payload, 'POST')
    if error:
        data = { 'response': 'error', 'message': error }
        return jsonify(data), 404

    return jsonify(payload), 200
