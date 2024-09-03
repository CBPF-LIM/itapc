import os
from flask import Blueprint, request, jsonify, render_template, redirect, current_app, url_for
from tools.filelines import tail_index, lines2rowcol

bp = Blueprint('view', __name__)

def emitter():
    return current_app.socketio.emit

@bp.route('/')
def view_route():
    return render_template('view.html')

@bp.route('/chart')
def view_chart():
    with open('data.csv', 'r') as f:
        line = f.readline()

    headers = line.strip().split('\t')
    headers = [ h.strip().strip('"') for h in headers ]

    return render_template('chart.html', headers=headers)

@bp.route('/chart/data', methods=['POST'])
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
        if col == x:
            x_index = i
        if col.strip('"') == y:
            y_index = i
        i += 1

    x_data = []
    y_data = []
    for line in lines[1:]:
        data = line.strip().split('\t')
        x_data.append(data[x_index])
        y_data.append(data[y_index])

    x_data = [ str(d).strip().strip('"') for d in x_data ]
    y_data = [ str(d).strip().strip('"') for d in y_data ]

    return jsonify({'x': x_data, 'y': y_data })


@bp.route('/lines/from_index/<int:index>', methods=['GET'])
def view_from(index):
    lines = tail_index('data.csv', index)
    rows = lines2rowcol(lines)
    data = { 'response': 'success', 'type': 'GET', 'data': rows }

    return jsonify(data)

@bp.route('/logs', methods=['GET'])
def view_logs():
    # open error log if exists
    if os.path.exists('error.log'):
        with open('error.log', 'r') as f:
            logs = f.readlines()
    else:
        logs = []

    return render_template('logs.html', logs=logs)

@bp.route('/logs/clear', methods=['GET'])
def clear_logs():
    with open('error.log', 'w') as f:
        f.write('')

    return redirect(url_for('view.view_logs'))

@bp.route('/tools', methods=['GET'])
def view_tools():
    return render_template('tools.html')
