from flask import request
from app import response
import app.ita as ita
from tools.flasktools import *

bp = auto_blueprint()

@bp.route('/', methods=['POST'])
def doPost():
    data = ita.processPost(request.json)
    processed_data = response.process(data)

    if data['response'] == 'success':
        channel = data.get('data', 'done').get('channel', 'done')
        print(f"Emitting to channel: {channel}")
        print(f"Data: {data}")
        emitter(channel, data)

    return processed_data

@bp.route('/', methods=['GET'])
def doGet():
    q = request.args.to_dict()
    data = ita.processGet(q)
    return response.process(data)
