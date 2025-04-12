from flask import request
from app import data_processor
from app.services import ita
from tools.flasktools import *
from tools.shortcuts import b

bp = auto_blueprint()

@bp.route('/', methods=['POST'])
def doPost():
    data = ita.processPost(request.json)
    update_channel(data)
    return data_processor.response(data)

@bp.route('/', methods=['GET'])
def doGet():
    q = request.args.to_dict()
    data = ita.processGet(q)
    return data_processor.response(data)

def update_channel(data):
    if data['response'] == 'success':
        channel = data.get('data', 'done').get('channel', 'done')
        print(f"Processed: Request: {request.json}")
        print(f"           Response: {data}")
        emitter(channel, data)
