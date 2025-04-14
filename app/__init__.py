from flask import Flask
from flask_socketio import SocketIO
import jinja_partials
from tools.flasktools import register_flasktools_helpers
from app.environment import ENV, config_class
from app.routes import draw_routes_for
from app.secret import get_app_secret
from app.models import db, init_db

def create_app():
    app = Flask(__name__)
    app.ENV = ENV
    print(app.ENV)

    app.config.from_object(config_class())
    db.init(app.config['DATABASE'])

    app.config['SECRET_KEY'] = get_app_secret()
    app.socketio = SocketIO(app, async_mode='eventlet')
    jinja_partials.register_extensions(app)
    register_flasktools_helpers(app)

    app.boot_params = {
        'host': app.ENV['host'],
        'port': app.ENV['port'],
        'debug': app.ENV['debug']
    }

    with app.app_context():
        db.init(app.config['DATABASE'])
        init_db()

    draw_routes_for(app)

    return app
