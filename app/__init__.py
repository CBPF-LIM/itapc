from flask import Flask, request, jsonify, render_template, redirect
from flask_socketio import SocketIO, emit

from app import response
from tools.shortcuts import b
from tools.filelines import tail_index, lines2rowcol
import os

def create_app(processPost, processGet):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'app_secret_key'
    socketio = SocketIO(app, async_mode='eventlet')
    emitter = socketio.emit

    @app.route('/ita/exec', methods=['POST'])
    @app.route('/ita/exec/', methods=['POST'])
    def doPost():
        data = processPost(request.json)
        processed_data = response.process(data)
        emitter('done')

        return processed_data

    @app.route('/ita/exec', methods=['GET'])
    @app.route('/ita/exec/', methods=['GET'])
    def doGet():
        q = request.args.to_dict()
        data = processGet(q)
        return response.process(data)

    @app.route('/ita/view')
    def view_route():
        return render_template('view.html')

    @app.route('/ita/view/lines/from_index/<int:index>', methods=['GET'])
    def view_from(index):
        lines = tail_index('data.csv', index)
        rows = lines2rowcol(lines)
        data = { 'response': 'success', 'type': 'GET', 'data': rows }

        return jsonify(data)

    @app.route('/ita/view/logs', methods=['GET'])
    def view_logs():
        # open error log if exists
        if os.path.exists('error.log'):
            with open('error.log', 'r') as f:
                logs = f.readlines()
        else:
            logs = []

        return render_template('logs.html', logs=logs)

    @app.route('/ita/view/logs/clear', methods=['GET'])
    def clear_logs():
        with open('error.log', 'w') as f:
            f.write('')

        return redirect('/ita/view/logs')


    @app.route('/ita/view/tools', methods=['GET'])
    def view_tools():
        return render_template('tools.html')


    return app
