from flask import Flask, g
from flask_socketio import SocketIO
import jinja_partials
from tools.flasktools import register_flasktools_helpers
from app.environment import ENV
from app.routes import draw_routes_for
from app.secret import get_app_secret

def create_app():
    app = Flask(__name__)
    app.ENV = ENV
    app.config['SECRET_KEY'] = get_app_secret()
    app.socketio = SocketIO(app, async_mode='eventlet')
    jinja_partials.register_extensions(app)
    register_flasktools_helpers(app)

    app.boot_params = {
        'host': app.ENV['host'],
        'port': app.ENV['port'],
        'debug': app.ENV['debug']
    }

    draw_routes_for(app)

    return app
