from flask import Flask
import jinja_partials
from flask_socketio import SocketIO

from app.configs import base
from app.routes import draw_routes_for

def create_app(settings, config):
    app = Flask(__name__)
    socketio = SocketIO(app, async_mode='eventlet')
    jinja_partials.register_extensions(app)

    app.config.update(config)
    app.settings = settings
    app.socketio = socketio

    app.config['SECRET_KEY'] = app.settings['secret']

    draw_routes_for(app)

    return app, socketio
