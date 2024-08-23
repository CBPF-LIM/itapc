from flask import Flask, request, jsonify
from app import response
from tools.shortcuts import b

def create_app(processPost, processGet):
    app = Flask(__name__)

    @app.route('/ita/exec', methods=['POST'])
    @app.route('/ita/exec/', methods=['POST'])
    def doPost():
        data = processPost(request.json)
        return response.process(data)

    @app.route('/ita/exec', methods=['GET'])
    @app.route('/ita/exec/', methods=['GET'])
    def doGet():
        q = request.args.to_dict()
        data = processGet(q)
        return response.process(data)

    return app
