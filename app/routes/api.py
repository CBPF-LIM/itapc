from flask import Blueprint, request, current_app
from app import response
import ita

bp = Blueprint('api', __name__)

def emitter(event, data):
    return current_app.socketio.emit(event, data)

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
