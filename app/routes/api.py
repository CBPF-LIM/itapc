from flask import Blueprint, request, current_app
from app import response
import ita

bp = Blueprint('api', __name__)

def emitter():
    return current_app.socketio.emit

@bp.route('/', methods=['POST'])
def doPost():
    data = ita.processPost(request.json)
    processed_data = response.process(data)

    if data['response'] == 'success':
        emitter()

    return processed_data

@bp.route('/', methods=['GET'])
def doGet():
    q = request.args.to_dict()
    data = ita.processGet(q)
    return response.process(data)
