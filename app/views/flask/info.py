from flask import current_app
from tools.flasktools import *

bp = auto_blueprint()

@bp.route('/', methods=['GET'])
def index():
    return render('index', routes=get_routes(current_app))
