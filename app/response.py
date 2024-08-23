import json
from tools.shortcuts import b

def process_get(payload):
    if 'error' in payload['response']:
        return f'error: {payload["message"]}', 404

    return str(payload['data']), 200

def process_post(payload):
    if 'error' in payload['response']:
        return jsonify({'error': payload['message']}), 500

    return jsonify(payload['data']), 200

def process(data):
    if data['type'] == 'GET':
        return process_get(data)

    if data['type'] == 'POST':
        return process_post(data)
