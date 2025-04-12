from flask import Flask
import jinja_partials
from flask_socketio import SocketIO
from app.routes import draw_routes_for
from tools.flasktools import action_for
import os

def create_app():
    app = Flask(__name__)
    socketio = SocketIO(app, async_mode='eventlet')
    jinja_partials.register_extensions(app)

    app.socketio = socketio

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')

    draw_routes_for(app)

    @app.context_processor

    def expose_helpers():
        return dict(action_for=action_for)

    return app, socketio
