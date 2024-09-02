from flask import Flask, request, jsonify, render_template, redirect
import jinja_partials
from flask_socketio import SocketIO, emit

from app import response
from tools.shortcuts import b
from tools.filelines import tail_index, lines2rowcol
import os

def create_app(processPost, processGet):
    app = Flask(__name__)
    jinja_partials.register_extensions(app)

    app.config['SECRET_KEY'] = 'app_secret_key'
    socketio = SocketIO(app, async_mode='eventlet')
    emitter = socketio.emit

    @app.route('/ita/exec', methods=['POST'])
    @app.route('/ita/exec/', methods=['POST'])
    def doPost():
        data = processPost(request.json)
        processed_data = response.process(data)

        if data['response'] == 'success':
            emitter('done', data)

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

    @app.route('/ita/view/chart')
    def view_chart():
        with open('data.csv', 'r') as f:
            line = f.readline()

        headers = line.strip().split('\t')
        headers = [ h.strip().strip('"') for h in headers ]

        return render_template('chart.html', headers=headers)

    @app.route('/ita/view/chart/data', methods=['POST'])
    def view_chart_data():
        x = request.json['x']
        y = request.json['y']
        #n = request.json['n']

        with open('data.csv', 'r') as f:
            lines = f.readlines()

        headers = lines[0].split('\t')

        x_index = -1
        y_index = -1

        i = 0
        for header in headers:
            col = header.strip().strip('"')
            print('header:', col)
            print('x:', x)
            print('y:', y)
            if col == x:
                print('found x')
                x_index = i
            if col.strip('"') == y:
                print('found y')
                y_index = i
            i += 1

        x_data = []
        y_data = []

        x_data = []
        y_data = []
        for line in lines[1:]:
            data = line.strip().split('\t')
            x_data.append(data[x_index])
            y_data.append(data[y_index])

        x_data = [ str(d).strip().strip('"') for d in x_data ]
        y_data = [ str(d).strip().strip('"') for d in y_data ]

        print('x_data:', x_data)
        print('y_data:', y_data)


        return jsonify({'x': x_data, 'y': y_data })


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

    @app.route('/', methods=['GET'])
    def app_index():
        return redirect('/ita/view')


    return app
