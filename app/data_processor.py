import time
from tools.shortcuts import b
from flask import jsonify

def success(data, type='GET'):
    data = {
        'response': 'success',
        'type': type,
        'data': data
    }
    return data

def error(message=None, type='GET'):
    data = {
        'response': 'error',
        'type': type,
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
        data = { 'response': 'error', 'type': 'POST', 'message': error }
        return jsonify(data), 404

    return jsonify({'response': 'success'}), 200

def response(data):
    if data['type'] == 'GET':
        return process_get(data)

    if data['type'] == 'POST':
        return process_post(data)
